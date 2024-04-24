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
        format_header_note_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

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
        pass

    return


@phantom.playbook_block()
def format_header_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_header_note_1() called")

    filtered_artifact_0_data_filter_email_artifact = phantom.collect2(container=container, datapath=["filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.To","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Date","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.From","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Subject","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.References","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.In-Reply-To","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Content-Type","filtered-data:filter_email_artifact:condition_1:artifact:*.cef.emailHeaders.Content-Transfer-Encoding"], scope="all")

    filtered_artifact_0__cef_emailheaders_to = [item[0] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_date = [item[1] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_from = [item[2] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_subject = [item[3] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_references = [item[4] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_in_reply_to = [item[5] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_content_type = [item[6] for item in filtered_artifact_0_data_filter_email_artifact]
    filtered_artifact_0__cef_emailheaders_content_transfer_encoding = [item[7] for item in filtered_artifact_0_data_filter_email_artifact]

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
    phantom.debug(filtered_artifact_0__cef_emailheaders_content_type[0])
    phantom.debug(filtered_artifact_0__cef_emailheaders_content_transfer_encoding[0])
    sender = filtered_artifact_0__cef_emailheaders_from[0]
    phantom.debug("sender before")
    phantom.debug(sender)
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', sender)
    sender = match[0]
    phantom.debug("sender after")
    phantom.debug(sender)
    sender_domain = sender[sender.index('@') + 1 : ]
    replyto = filtered_artifact_0__cef_emailheaders_in_reply_to[0]
    phantom.debug("replyto")
    phantom.debug(replyto)
    recipient = filtered_artifact_0__cef_emailheaders_to[0]
    phantom.debug("recipient before")
    phantom.debug(recipient)
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', recipient)
    recipient = match[0]
    phantom.debug("recipient after")
    phantom.debug(recipient)
    date = filtered_artifact_0__cef_emailheaders_date[0]
    routing_info = filtered_artifact_0__cef_emailheaders_references[0]
    contenttype = filtered_artifact_0__cef_emailheaders_content_type[0]
    contentencoding = filtered_artifact_0__cef_emailheaders_content_transfer_encoding[0]
    
    note = (
        "| Sender email | Sender domain | Reply To | Recipient | Date | Routing information | Content type | Content Encoding |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    )
    
    note += "|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(sender, sender_domain, replyto, recipient, date, routing_info, contenttype, contentencoding)
    
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