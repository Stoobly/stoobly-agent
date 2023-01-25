import pdb

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings

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

        scenario_model = self.__scenario_model(context)
        scenario = scenario_model.create(**context.params)

        if not scenario:
            return context.internal_error()
        
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
        scenario = scenario_model.show(context.params.get('id'))

        if not scenario:
            return context.not_found()
        
        context.render(
            json = scenario,
            status = 200
        )

    # GET /scenarios
    def index(self, context):
        scenario_model = self.__scenario_model(context)
        requests = scenario_model.index(**context.params)

        context.render(
            json = requests,
            status = 200
        )

    # PUT /scenarios/:id
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        scenario_id = context.params.get('id')

        scenario_model = self.__scenario_model(context)
        scenario = scenario_model.update(scenario_id, **context.params.get('scenario'))

        if not scenario:
            return context.not_found()
            
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
        scenario = scenario_model.destroy(scenario_id)

        if not scenario:
           return context.not_found()

        context.render(
            plain = '',
            status = 200
        )

    def __scenario_model(self, context: SimpleHTTPRequestHandler):
        scenario_model = ScenarioModel(Settings.instance())
        scenario_model.as_remote() if context.headers.get('access-token') else scenario_model.as_local()
        return scenario_model