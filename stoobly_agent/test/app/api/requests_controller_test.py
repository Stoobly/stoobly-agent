import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
    return reset()


@pytest.fixture(scope='module')
def adapter():
    return LocalDBRequestAdapter(request_orm=Request, response_orm=Response)


@pytest.fixture(scope='module')
def created_request(settings: Settings):
    status = RequestBuilder(
        method='GET',
        request_body='',
        request_headers={},
        response_body='',
        status_code=200,
        url='https://petstore.swagger.io/v2/pets',
    ).with_settings(settings).build()[1]
    assert status == 200

    record = Request.last()
    yield record
    record.delete()


class TestUpdate:

    class TestWhenRestoringFromTrash:

        @pytest.fixture(autouse=True)
        def soft_delete_request(self, created_request):
            created_request.update({'is_deleted': True})
            yield
            created_request.update({'is_deleted': False})

        def test_it_returns_200(self, adapter, created_request):
            _, status = adapter.update(created_request.id, is_deleted=False)
            assert status == 200

        def test_it_unsets_is_deleted(self, adapter, created_request):
            response_body, _ = adapter.update(created_request.id, is_deleted=False)
            assert response_body['is_deleted'] == False

        def test_it_persists_is_deleted_false(self, adapter, created_request):
            adapter.update(created_request.id, is_deleted=False)
            refreshed = Request.find(created_request.id)
            assert refreshed.is_deleted == False

    class TestWhenRequestDoesNotExist:

        def test_it_returns_404(self, adapter):
            _, status = adapter.update(99999, is_deleted=False)
            assert status == 404

    class TestWhenMovingToTrashFromScenario:

        @pytest.fixture(autouse=True, scope='class')
        def scenario(self):
            record = Scenario.create(name='test scenario')
            yield record
            record.delete()

        @pytest.fixture(autouse=True, scope='class')
        def request_in_scenario(self, settings: Settings, scenario: Scenario):
            status = RequestBuilder(
                method='GET',
                request_body='',
                request_headers={},
                response_body='',
                status_code=200,
                url='https://petstore.swagger.io/v2/scenario-pets',
            ).with_settings(settings).build()[1]
            assert status == 200

            record = Request.last()
            record.update({'scenario_id': scenario.id})
            yield record
            record.delete()

        def test_it_clears_scenario_id(self, adapter, request_in_scenario: Request):
            adapter.update(request_in_scenario.id, is_deleted=True)
            refreshed = Request.find(request_in_scenario.id)
            assert refreshed.scenario_id is None

        def test_it_decrements_scenario_requests_count(self, adapter, scenario: Scenario, request_in_scenario: Request):
            # Use adapter (fetches fresh ORM object) so get_original() is accurate
            adapter.update(request_in_scenario.id, is_deleted=False, scenario_id=scenario.id)
            count_before = Scenario.find(scenario.id).requests_count

            adapter.update(request_in_scenario.id, is_deleted=True)

            assert Scenario.find(scenario.id).requests_count == count_before - 1

    class TestWhenRestoringFromTrashIntoScenario:

        @pytest.fixture(autouse=True, scope='class')
        def scenario(self):
            record = Scenario.create(name='restore target scenario')
            yield record
            record.delete()

        @pytest.fixture(autouse=True, scope='class')
        def trashed_request(self, settings: Settings):
            status = RequestBuilder(
                method='GET',
                request_body='',
                request_headers={},
                response_body='',
                status_code=200,
                url='https://petstore.swagger.io/v2/trashed-pets',
            ).with_settings(settings).build()[1]
            assert status == 200

            record = Request.last()
            record.update({'is_deleted': True})
            yield record
            record.delete()

        @pytest.fixture(autouse=True)
        def ensure_trashed(self, trashed_request: Request):
            Request.find(trashed_request.id).update({'is_deleted': True, 'scenario_id': None})
            yield
            # Restore cleanly after each test so class teardown doesn't double-decrement counts
            Request.find(trashed_request.id).update({'is_deleted': False, 'scenario_id': None})

        def test_it_assigns_scenario_id_without_is_deleted(self, adapter, trashed_request: Request, scenario: Scenario):
            """UI sends only scenario_id without is_deleted — server should auto-restore."""
            response_body, status = adapter.update(trashed_request.id, scenario_id=scenario.id)
            refreshed = Request.find(trashed_request.id)
            assert status == 200
            assert response_body['scenario_id'] == scenario.id
            assert refreshed.scenario_id == scenario.id

        def test_it_auto_restores_is_deleted_when_scenario_id_assigned(self, adapter, trashed_request: Request, scenario: Scenario):
            response_body, _ = adapter.update(trashed_request.id, scenario_id=scenario.id)
            refreshed = Request.find(trashed_request.id)
            assert refreshed.is_deleted == False
            assert response_body['is_deleted'] == False

        def test_it_increments_scenario_requests_count_without_is_deleted(self, adapter, trashed_request: Request, scenario: Scenario):
            count_before = Scenario.find(scenario.id).requests_count
            adapter.update(trashed_request.id, scenario_id=scenario.id)
            assert Scenario.find(scenario.id).requests_count == count_before + 1

        def test_it_restores_with_scenario_id(self, adapter, trashed_request: Request, scenario: Scenario):
            adapter.update(trashed_request.id, is_deleted=False, scenario_id=scenario.id)
            refreshed = Request.find(trashed_request.id)
            assert refreshed.is_deleted == False
            assert refreshed.scenario_id == scenario.id

        def test_it_increments_scenario_requests_count(self, adapter, trashed_request: Request, scenario: Scenario):
            # Use adapter (fetches fresh ORM object) so get_original() is accurate
            adapter.update(trashed_request.id, is_deleted=True)
            count_before = Scenario.find(scenario.id).requests_count

            adapter.update(trashed_request.id, is_deleted=False, scenario_id=scenario.id)

            assert Scenario.find(scenario.id).requests_count == count_before + 1
