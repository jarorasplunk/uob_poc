"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_email_artifact' block
    filter_email_artifact(container=container)
    # call 'extract_email_1' block
    extract_email_1(container=container)

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

    phantom.custom_function(custom_function="community/vault_list", parameters=parameters, name="vault_list_1", callback=filter_vault_for_emails)

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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_4", callback=playbook_saa_dynamic_email_analysis_1)

    return


@phantom.playbook_block()
def playbook_saa_dynamic_email_analysis_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_saa_dynamic_email_analysis_1() called")

    filtered_cf_result_0 = phantom.collect2(container=container, datapath=["filtered-data:filter_vault_for_emails:condition_1:vault_list_1:custom_function_result.data.vault_id"])

    filtered_cf_result_0_data_vault_id = [item[0] for item in filtered_cf_result_0]

    inputs = {
        "vault_id": filtered_cf_result_0_data_vault_id,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/SAA_Dynamic_Email_Analysis", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/SAA_Dynamic_Email_Analysis", container=container, name="playbook_saa_dynamic_email_analysis_1", callback=add_note_whois_info, inputs=inputs)

    return


@phantom.playbook_block()
def add_note_observable_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_observable_details() called")

    playbook_saa_dynamic_email_analysis_1_output_observable = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:observable"])

    playbook_saa_dynamic_email_analysis_1_output_observable_values = [item[0] for item in playbook_saa_dynamic_email_analysis_1_output_observable]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    observable_values = str()
    for item in playbook_saa_dynamic_email_analysis_1_output_observable_values:
        if item is not None:
            observable_values = item
            
    playbook_saa_dynamic_email_analysis_1_output_observable_values = observable_values
    
    for item in playbook_saa_dynamic_email_analysis_1_output_observable_values:
        phantom.debug(item)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=playbook_saa_dynamic_email_analysis_1_output_observable_values, note_format="markdown", note_type="general", title="Obervable details")

    add_note_saa_report(container=container)

    return


@phantom.playbook_block()
def add_note_saa_report(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_saa_report() called")

    playbook_saa_dynamic_email_analysis_1_output_report = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:report"])

    playbook_saa_dynamic_email_analysis_1_output_report_values = [item[0] for item in playbook_saa_dynamic_email_analysis_1_output_report]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    report_data = str()
    for item in playbook_saa_dynamic_email_analysis_1_output_report_values:
        if item is not None:
            report_data = item
            
    playbook_saa_dynamic_email_analysis_1_output_report_values = report_data

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=playbook_saa_dynamic_email_analysis_1_output_report_values, note_format="markdown", note_type="general", title="Email Analysis Report")

    debug_2(container=container)

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
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        regex_extract_email_11(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def add_note_whois_info(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_whois_info() called")

    playbook_saa_dynamic_email_analysis_1_output_whois_note = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:whois_note"])

    playbook_saa_dynamic_email_analysis_1_output_whois_note_values = [item[0] for item in playbook_saa_dynamic_email_analysis_1_output_whois_note]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    playbook_saa_dynamic_email_analysis_1_output_whois_note_values = playbook_saa_dynamic_email_analysis_1_output_whois_note_values[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=playbook_saa_dynamic_email_analysis_1_output_whois_note_values, note_format="markdown", note_type="general", title="Suspected domain's whois information:")

    add_note_observable_details(container=container)

    return


@phantom.playbook_block()
def check_phish(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("check_phish() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="or",
        conditions=[
            ["playbook_saa_dynamic_email_analysis_1:playbook_output:verdict", "==", "phish"],
            ["playbook_saa_dynamic_email_analysis_1:playbook_output:verdict", "==", "malware"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        join_send_htmlemail_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        conditions=[
            ["playbook_saa_dynamic_email_analysis_1:playbook_output:verdict", "==", "spam"]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        join_send_htmlemail_3(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 3
    join_send_htmlemail_2(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def join_send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_send_htmlemail_1() called")

    if phantom.completed(custom_function_names=["debug_2", "email_username"]):
        # call connected block "send_htmlemail_1"
        send_htmlemail_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Dear {1},</p>\n\n<p>The for reporting and forwarding the email.</p>\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, this email has been categorised as &quot;Malicious&quot;</p>\n\n<p>Please see below some more details about the analysis of reported email:</p>\n\n<p>{0}</p>\n\n<p>Please delete any copies of this email from your mailbox and DO NOT attempt to click on any links or download any files from the malicious email.</p>\n\n<p>If you have any further concerns or if you would like to know more on the investigation of this phishing attempt, reach out to your friendly Splunk Security team at UoB, otherwise no further actions are required from your end.</p>\n\n<p> Thanks</p>\n\n""",
        parameters=[
            "playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only",
            "email_username:custom_function_result.data.0.item"
        ])

    regex_extract_email_11_data = phantom.collect2(container=container, datapath=["regex_extract_email_11:custom_function_result.data.*.email_address"])
    playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only"])
    email_username__result = phantom.collect2(container=container, datapath=["email_username:custom_function_result.data.0.item"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for regex_extract_email_11_data_item in regex_extract_email_11_data:
        for playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only_item in playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only:
            for email_username__result_item in email_username__result:
                if regex_extract_email_11_data_item[0] is not None and html_body_formatted_string is not None:
                    parameters.append({
                        "to": regex_extract_email_11_data_item[0],
                        "from": "splunkphisingpoc@gmail.com",
                        "subject": "Thanks for reporting the phishing email!",
                        "html_body": html_body_formatted_string,
                    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_1", assets=["soar_poc_phishing_smtp"], callback=set_status_promote_to_case_set_severity_add_note_10)

    return


@phantom.playbook_block()
def set_status_promote_to_case_set_severity_add_note_10(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_status_promote_to_case_set_severity_add_note_10() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.promote(container=container, template="Suspicious Email")
    phantom.add_note(container=container, content="This event has been updated to a case and the severity has been raised to critical.", note_format="markdown", note_type="general", title="Investigation status update")
    phantom.set_status(container=container, status="open")
    phantom.set_severity(container=container, severity="critical")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def join_send_htmlemail_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_send_htmlemail_2() called")

    if phantom.completed(custom_function_names=["debug_2", "email_username"]):
        # call connected block "send_htmlemail_2"
        send_htmlemail_2(container=container, handle=handle)

    return


@phantom.playbook_block()
def send_htmlemail_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Dear {0},</p>\n\n<p>The for reporting and forwarding the email.</p>\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, this email has been categorised as &quot;Safe&quot;.</p>\n\n<p>If you have any further concerns or if you would like to know more on the investigation of this phishing attempt and analysis, reach out to your friendly Splunk Security team at UoB, otherwise no further actions are required from your end.</p>\n\n<p> Thanks</p>\n\n""",
        parameters=[
            "email_username:custom_function_result.data.0.item"
        ])

    regex_extract_email_11_data = phantom.collect2(container=container, datapath=["regex_extract_email_11:custom_function_result.data.*.email_address"])
    email_username__result = phantom.collect2(container=container, datapath=["email_username:custom_function_result.data.0.item"])

    parameters = []

    # build parameters list for 'send_htmlemail_2' call
    for regex_extract_email_11_data_item in regex_extract_email_11_data:
        for email_username__result_item in email_username__result:
            if regex_extract_email_11_data_item[0] is not None and html_body_formatted_string is not None:
                parameters.append({
                    "to": regex_extract_email_11_data_item[0],
                    "from": "splunkphisingpoc@gmail.com",
                    "subject": "Thanks for reporting the phishing email!",
                    "html_body": html_body_formatted_string,
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_2", assets=["soar_poc_phishing_smtp"])

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

    phantom.custom_function(custom_function="community/regex_split", parameters=parameters, name="email_username", callback=email_username_callback)

    return


@phantom.playbook_block()
def email_username_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("email_username_callback() called")

    
    join_send_htmlemail_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    join_send_htmlemail_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    join_send_htmlemail_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def join_send_htmlemail_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_send_htmlemail_3() called")

    if phantom.completed(custom_function_names=["debug_2", "email_username"]):
        # call connected block "send_htmlemail_3"
        send_htmlemail_3(container=container, handle=handle)

    return


@phantom.playbook_block()
def send_htmlemail_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Dear {1},</p>\n\n<p>The for reporting and forwarding the email.</p>\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, this email has been categorised as &quot;Unknown&quot;</p>\n\n<p>Please see below some more details about the analysis of reported email:</p>\n\n<p>{0}</p>\n\n<p>Please delete any copies of this email from your mailbox and DO NOT attempt to click on any links or download any files from the malicious email.</p>\n\n<p>If you have any further concerns or if you would like to know more on the investigation of this phishing attempt, reach out to your friendly Splunk Security team at UoB, otherwise no further actions are required from your end.</p>\n\n<p> Thanks</p>\n""",
        parameters=[
            "playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only",
            "email_username:custom_function_result.data.0.item"
        ])

    regex_extract_email_11_data = phantom.collect2(container=container, datapath=["regex_extract_email_11:custom_function_result.data.*.email_address"])
    playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only"])
    email_username__result = phantom.collect2(container=container, datapath=["email_username:custom_function_result.data.0.item"])

    parameters = []

    # build parameters list for 'send_htmlemail_3' call
    for regex_extract_email_11_data_item in regex_extract_email_11_data:
        for playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only_item in playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only:
            for email_username__result_item in email_username__result:
                if regex_extract_email_11_data_item[0] is not None and html_body_formatted_string is not None:
                    parameters.append({
                        "to": regex_extract_email_11_data_item[0],
                        "from": "splunkphisingpoc@gmail.com",
                        "subject": "Thanks for reporting the phishing email!",
                        "html_body": html_body_formatted_string,
                    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_3", assets=["soar_poc_phishing_smtp"], callback=send_htmlemail_4)

    return


@phantom.playbook_block()
def send_htmlemail_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_4() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    headers_formatted_string = phantom.format(
        container=container,
        template="""ContainerID - {0} # Phishing Email Result Unknown""",
        parameters=[
            "container:id"
        ])
    html_body_formatted_string = phantom.format(
        container=container,
        template="""Hi Analyst,\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, a reported email has been categorised as &quot;Unknown&quot;</p>\n\n<p>Please see below some more details about the analysis of reported email:</p>\n\n<p>{0}</p>\n\n<p>Please review container ID &quot;{1}{1}&quot;</p>""",
        parameters=[
            "playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only",
            "container:id"
        ])

    id_value = container.get("id", None)
    playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only"])

    parameters = []

    # build parameters list for 'send_htmlemail_4' call
    for playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only_item in playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only:
        if html_body_formatted_string is not None:
            parameters.append({
                "to": "fwinata@splunk.com",
                "from": "splunkphisingpoc@gmail.com",
                "headers": headers_formatted_string,
                "html_body": html_body_formatted_string,
                "text_body": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_4", assets=["soar_poc_phishing_smtp"])

    return


@phantom.playbook_block()
def debug_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_2() called")

    playbook_saa_dynamic_email_analysis_1_output_verdict = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:verdict"])

    playbook_saa_dynamic_email_analysis_1_output_verdict_values = [item[0] for item in playbook_saa_dynamic_email_analysis_1_output_verdict]

    parameters = []

    parameters.append({
        "input_1": playbook_saa_dynamic_email_analysis_1_output_verdict_values,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_2", callback=check_phish)

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

    vault_list_1(container=container)

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