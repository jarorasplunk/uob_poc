"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_3' block
    filter_3(container=container)

    return

@phantom.playbook_block()
def block_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("block_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_input_0_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_3:condition_1:playbook_input:ip"])

    parameters = []

    # build parameters list for 'block_ip_1' call
    for filtered_input_0_ip_item in filtered_input_0_ip:
        if filtered_input_0_ip_item[0] is not None:
            parameters.append({
                "ip": filtered_input_0_ip_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("block ip", parameters=parameters, name="block_ip_1", assets=["zscaler"], callback=mark_evidence_2)

    return


@phantom.playbook_block()
def block_url_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("block_url_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_input_0_url = phantom.collect2(container=container, datapath=["filtered-data:filter_3:condition_2:playbook_input:url"])

    parameters = []

    # build parameters list for 'block_url_1' call
    for filtered_input_0_url_item in filtered_input_0_url:
        if filtered_input_0_url_item[0] is not None:
            parameters.append({
                "url": filtered_input_0_url_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("block url", parameters=parameters, name="block_url_1", assets=["zscaler"], callback=mark_evidence_3)

    return


@phantom.playbook_block()
def indicator_tag_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_tag_1() called")

    list_merge_5_data = phantom.collect2(container=container, datapath=["list_merge_5:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'indicator_tag_1' call
    for list_merge_5_data_item in list_merge_5_data:
        parameters.append({
            "tags": "blocked",
            "indicator": list_merge_5_data_item[0],
            "overwrite": True,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/indicator_tag", parameters=parameters, name="indicator_tag_1")

    return


@phantom.playbook_block()
def join_filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_filter_2() called")

    if phantom.completed(custom_function_names=["mark_evidence_2", "mark_evidence_3"]):
        # call connected block "filter_2"
        filter_2(container=container, handle=handle)

    return


@phantom.playbook_block()
def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_2() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="or",
        conditions=[
            ["block_ip_1:action_result.status", "==", "success"],
            ["block_url_1:action_result.status", "==", "success"]
        ],
        name="filter_2:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        list_merge_5(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def list_merge_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("list_merge_5() called")

    filtered_result_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:block_ip_1:action_result.parameter.ip"])
    filtered_result_1_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:block_url_1:action_result.parameter.url"])

    filtered_result_0_parameter_ip = [item[0] for item in filtered_result_0_data_filter_2]
    filtered_result_1_parameter_url = [item[0] for item in filtered_result_1_data_filter_2]

    parameters = []

    parameters.append({
        "input_1": filtered_result_0_parameter_ip,
        "input_2": filtered_result_1_parameter_url,
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/list_merge", parameters=parameters, name="list_merge_5", callback=indicator_tag_1)

    return


@phantom.playbook_block()
def filter_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_3() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:ip", "!=", ""]
        ],
        name="filter_3:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        block_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:url", "!=", ""]
        ],
        name="filter_3:condition_2",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        block_url_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def mark_evidence_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("mark_evidence_2() called")

    id_value = container.get("id", None)

    parameters = []

    parameters.append({
        "container": id_value,
        "content_type": "action_run_id",
        "input_object": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []

    parameters.append({
        "container": id_value,
        "input_object": results,
        "content_type": "action_run_id",
    })

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/mark_evidence", parameters=parameters, name="mark_evidence_2", callback=join_filter_2)

    return


@phantom.playbook_block()
def mark_evidence_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("mark_evidence_3() called")

    id_value = container.get("id", None)

    parameters = []

    parameters.append({
        "container": id_value,
        "content_type": "action_run_id",
        "input_object": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []

    parameters.append({
        "container": id_value,
        "input_object": results,
        "content_type": "action_run_id",
    })

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/mark_evidence", parameters=parameters, name="mark_evidence_3", callback=join_filter_2)

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