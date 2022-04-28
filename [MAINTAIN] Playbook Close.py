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
        get_close_playbook(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    custom_function_failed_comment(action=action, success=success, container=container, results=results, handle=handle)

    return


def get_close_playbook(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_close_playbook() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "location": "playbook?_filter_name='[Quick Close] No Threat'",
        "verify_certificate": False,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="get_close_playbook", assets=["phantom_http"], callback=format_list_of_items_and_playbook_ids)

    return


def format_list_of_items_and_playbook_ids(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_list_of_items_and_playbook_ids() called")

    get_custom_list_copy_1__result = phantom.collect2(container=container, datapath=["get_custom_list_copy_1:custom_function_result.data.list_of_items"])
    get_close_playbook_result_data = phantom.collect2(container=container, datapath=["get_close_playbook:action_result.data.*.parsed_response_body.data.*.id"], action_results=results)

    get_custom_list_copy_1_data_list_of_items = [item[0] for item in get_custom_list_copy_1__result]
    get_close_playbook_result_item_0 = [item[0] for item in get_close_playbook_result_data]

    format_list_of_items_and_playbook_ids__list_of_items = None
    format_list_of_items_and_playbook_ids__list_of_playbook_id = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="format_list_of_items_and_playbook_ids:list_of_items", value=json.dumps(format_list_of_items_and_playbook_ids__list_of_items))
    phantom.save_run_data(key="format_list_of_items_and_playbook_ids:list_of_playbook_id", value=json.dumps(format_list_of_items_and_playbook_ids__list_of_playbook_id))

    format_json_for_container(container=container)

    return


def format_json_for_container(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_json_for_container() called")

    template = """%%\n{{\n    \"container_id\": {0},\n    \"playbook_id\": {1},\n    \"scope\": \"all\",\n    \"run\": true\n}}\n%%\n"""

    # parameter list for template variable replacement
    parameters = [
        "format_list_of_items_and_playbook_ids:custom_function:list_of_items",
        "format_list_of_items_and_playbook_ids:custom_function:list_of_playbook_id"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_json_for_container")

    post_data_1(container=container)

    return


def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    formatted_data_value = container.get("formatted_data", None)

    parameters = []

    if formatted_data_value is not None:
        parameters.append({
            "body": formatted_data_value,
            "location": "/playbook_run",
            "verify_certificate": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_1", assets=["phantom_http"])

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