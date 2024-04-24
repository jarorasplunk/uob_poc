"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'vault_list_1' block
    vault_list_1(container=container)
    # call 'filter_email_artifact' block
    filter_email_artifact(container=container)

    return

@phantom.playbook_block()
def vault_list_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("vault_list_1() called")

    id_value = container.get("id", None)

    parameters = []

    parameters.append({
        "vault_id": None,
        "file_name": None,
        "container_id": id_value,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/vault_list", parameters=parameters, name="vault_list_1", callback=extract_email_1)

    return


@phantom.playbook_block()
def debug_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_3() called")

    vault_list_1__result = phantom.collect2(container=container, datapath=["vault_list_1:custom_function_result.data.container_name","vault_list_1:custom_function_result.data.file_name","vault_list_1:custom_function_result.data.vault_id","vault_list_1:custom_function_result.data.path"])

    vault_list_1_data_container_name = [item[0] for item in vault_list_1__result]
    vault_list_1_data_file_name = [item[1] for item in vault_list_1__result]
    vault_list_1_data_vault_id = [item[2] for item in vault_list_1__result]
    vault_list_1_data_path = [item[3] for item in vault_list_1__result]

    parameters = []

    parameters.append({
        "input_1": vault_list_1_data_container_name,
        "input_2": vault_list_1_data_file_name,
        "input_3": vault_list_1_data_vault_id,
        "input_4": vault_list_1_data_path,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_3")

    return


@phantom.playbook_block()
def filter_vault_for_emails(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_vault_for_emails() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="or",
        conditions=[
            [".msg", "in", "vault_list_1:custom_function_result.data.file_name"],
            [".eml", "in", "vault_list_1:custom_function_result.data.file_name"]
        ],
        name="filter_vault_for_emails:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        debug_4(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def debug_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_4() called")

    filtered_cf_result_0 = phantom.collect2(container=container, datapath=["filtered-data:filter_vault_for_emails:condition_1:vault_list_1:custom_function_result.data.vault_id","filtered-data:filter_vault_for_emails:condition_1:vault_list_1:custom_function_result.data.file_name"])

    filtered_cf_result_0_data_vault_id = [item[0] for item in filtered_cf_result_0]
    filtered_cf_result_0_data_file_name = [item[1] for item in filtered_cf_result_0]

    parameters = []

    parameters.append({
        "input_1": filtered_cf_result_0_data_vault_id,
        "input_2": filtered_cf_result_0_data_file_name,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_4")

    return


@phantom.playbook_block()
def filter_email_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_email_artifact() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Email Artifact"],
            ["artifact:*.description", "==", "Artifact added by MSG File Parser"]
        ],
        name="filter_email_artifact:condition_1",
        scope="all",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pass

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Email Artifact"],
            ["artifact:*.description", "==", "Artifact added by IMAP"]
        ],
        name="filter_email_artifact:condition_2",
        scope="all",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        regex_extract_email_11(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def regex_extract_email_11(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_extract_email_11() called")

    filtered_artifact_0_data_filter_email_artifact = phantom.collect2(container=container, datapath=["filtered-data:filter_email_artifact:condition_2:artifact:*.cef.emailHeaders.From","filtered-data:filter_email_artifact:condition_2:artifact:*.id"])

    parameters = []

    # build parameters list for 'regex_extract_email_11' call
    for filtered_artifact_0_item_filter_email_artifact in filtered_artifact_0_data_filter_email_artifact:
        parameters.append({
            "input_string": filtered_artifact_0_item_filter_email_artifact[0],
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_extract_email", parameters=parameters, name="regex_extract_email_11", callback=email_username)

    return


@phantom.playbook_block()
def extract_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("extract_email_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    id_value = container.get("id", None)
    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.vaultId","artifact:*.id"])

    parameters = []

    # build parameters list for 'extract_email_1' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "severity": "medium",
                "vault_id": container_artifact_item[0],
                "container_id": id_value,
                "artifact_name": "Email Artifact",
                "run_automation": True,
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("extract email", parameters=parameters, name="extract_email_1", assets=["splunk_poc"], callback=playbook_testing_usecase_1_automated_phising_v2_only_notes_subplaybook_1)

    return


@phantom.playbook_block()
def email_username(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("email_username() called")

    filtered_artifact_0_data_filter_email_artifact = phantom.collect2(container=container, datapath=["filtered-data:filter_email_artifact:condition_2:artifact:*.cef.emailHeaders.From","filtered-data:filter_email_artifact:condition_2:artifact:*.id"])

    parameters = []

    # build parameters list for 'email_username' call
    for filtered_artifact_0_item_filter_email_artifact in filtered_artifact_0_data_filter_email_artifact:
        parameters.append({
            "regex": "\\s\\<",
            "input_string": filtered_artifact_0_item_filter_email_artifact[0],
            "strip_whitespace": None,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_split", parameters=parameters, name="email_username")

    return


@phantom.playbook_block()
def playbook_testing_usecase_1_automated_phising_v2_only_notes_subplaybook_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_testing_usecase_1_automated_phising_v2_only_notes_subplaybook_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/testing_usecase_1_automated_phising_v2_only_notes_subplaybook", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/testing_usecase_1_automated_phising_v2_only_notes_subplaybook", container=container)

    filter_vault_for_emails(container=container)

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