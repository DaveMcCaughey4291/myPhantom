"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_playbook_owner' block
    get_playbook_owner(container=container)

    return

@phantom.playbook_block()
def get_playbook_owner(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_playbook_owner() called")

    get_playbook_owner__user_id = None
    get_playbook_owner__username = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    pb_info = phantom.get_playbook_info()
    phantom.debug(f"Found playbook info: {str(pb_info)}")
    
    user_id = int(pb_info[0]['effective_user_id'])
    phantom.debug(f"Found user ID: {user_id}")
    
    # Build owner details URL
    url = phantom.build_phantom_rest_url('ph_user', user_id)
    phantom.debug(f"Making HTTP GET request to: {url}")
    response = phantom.requests.get(url, verify=False)
    phantom.debug(f"Response from Phantom: {response}")
    owner_info = response.json()
    
    username = owner_info['username']
    phantom.debug(f"Found username: {username}")
    
    get_playbook_owner__user_id = user_id
    get_playbook_owner__username = username

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_playbook_owner:user_id", value=json.dumps(get_playbook_owner__user_id))
    phantom.save_run_data(key="get_playbook_owner:username", value=json.dumps(get_playbook_owner__username))

    prompt_2(container=container)

    return


@phantom.playbook_block()
def prompt_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("prompt_2() called")

    # set user and message variables for phantom.prompt call

    user = json.loads(phantom.get_run_data(key="get_playbook_owner:username"))
    message = """Hello {0}."""

    # parameter list for template variable replacement
    parameters = [
        "get_playbook_owner:custom_function:username"
    ]

    # responses
    response_types = [
        {
            "prompt": "Something",
            "options": {
                "type": "message",
            },
        }
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_2", parameters=parameters, response_types=response_types, callback=format_note)

    return

@phantom.playbook_block()
def format_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_note() called")

    template = """User {0} said {1}\n"""

    # parameter list for template variable replacement
    parameters = [
        "get_playbook_owner:custom_function:username",
        "prompt_2:action_result.summary.responses.0"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_note")

    add_note_1(container=container)

    return


@phantom.playbook_block()
def add_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_note_1() called")

    format_note = phantom.get_format_data(name="format_note")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=format_note, note_format="markdown", note_type="general")

    return


@phantom.playbook_block()
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