"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'decision_1' block
    decision_1(container=container)

    return

@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Email Artifact"],
            ["behaviour", "in", "artifact:*.cef.bodyPart1"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        extract_container_id(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def extract_container_id(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_container_id() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.emailHeaders.Subject","artifact:*.cef.bodyPart1"])

    container_artifact_cef_item_0 = [item[0] for item in container_artifact_data]
    container_artifact_cef_item_1 = [item[1] for item in container_artifact_data]

    extract_container_id__container_id = None
    extract_container_id__user_response = None
    extract_container_id__artifact_json = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    container = container_artifact_cef_item_0[0].split('-')
    phantom.debug(container[0])
    
    extract_container_id__container_id = container[0]
    
    extract_container_id__user_response = container_artifact_cef_item_1[0]
    
    extract_container_id__artifact_json = {
        "userResponse": extract_container_id__user_response
    }
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="extract_container_id:container_id", value=json.dumps(extract_container_id__container_id))
    phantom.save_run_data(key="extract_container_id:user_response", value=json.dumps(extract_container_id__user_response))
    phantom.save_run_data(key="extract_container_id:artifact_json", value=json.dumps(extract_container_id__artifact_json))

    artifact_create(container=container)

    return


@phantom.playbook_block()
def artifact_create(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("artifact_create() called")

    extract_container_id__user_response = json.loads(_ if (_ := phantom.get_run_data(key="extract_container_id:user_response")) != "" else "null")  # pylint: disable=used-before-assignment
    extract_container_id__container_id = json.loads(_ if (_ := phantom.get_run_data(key="extract_container_id:container_id")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    parameters.append({
        "name": "User Response Artifact",
        "tags": "user_response",
        "label": "process_analysed",
        "severity": None,
        "cef_field": "userResponse",
        "cef_value": extract_container_id__user_response,
        "container": extract_container_id__container_id,
        "input_json": None,
        "cef_data_type": None,
        "run_automation": False,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    phantom.debug(type(extract_container_id__container_id))
    phantom.debug(extract_container_id__container_id)
    
    parameters = []

    parameters.append({
        "container": int(extract_container_id__container_id),
        "name": "User Response Artifact",
        "label": None,
        "severity": None,
        "cef_field": "userResponse",
        "cef_value": extract_container_id__user_response,
        "cef_data_type": None,
        "tags": None,
        "run_automation": None,
        "input_json": None,
    })
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/artifact_create", parameters=parameters, name="artifact_create")

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