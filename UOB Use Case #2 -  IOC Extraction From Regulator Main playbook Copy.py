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
def extract_ip_ioc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_ip_ioc() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_1:artifact:*.cef.vaultId","filtered-data:filter_2:condition_1:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_ip_ioc' call
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

    phantom.act("extract ioc", parameters=parameters, name="extract_ip_ioc", assets=["soar_poc_parser"], callback=join_playbook_soar_poc_put_ioc_custom_list_1)

    return


@phantom.playbook_block()
def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_2() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.fileName", "==", "ip.txt"]
        ],
        name="filter_2:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        extract_ip_ioc(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.fileName", "==", "domain.txt"]
        ],
        name="filter_2:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        extract_domain_ioc(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids and results for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.fileName", "==", "MD5.txt"]
        ],
        name="filter_2:condition_3",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        extract_hash_ioc(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    # collect filtered artifact ids and results for 'if' condition 4
    matched_artifacts_4, matched_results_4 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.description", "!=", "Artifact added by Parser"]
        ],
        name="filter_2:condition_4",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_4 or matched_results_4:
        pass

    return


@phantom.playbook_block()
def extract_domain_ioc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_domain_ioc() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_2:artifact:*.cef.vaultId","filtered-data:filter_2:condition_2:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_domain_ioc' call
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

    phantom.act("extract ioc", parameters=parameters, name="extract_domain_ioc", assets=["soar_poc_parser"], callback=join_playbook_soar_poc_put_ioc_custom_list_1)

    return


@phantom.playbook_block()
def extract_hash_ioc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_hash_ioc() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    filtered_artifact_0_data_filter_2 = phantom.collect2(container=container, datapath=["filtered-data:filter_2:condition_3:artifact:*.cef.vaultId","filtered-data:filter_2:condition_3:artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_hash_ioc' call
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

    phantom.act("extract ioc", parameters=parameters, name="extract_hash_ioc", assets=["soar_poc_parser"], callback=join_playbook_soar_poc_put_ioc_custom_list_1)

    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_ip_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/soar_poc_execute_search_IP", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/soar_poc_execute_search_IP", container=container, name="playbook_soar_poc_execute_search_ip_1", callback=playbook_soar_poc_execute_search_ip_1_callback)

    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_ip_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_ip_1_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_domain_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/soar_poc_execute_search_domain", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/soar_poc_execute_search_domain", container=container, name="playbook_soar_poc_execute_search_domain_1", callback=playbook_soar_poc_execute_search_domain_1_callback)

    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_domain_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_domain_1_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_md5_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_md5_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/soar_poc_execute_search_md5", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/soar_poc_execute_search_md5", container=container, name="playbook_soar_poc_execute_search_md5_1", callback=playbook_soar_poc_execute_search_md5_1_callback)

    return


@phantom.playbook_block()
def playbook_soar_poc_execute_search_md5_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_execute_search_md5_1_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


@phantom.playbook_block()
def join_playbook_soar_poc_put_ioc_custom_list_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_playbook_soar_poc_put_ioc_custom_list_1() called")

    if phantom.completed(action_names=["extract_ip_ioc", "extract_domain_ioc", "extract_hash_ioc"]):
        # call connected block "playbook_soar_poc_put_ioc_custom_list_1"
        playbook_soar_poc_put_ioc_custom_list_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def playbook_soar_poc_put_ioc_custom_list_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_soar_poc_put_ioc_custom_list_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/soar_poc_put_IOC_custom_list", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/soar_poc_put_IOC_custom_list", container=container)

    playbook_soar_poc_execute_search_ip_1(container=container)
    playbook_soar_poc_execute_search_domain_1(container=container)
    playbook_soar_poc_execute_search_md5_1(container=container)

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