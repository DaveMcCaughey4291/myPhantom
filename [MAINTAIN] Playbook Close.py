"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_custom_list_copy_1' block
    get_custom_list_copy_1(container=container)

    return

def get_custom_list_copy_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_custom_list_copy_1() called")

    parameters = []

    parameters.append({
        "list_name": "test_list",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="myPhantom/get_custom_list_copy", parameters=parameters, name="get_custom_list_copy_1", callback=decision_1)

    return


def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["get_custom_list_copy_1:custom_function_result.data.status", "==", "success"]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        run_playbook_3(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    custom_function_failed_comment(action=action, success=success, container=container, results=results, handle=handle)

    return


def custom_function_failed_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("custom_function_failed_comment() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="The retrieve custom list data custom function has failed.")

    return


def run_playbook_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("run_playbook_3() called")

    get_custom_list_copy_1__result = phantom.collect2(container=container, datapath=["get_custom_list_copy_1:custom_function_result.data.list_of_items"])

    get_custom_list_copy_1_data_list_of_items = [item[0] for item in get_custom_list_copy_1__result]

    parameters = []

    parameters.append({
        "container_list": get_custom_list_copy_1_data_list_of_items,
        "playbook_name": "[Quick Close] No Threat",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="myPhantom/run_playbook", parameters=parameters, name="run_playbook_3")

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