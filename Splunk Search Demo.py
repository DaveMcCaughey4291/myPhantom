"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'run_query_1' block
    run_query_1(container=container)

    return

def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("run_query_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "command": "search",
        "query": "index=main host=uf1 COMMAND=sudo latest=-24h",
        "end_time": "-24h",
        "attach_result": True,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="run_query_1", assets=["splunk"], callback=parse_results)

    return


def parse_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("parse_results() called")

    run_query_1_result_data = phantom.collect2(container=container, datapath=["run_query_1:action_result.data"], action_results=results)

    run_query_1_result_item_0 = [item[0] for item in run_query_1_result_data]

    parse_results__usernames = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    phantom.debug(f"Search results: {run_query_1_result_item_0}")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_results:usernames", value=json.dumps(parse_results__usernames))

    artifact_create_1(container=container)

    return


def artifact_create_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("artifact_create_1() called")

    id_value = container.get("id", None)
    parse_results__usernames = json.loads(phantom.get_run_data(key="parse_results:usernames"))

    parameters = []

    parameters.append({
        "container": id_value,
        "name": "source user",
        "label": None,
        "severity": "medium",
        "cef_field": "sourceUsername",
        "cef_value": parse_results__usernames,
        "cef_data_type": "username",
        "tags": None,
        "run_automation": None,
        "input_json": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/artifact_create", parameters=parameters, name="artifact_create_1")

    return


def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return