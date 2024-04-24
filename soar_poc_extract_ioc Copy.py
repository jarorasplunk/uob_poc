"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_2' block
    filter_2(container=container)

    return

@phantom.playbook_block()
def extract_ioc_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_ioc_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:artifact:*.cef.vaultId","filtered-data:filter_2:condition_1:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_ioc_1' call
    for filtered_artifact_0_item_filter_2 in filtered_artifact_0_data_filter_2:
        parameters.append({
            "text": "",
            "label": "",
            "keep_raw": False,
            "severity": "medium",
            "vault_id": filtered_artifact_0_item_filter_2[0],
            "file_type": "txt",
            "container_id": id_value,
            "artifact_tags": "ip_ioc",
            "is_structured": False,
            "parse_domains": False,
            "run_automation": True,
            "remap_cef_fields": "Do not apply CEF -> CIM remapping, only apply custom remap",
            "custom_remap_json": "{}",
            "context": {'artifact_id': filtered_artifact_0_item_filter_2[1]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("extract ioc", parameters=parameters, name="extract_ioc_1", assets=["soar_poc_parser"], callback=debug_1)

    return


@phantom.playbook_block()
def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_2() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Vault Artifact"],
            ["artifact:*.cef.cs6Label", "==", "Vault ID"],
            ["artifact:*.cef.fileName", "==", "ip.txt"]
        ],
        name="filter_2:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        extract_ioc_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Vault Artifact"],
            ["artifact:*.cef.cs6Label", "==", "Vault ID"],
            ["artifact:*.cef.fileName", "==", "domain.txt"]
        ],
        name="filter_2:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        extract_ioc_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids and results for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Vault Artifact"],
            ["artifact:*.cef.cs6Label", "==", "Vault ID"],
            ["artifact:*.cef.fileName", "==", "MD5.txt"]
        ],
        name="filter_2:condition_3",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        extract_ioc_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    # collect filtered artifact ids and results for 'if' condition 4
    matched_artifacts_4, matched_results_4 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.description", "==", "Artifact added by Parser"]
        ],
        name="filter_2:condition_4",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_4 or matched_results_4:
        playbook_soar_poc_put_ioc_custom_list_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_4, filtered_results=matched_results_4)

    return


@phantom.playbook_block()
def extract_ioc_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_ioc_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_2:artifact:*.cef.vaultId","filtered-data:filter_2:condition_2:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_ioc_2' call
    for filtered_artifact_0_item_filter_2 in filtered_artifact_0_data_filter_2:
        parameters.append({
            "severity": "medium",
            "vault_id": filtered_artifact_0_item_filter_2[0],
            "file_type": "txt",
            "container_id": id_value,
            "artifact_tags": "domain_ioc",
            "parse_domains": True,
            "run_automation": True,
            "remap_cef_fields": "Do not apply CEF -> CIM remapping, only apply custom remap",
            "custom_remap_json": "{}",
            "context": {'artifact_id': filtered_artifact_0_item_filter_2[1]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("extract ioc", parameters=parameters, name="extract_ioc_2", assets=["soar_poc_parser"])

    return


@phantom.playbook_block()
def extract_ioc_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_ioc_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_3:artifact:*.cef.vaultId","filtered-data:filter_2:condition_3:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_ioc_3' call
    for filtered_artifact_0_item_filter_2 in filtered_artifact_0_data_filter_2:
        parameters.append({
            "severity": "medium",
            "vault_id": filtered_artifact_0_item_filter_2[0],
            "file_type": "txt",
            "container_id": id_value,
            "artifact_tags": "md5_ioc",
            "parse_domains": True,
            "run_automation": True,
            "remap_cef_fields": "Do not apply CEF -> CIM remapping, only apply custom remap",
            "custom_remap_json": "{}",
            "context": {'artifact_id': filtered_artifact_0_item_filter_2[1]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("extract ioc", parameters=parameters, name="extract_ioc_3", assets=["soar_poc_parser"])

    return


@phantom.playbook_block()
def playbook_soar_poc_put_ioc_custom_list_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_put_ioc_custom_list_2() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/soar_poc_put_IOC_custom_list", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/soar_poc_put_IOC_custom_list", container=container, name="playbook_soar_poc_put_ioc_custom_list_2", callback=playbook_soar_poc_put_ioc_custom_list_2_callback)

    return


@phantom.playbook_block()
def playbook_soar_poc_put_ioc_custom_list_2_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_put_ioc_custom_list_2_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    extract_ioc_1_result_data = phantom.collect2(container=container, datapath=["extract_ioc_1:action_result.data","extract_ioc_1:action_result.parameter.context.artifact_id"], action_results=results)

    extract_ioc_1_result_item_0 = [item[0] for item in extract_ioc_1_result_data]

    parameters = []

    parameters.append({
        "input_1": extract_ioc_1_result_item_0,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

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