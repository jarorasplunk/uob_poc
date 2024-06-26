"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'noop_1' block
    noop_1(container=container)

    return

@phantom.playbook_block()
def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_1() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.label", "==", "events"],
            ["regex_split_3:custom_function_result.data.0.item", "==", "Not expected behaviour"]
        ],
        name="filter_1:condition_1",
        case_sensitive=False,
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        set_status_6(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.label", "==", "events"],
            ["regex_split_3:custom_function_result.data.0.item", "==", "Expected behaviour"]
        ],
        name="filter_1:condition_2",
        case_sensitive=False,
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        debug_5(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def regex_split_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_split_3() called")

    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:artifact:*.cef.userResponse","filtered-data:filter_2:condition_1:artifact:*.id"])

    parameters = []

    # build parameters list for 'regex_split_3' call
    for filtered_artifact_0_item_filter_2 in filtered_artifact_0_data_filter_2:
        parameters.append({
            "regex": "\\r\\n",
            "input_string": filtered_artifact_0_item_filter_2[0],
            "strip_whitespace": None,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_split", parameters=parameters, name="regex_split_3", callback=filter_1)

    return


@phantom.playbook_block()
def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_2() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.name", "==", "User Response Artifact"]
        ],
        name="filter_2:condition_1",
        scope="all",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        regex_split_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.name", "!=", "User Response Artifact"]
        ],
        name="filter_2:condition_2",
        scope="all",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        pass

    return


@phantom.playbook_block()
def debug_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_5() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef","artifact:*.id"])

    container_artifact_header_item_0 = [item[0] for item in container_artifact_data]

    parameters = []

    parameters.append({
        "input_1": container_artifact_header_item_0,
        "input_2": None,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_5", callback=promote_to_case_add_note_set_status_set_severity_7)

    return


@phantom.playbook_block()
def set_status_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_status_6() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    playbook_splunk_enterprise_security_close_investigation_1(container=container)

    return


@phantom.playbook_block()
def promote_to_case_add_note_set_status_set_severity_7(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("promote_to_case_add_note_set_status_set_severity_7() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.promote(container=container, template="Data Breach")
    phantom.add_note(container=container, content="This event has been updated to a case and the severity has been raised to critical.", note_format="markdown", note_type="general", title="Investigation status update")
    phantom.set_status(container=container, status="open")
    phantom.set_severity(container=container, severity="critical")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def playbook_splunk_enterprise_security_close_investigation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_splunk_enterprise_security_close_investigation_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/splunk_enterprise_security_close_investigation", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/splunk_enterprise_security_close_investigation", container=container)

    return


@phantom.playbook_block()
def loop_noop_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("loop_noop_1() called")

    loop_state = phantom.LoopState(state=loop_state_json)

    if loop_state.should_continue(container=container, results=results): # should_continue evaluates iteration/timeout/conditions
        loop_state.increment() # increments iteration count
        noop_1(container=container, loop_state_json=loop_state.to_json())
    else:
        debug_2(container=container)

    return


@phantom.playbook_block()
def noop_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("noop_1() called")

    parameters = [{}]

    if not loop_state_json:
        # Loop state is empty. We are creating a new one from the inputs
        loop_state_json = {
            # Looping configs
            "current_iteration": 1,
            "max_iterations": 3,
            "conditions": [
                ["artifact:*.name", "==", "User Response Artifact"]
            ],
            "max_ttl": 300,
            "delay_time": 60,
        }

    # Load state from the JSON passed to it
    loop_state = phantom.LoopState(state=loop_state_json)

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/noop", parameters=parameters, name="noop_1", callback=loop_noop_1, loop_state=loop_state.to_json())

    return


@phantom.playbook_block()
def debug_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_2() called")

    noop_1__result = phantom.collect2(container=container, datapath=["noop_1:custom_function_result.loop_state.current_iteration","noop_1:custom_function_result.loop_state.max_iterations","noop_1:custom_function_result.loop_state.exit_reason","noop_1:custom_function_result.loop_state.conditions","noop_1:custom_function_result.loop_state.delay_time"])

    noop_1_loop_state_current_iteration = [item[0] for item in noop_1__result]
    noop_1_loop_state_max_iterations = [item[1] for item in noop_1__result]
    noop_1_loop_state_exit_reason = [item[2] for item in noop_1__result]
    noop_1_loop_state_conditions = [item[3] for item in noop_1__result]
    noop_1_loop_state_delay_time = [item[4] for item in noop_1__result]

    parameters = []

    parameters.append({
        "input_1": noop_1_loop_state_current_iteration,
        "input_2": noop_1_loop_state_max_iterations,
        "input_3": noop_1_loop_state_exit_reason,
        "input_4": noop_1_loop_state_conditions,
        "input_5": noop_1_loop_state_delay_time,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_2", callback=decision_3)

    return


@phantom.playbook_block()
def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_3() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["noop_1:custom_function_result.loop_state.exit_reason", "==", "reached exit_condition"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        filter_2(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        conditions=[
            ["noop_1:custom_function_result.loop_state.exit_reason", "==", "reached max_iterations"]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        return

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