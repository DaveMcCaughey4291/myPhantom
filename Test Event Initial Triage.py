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
        conditions_dps=[
            ["container:status", "!=", "closed"]
        ],
        name="open_check:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        ip_check(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    already_closed_comment(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def join_close_ticket(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_close_ticket() called")

    if phantom.completed(action_names=["lookup_whois"]):
        # call connected block "close_ticket"
        close_ticket(container=container, handle=handle)

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
def ip_check(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ip_check() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["artifact:*.cef.destinationAddress", "!=", ""]
        ],
        conditions_dps=[
            ["artifact:*.cef.destinationAddress", "!=", ""]
        ],
        name="ip_check:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        ip_filter(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    join_close_ticket(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def ip_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ip_filter() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.destinationAddress", "!=", ""]
        ],
        conditions_dps=[
            ["artifact:*.cef.destinationAddress", "!=", ""]
        ],
        name="ip_filter:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        lookup_whois(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def lookup_whois(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("lookup_whois() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_artifact_0_data_ip_filter = phantom.collect2(container=container, datapath=["filtered-data:ip_filter:condition_1:artifact:*.cef.destinationAddress","filtered-data:ip_filter:condition_1:artifact:*.id"])

    parameters = []

    # build parameters list for 'lookup_whois' call
    for filtered_artifact_0_item_ip_filter in filtered_artifact_0_data_ip_filter:
        if filtered_artifact_0_item_ip_filter[0] is not None:
            parameters.append({
                "ip": filtered_artifact_0_item_ip_filter[0],
                "context": {'artifact_id': filtered_artifact_0_item_ip_filter[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("whois ip", parameters=parameters, name="lookup_whois", assets=["splunk_whois_rdap"], callback=join_close_ticket)

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