"""
Work test events
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'open_check' block
    open_check(container=container)

    return

@phantom.playbook_block()
def open_check(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("open_check() called")

    status_value = container.get("status", None)

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            [status_value, "!=", "closed"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        close_ticket(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    already_closed_comment(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def close_ticket(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("close_ticket() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="Closing ticket")
    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def already_closed_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("already_closed_comment() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="Ticket already closed")

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return