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
        run_playbook(action=action, success=success, container=container, results=results, handle=handle)
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


def run_playbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("run_playbook() called")

    get_custom_list_copy_1__result = phantom.collect2(container=container, datapath=["get_custom_list_copy_1:custom_function_result.data.list_of_items"])

    get_custom_list_copy_1_data_list_of_items = [item[0] for item in get_custom_list_copy_1__result]

    run_playbook__status = None
    run_playbook__message = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Setup variables
    num_success = 0
    num_failed = 0
    
    phantom.debug(f'Inputs: {get_custom_list_copy_1_data_list_of_items}')
    
    for item in get_custom_list_copy_1_data_list_of_items[0]:
        container = phantom.get_container(item)
        phantom.debug(f'Found container: {container}')
        success, message, run_id = phantom.playbook(playbook='myPhantom/[Quick Close] No Threat', container=container, name='Run playbook', callback=decision_1)
        if success:
            num_success += 1
            phantom.debug(f'Successfully ran playbook on container with run id: {run_id}')
        else:
            phantom.debug(f'Failed to run playbook.  Message from Phantom: {message}')
            num_failed += 1
            
    if num_failed > 0:
        message = f'One or more playbook executions failed to run. Success: {num_success} Failed: {num_failed}'
        status = 'failure'
    else:
        message = f'Successfully ran playbook on {num_success} containers.'
        status = 'success'
    outputs = {
        "status": status,
        "message": message
    }

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="run_playbook:status", value=json.dumps(run_playbook__status))
    phantom.save_run_data(key="run_playbook:message", value=json.dumps(run_playbook__message))

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