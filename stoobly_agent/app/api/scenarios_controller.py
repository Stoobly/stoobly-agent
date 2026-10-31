import pdb

from datetime import datetime

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.helpers.create_request_service import InvalidRequestFormatError
from stoobly_agent.app.models.import_ import IMPORT_FORMATS, get_importer
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.utils.decode import decode

class ScenariosController:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    # POST /scenarios
    def create(self, context: SimpleHTTPRequestHandler):
        body_params = context.params
        if not context.required_params(body_params, ['name']):
            return

        description = decode(body_params['description'] if 'description' in body_params else '')
        name = decode(body_params['name'])
        priority = decode(body_params['priority'] if 'priority' in body_params else '0')

        file_content = body_params.get('file')
        format = body_params.get('format')
        if format is not None:
            format = decode(format)

        if file_content is not None or format is not None:
            if format not in IMPORT_FORMATS:
                return context.bad_request(f"Invalid format. Expected one of: {', '.join(IMPORT_FORMATS)}")
            if file_content is None:
                return context.bad_request('Missing param file')

        scenario_model = self.__scenario_model(context)
        scenario, status = scenario_model.create(**{
            'name':name, 
            'description': description,
            'priority': priority,
        })

        if context.filter_response(scenario, status):
            return

        if file_content is not None:
            importer = get_importer(format)
            try:
                import_res, import_status = importer.import_file(
                    file_content,
                    scenario['uuid'],
                    settings=Settings.instance(),
                )
            except InvalidRequestFormatError as e:
                scenario_model.destroy(scenario['uuid'], force=True)
                return context.bad_request(str(e))

            if import_status >= 400:
                scenario_model.destroy(scenario['uuid'], force=True)
                error = import_res.get('error') if isinstance(import_res, dict) else import_res
                return context.bad_request(error or 'Could not import file')

            scenario, status = scenario_model.show(scenario['uuid'])
            if context.filter_response(scenario, status):
                return

        context.render(
            json = scenario,
            status = 200
        )

    # GET /scenarios/:id
    def get(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        scenario_model = self.__scenario_model(context)
        scenario, status = scenario_model.show(context.params.get('id'))

        if context.filter_response(scenario, status):
            return
        
        context.render(
            json = scenario,
            status = 200
        )

    # GET /scenarios
    def index(self, context: SimpleHTTPRequestHandler):
        scenario_model = self.__scenario_model(context)
        scenarios, status = scenario_model.index(**context.params)

        if context.filter_response(scenarios, status):
            return

        context.render(
            json = scenarios,
            status = 200
        )

    # PUT /scenarios/:id
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        scenario_id = context.params.get('id')

        scenario_model = self.__scenario_model(context)
        scenario, status = scenario_model.update(scenario_id, **context.params.get('scenario'))

        if context.filter_response(scenario, status):
            return
            
        context.render(
            json = scenario,
            status = 200
        )

    # DELETE /scenarios/:id
    def destroy(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        scenario_id = context.params.get('id')

        scenario_model = self.__scenario_model(context)
        scenario, status = scenario_model.destroy(scenario_id)

        if context.filter_response(scenario, status):
            return

        context.render(
            plain = '',
            status = 200
        )

    def download(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })
        scenario_id = int(context.params.get('id'))
        format = context.params.get('format')
        scenario = Scenario.find(scenario_id)

        if not scenario:
            return context.not_found()

        if format == 'gor':
            filename = f"SCENARIO-{int(datetime.now().timestamp())}.gor"
            requests = scenario.requests

            content = ''
            for request in requests:
                content = JoinedRequestStringAdapter(request).adapt(content)

            context.render(
                download = content,
                filename = filename,
                status = 200
            )
        else:
            return context.bad_request('Invalid format')

    def __scenario_model(self, context: SimpleHTTPRequestHandler):
        access_token = context.headers.get('access-token')
        scenario_model = ScenarioModel(Settings.instance(), access_token=access_token)
        return scenario_model