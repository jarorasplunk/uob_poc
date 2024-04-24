"""
A playbook that closes out an investigation in both Splunk Enterprise Security and Splunk SOAR.
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
def close_notable(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("close_notable() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    comment_formatted_string = phantom.format(
        container=container,
        template="""Splunk SOAR event {0} closed at {1} by {2}""",
        parameters=[
            "container:id",
            "container:close_time",
            "get_playbook_owner:custom_function:value"
        ])

    ################################################################################
    # Close the Notable in Splunk Enterprise Security with a comment.
    ################################################################################

    id_value = container.get("id", None)
    close_time_value = container.get("close_time", None)
    filtered_artifact_0_data_event_id_filter = phantom.collect2(container=container, datapath=["filtered-data:event_id_filter:condition_1:artifact:*.cef.event_id","filtered-data:event_id_filter:condition_1:artifact:*.id"])
    get_playbook_owner__value = json.loads(_ if (_ := phantom.get_run_data(key="get_playbook_owner:value")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'close_notable' call
    for filtered_artifact_0_item_event_id_filter in filtered_artifact_0_data_event_id_filter:
        if filtered_artifact_0_item_event_id_filter[0] is not None:
            parameters.append({
                "status": "closed",
                "comment": comment_formatted_string,
                "event_ids": filtered_artifact_0_item_event_id_filter[0],
                "context": {'artifact_id': filtered_artifact_0_item_event_id_filter[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update event", parameters=parameters, name="close_notable", assets=["splunk"])

    return


@phantom.playbook_block()
def get_playbook_owner(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_playbook_owner() called")

    ################################################################################
    # Get effective (execution) user of playbook
    ################################################################################

    get_playbook_owner__value = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    user_id = phantom.get_effective_user()
    url = phantom.build_phantom_rest_url('ph_user', user_id)
    response = phantom.requests.get(url, verify=False).json()
    get_playbook_owner__value = response['username']

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_playbook_owner:value", value=json.dumps(get_playbook_owner__value))

    close_event(container=container)

    return


@phantom.playbook_block()
def close_event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("close_event() called")

    ################################################################################
    # Close the container in Splunk SOAR
    ################################################################################

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    event_id_filter(container=container)

    return


@phantom.playbook_block()
def event_id_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("event_id_filter() called")

    ################################################################################
    # Get the artifacts with the event id
    ################################################################################

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.event_id", "!=", ""]
        ],
        name="event_id_filter:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        close_notable(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

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