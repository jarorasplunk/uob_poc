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

    phantom.custom_function(custom_function="community/vault_list", parameters=parameters, name="vault_list_1", callback=vault_list_1_callback)

    return


@phantom.playbook_block()
def vault_list_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("vault_list_1_callback() called")

    
    filter_email_artifact(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    filter_vault_for_emails(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


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

    check_phish(container=container)

    return


@phantom.playbook_block()
def filter_email_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_email_artifact() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.bodyText", "!=", ""]
        ],
        name="filter_email_artifact:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        format_header_note_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def format_header_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_header_note_1() called")

    filtered_artifact_0_data_filter_email_artifact = phantom.collect2(container=container, datapath=["filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.To","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Date","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.From","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Subject","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.References","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.In-Reply-To","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.ContentType","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.X-MS-Has-Attach"])

    filtered_artifact_0__cef_emailheaders_to = [item[0] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_date = [item[1] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_from = [item[2] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_subject = [item[3] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_references = [item[4] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_in_reply_to = [item[5] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_contenttype = [item[6] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_x_ms_has_attach = [item[7] for item in filtered_artifact_0_data_filter_email_artifact]

    format_header_note_1__header_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import re
    
    phantom.debug(filtered_artifact_0__cef_emailheaders_to[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_date[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_from[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_subject[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_references[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_in_reply_to[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_contenttype[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_x_ms_has_attach[0])
    sender = filtered_artifact_0__cef_emailheaders_from[0]
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', sender)
    sender = match[0]
    sender_domain = sender[sender.index('@') + 1 : ]
    replyto = filtered_artifact_0__cef_emailheaders_in_reply_to[0]
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', replyto)
    replyto = match[0]
    recipient = filtered_artifact_0__cef_emailheaders_to[0]
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', recipient)
    recipient = match[0]
    date = filtered_artifact_0__cef_emailheaders_date[0]
    routing_info = filtered_artifact_0__cef_emailheaders_references[0]
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', routing_info)
    routing_info = match
    contenttype = filtered_artifact_0__cef_emailheaders_contenttype[0]
    hasattachment = filtered_artifact_0__cef_emailheaders_x_ms_has_attach[0]
    
    note = (
        "| Sender email | Sender domain | Reply To | Recipient | Date | Routing information | Content type | Hast attachment? |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    )
    
    note += "|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(sender, sender_domain, replyto, recipient, date, routing_info, contenttype, hasattachment)
    
    format_header_note_1__header_note = note
    
    
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="format_header_note_1:header_note", value=json.dumps(format_header_note_1__header_note))

    add_note_8(container=container)

    return


@phantom.playbook_block()
def add_note_8(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_8() called")

    format_header_note_1__header_note = json.loads(_ if (_ := phantom.get_run_data(key="format_header_note_1:header_note")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=format_header_note_1__header_note, note_format="markdown", note_type="general", title="Email header details")

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
        conditions=[
            ["playbook_saa_dynamic_email_analysis_1:playbook_output:verdict", "==", "phish"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        send_htmlemail_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    send_htmlemail_2(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Dear User,</p>\n\n<p>The for reporting and forwarding the email.</p>\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, this email has been categorised as &quot;Malicious&quot;</p>\n\n<p>Please see below some more details about the analysis of reported email:</p>\n\n<p>{0}</p>\n\n<p>Please delete any copies of this email from your mailbox and DO NOT attempt to click on any links or download any files from the malicious email.</p>\n\n<p>If you have any further concerns or if you would like to know more on the investigation of this phishing attempt, reach out to your friendly Splunk Security team at UoB, otherwise no further actions are required from your end.</p>\n\n<p> Thanks</p>\n""",
        parameters=[
            "playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only"
        ])

    playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only = phantom.collect2(container=container, datapath=["playbook_saa_dynamic_email_analysis_1:playbook_output:analysis_summary_only"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only_item in playbook_saa_dynamic_email_analysis_1_output_analysis_summary_only:
        if html_body_formatted_string is not None:
            parameters.append({
                "to": "jarora@splunk.com",
                "from": "splunksoarpoc@gmail.com",
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

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_1", assets=["soar_poc_smtp"], callback=set_status_promote_to_case_set_severity_add_note_10)

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
def send_htmlemail_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Hi {0},</p>\n\n<p>The for reporting and forwarding the email.</p>\n\n<p>Based on the automated analysis performed by Splunk SOAR and Splunk Attack Analyzer, this email has been categorised as &quot;Safe&quot;.</p>\n\n<p>If you have any further concerns or if you would like to know more on the investigation of this phishing attempt and analysis, reach out to your friendly Splunk Security team at UoB, otherwise no further actions are required from your end.</p>\n\n<p> Thanks</p>\n""",
        parameters=[])

    parameters = []

    if html_body_formatted_string is not None:
        parameters.append({
            "to": "jarora@splunk.com",
            "from": "splunksoarpoc@gmail.com",
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

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_2", assets=["soar_poc_smtp"])

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