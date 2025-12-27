import os
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.config.constants import custom_headers, env_vars
from stoobly_agent.lib.logger import Logger

LOG_ID = 'InterceptConcurrent'

# Only enable if AGENT_SIMULATE_LATENCY is set
if os.environ.get(env_vars.AGENT_SIMULATE_LATENCY):
    try:
        from mitmproxy.script import concurrent
    except ImportError:
        # Fallback if concurrent decorator is not available
        def concurrent(func):
            return func

    @concurrent
    def response(flow: 'MitmproxyHTTPFlow') -> None:
        """
        Simulate response latency using @concurrent to avoid blocking other requests.
        This handler runs in a separate thread, allowing mitmproxy to process other
        requests while this one is delayed.
        """
        # Check for latency header
        latency_header = flow.response.headers.get(custom_headers.RESPONSE_LATENCY)
        if not latency_header:
            return

        try:
            # Calculate wait time
            # wait_time (seconds) = expected_latency - estimated_rtt_network_latency - api_latency
            #
            # expected_latency = provided value (in milliseconds, converted to seconds)
            # estimated_rtt_network_latency = 15ms
            # api_latency = current_time - start_time of this request
            estimated_rtt_network_latency = 0.015  # seconds
            api_latency = time.time() - flow.request.timestamp_start
            expected_latency = float(latency_header) / 1000  # Convert ms to seconds

            wait_time = expected_latency - estimated_rtt_network_latency - api_latency

            Logger.instance(LOG_ID).debug(f"Expected latency: {expected_latency}")
            Logger.instance(LOG_ID).debug(f"API latency: {api_latency}")
            Logger.instance(LOG_ID).debug(f"Wait time: {wait_time}")

            if wait_time > 0:
                # With @concurrent, time.sleep() blocks only this request's thread,
                # allowing other requests to be processed concurrently
                time.sleep(wait_time)
        except (ValueError, TypeError, AttributeError) as e:
            Logger.instance(LOG_ID).warning(f"Error simulating latency: {e}")
