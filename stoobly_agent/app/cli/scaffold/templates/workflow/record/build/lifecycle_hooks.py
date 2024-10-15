# This file defines lifecyle hooks for when Stoobly intercepts a request
from stoobly_agent.app.proxy.record.context import RecordContext

def handle_before_request(context: RecordContext):
    intercept_settings = context.intercept_settings
    flow = context.flow
    request = flow.request

    # For example, uncomment the following
    #print(f"Agent running in {intercept_settings.mode} mode with {intercept_settings.policy} policy")
    #print(dir(request))
        