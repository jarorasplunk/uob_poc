"""
Grabs the cmdline value, attempt a base64 decode, and search for devices communicating to any discovered IPs. Adds a task note for the analyst with the results.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'encoded_powershell_investigation' block
    encoded_powershell_investigation(container=container)

    return

@phantom.playbook_block()
def encoded_powershell_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("encoded_powershell_investigation() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.cmdline"], scope="all")

    container_artifact_cef_item_0 = [item[0] for item in container_artifact_data]

    inputs = {
        "powershell_process": container_artifact_cef_item_0,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "uob_poc/encoded_powershell_investigation Copy", returns the playbook_run_id
    playbook_run_id = phantom.playbook("uob_poc/encoded_powershell_investigation Copy", container=container, name="encoded_powershell_investigation", callback=filter_1, inputs=inputs)

    return


@phantom.playbook_block()
def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_1() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["encoded_powershell_investigation:playbook_output:note_content", "!=", ""]
        ],
        name="filter_1:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        add_note_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def add_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_1() called")

    encoded_powershell_investigation_output_note_content = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_content"])
    encoded_powershell_investigation_output_note_title = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_title"])

    encoded_powershell_investigation_output_note_content_values = [item[0] for item in encoded_powershell_investigation_output_note_content]
    encoded_powershell_investigation_output_note_title_values = [item[0] for item in encoded_powershell_investigation_output_note_title]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    encoded_powershell_investigation_output_note_title_values = encoded_powershell_investigation_output_note_title_values[0]
    encoded_powershell_investigation_output_note_content_values = encoded_powershell_investigation_output_note_content_values[0]
    
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=encoded_powershell_investigation_output_note_content_values, note_format="html", note_type="general", title=encoded_powershell_investigation_output_note_title_values)

    update_event_1(container=container)

    return


@phantom.playbook_block()
def update_event_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("update_event_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    encoded_powershell_investigation_output_note_content = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_content"])
    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.event_id","artifact:*.id"])

    parameters = []

    # build parameters list for 'update_event_1' call
    for encoded_powershell_investigation_output_note_content_item in encoded_powershell_investigation_output_note_content:
        for container_artifact_item in container_artifact_data:
            if container_artifact_item[0] is not None:
                parameters.append({
                    "comment": encoded_powershell_investigation_output_note_content_item[0],
                    "event_ids": container_artifact_item[0],
                    "context": {'artifact_id': container_artifact_item[1]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update event", parameters=parameters, name="update_event_1", assets=["splunk"])

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    encoded_powershell_investigation_output_note_title = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_title"])
    encoded_powershell_investigation_output_note_content = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_content"])
    encoded_powershell_investigation_output_note_decoded_proc_info_first = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_decoded_proc_info_first"])
    encoded_powershell_investigation_output_note_decoded_proc_info_second = phantom.collect2(container=container, datapath=["encoded_powershell_investigation:playbook_output:note_decoded_proc_info_second"])

    encoded_powershell_investigation_output_note_title_values = [item[0] for item in encoded_powershell_investigation_output_note_title]
    encoded_powershell_investigation_output_note_content_values = [item[0] for item in encoded_powershell_investigation_output_note_content]
    encoded_powershell_investigation_output_note_decoded_proc_info_first_values = [item[0] for item in encoded_powershell_investigation_output_note_decoded_proc_info_first]
    encoded_powershell_investigation_output_note_decoded_proc_info_second_values = [item[0] for item in encoded_powershell_investigation_output_note_decoded_proc_info_second]

    output = {
        "note_title": encoded_powershell_investigation_output_note_title_values,
        "note_content": encoded_powershell_investigation_output_note_content_values,
        "note_content_process_info_first": encoded_powershell_investigation_output_note_decoded_proc_info_first_values,
        "note_content_process_info_second": encoded_powershell_investigation_output_note_decoded_proc_info_second_values,
    }

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

    phantom.save_playbook_output_data(output=output)

    return