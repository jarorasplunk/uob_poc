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

    splunk_enterprise_security_close_investigation(container=container)

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
def splunk_enterprise_security_close_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("splunk_enterprise_security_close_investigation() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "uob_poc/splunk_enterprise_security_close_investigation Copy", returns the playbook_run_id
    playbook_run_id = phantom.playbook("uob_poc/splunk_enterprise_security_close_investigation Copy", container=container)

    return


@phantom.playbook_block()
def loop_noop_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("loop_noop_1() called")

    loop_state = phantom.LoopState(state=loop_state_json)

    if loop_state.should_continue(container=container, results=results): # should_continue evaluates iteration/timeout/conditions
        loop_state.increment() # increments iteration count
        noop_1(container=container, loop_state_json=loop_state.to_json())

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
            "max_ttl": 900,
            "delay_time": 120,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_2")

    return


@phantom.playbook_block()
def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_3() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["indicator_collect_4:custom_function_result.loop_state.exit_reason", "==", "reached exit_condition"]
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
            ["indicator_collect_4:custom_function_result.loop_state.exit_reason", "==", "reached max_iterations"]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        send_htmlemail_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    subject_formatted_string = phantom.format(
        container=container,
        template="""[REMINDER]: Suspicious activity found on User computer: {0}\n""",
        parameters=[
            "artifact:*.cef.dest_nt_host"
        ])
    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Hi {0},</p>\n\n<p>This is a reminder to respond to the previous notification sent by SOAR regarding a anomalous process found on your computer: {1}</p>\n\n<p>Kindly respond to the previous email notification with Subject: </p>\n<p>Suspicious activity found on User computer: {0}</p>\n\n\n<p><strong>Action required </strong> Click on one of the links below to respond to this notification. This will create an email response and then you can click send without making any changes:</p>\n\n<p><a href=\"mailto:splunksoarpoc@gmail.com?subject={2}-User-{0}%20Response&body=Expected%20behaviour\">Expected behaviour</a></p>\n\n<p><a href=\"mailto:splunksoarpoc@gmail.com?subject={2}-User-{0}%20Response&body=Not%20expected%20behaviour\">Not expected behaviour</a></p>\n\n<p></p>\n""",
        parameters=[
            "artifact:*.cef.normalized_risk_object",
            "artifact:*.cef.dest_nt_host",
            "container:id"
        ])

    id_value = container.get("id", None)
    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.dest_nt_host","artifact:*.cef.normalized_risk_object","artifact:*.id"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for container_artifact_item in container_artifact_data:
        if html_body_formatted_string is not None:
            parameters.append({
                "to": "splunksoarpoc@gmail.com",
                "from": "splunksoarpoc@gmail.com",
                "subject": subject_formatted_string,
                "html_body": html_body_formatted_string,
                "context": {'artifact_id': container_artifact_item[2]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_1", assets=["soar_poc"])

    return


@phantom.playbook_block()
def indicator_collect_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_collect_4() called")

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_3 = phantom.collect2(container=container, datapath=["filtered-data:filter_3:condition_1:artifact:*.id","filtered-data:filter_3:condition_1:artifact:*.id"])

    filtered_artifact_0__id = [item[0] for item in filtered_artifact_0_data_filter_3]

    parameters = []

    parameters.append({
        "container": id_value,
        "artifact_ids_include": filtered_artifact_0__id,
        "indicator_tags_exclude": None,
        "indicator_tags_include": None,
        "indicator_types_exclude": None,
        "indicator_types_include": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/indicator_collect", parameters=parameters, name="indicator_collect_4", callback=debug_8)

    return


@phantom.playbook_block()
def debug_8(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_8() called")

    indicator_collect_4__result = phantom.collect2(container=container, datapath=["indicator_collect_4:custom_function_result.data.all_indicators"])

    indicator_collect_4_data_all_indicators = [item[0] for item in indicator_collect_4__result]

    parameters = []

    parameters.append({
        "input_1": indicator_collect_4_data_all_indicators,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_8", callback=decision_3)

    return


@phantom.playbook_block()
def filter_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_3() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.name", "==", "User Response Artifact"]
        ],
        name="filter_3:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        indicator_collect_4(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

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