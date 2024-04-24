"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'assets_and_identities_enrichment' block
    assets_and_identities_enrichment(container=container)

    return

@phantom.playbook_block()
def assets_and_identities_enrichment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("assets_and_identities_enrichment() called")

    inputs = {
        "user": [],
        "src_user": [],
        "src": [],
        "dest": [],
        "src_ip": [],
        "dest_hostname": [],
        "computername": [],
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "uob_poc/assets_and_identities_enrichment Copy", returns the playbook_run_id
    playbook_run_id = phantom.playbook("uob_poc/assets_and_identities_enrichment Copy", container=container, name="assets_and_identities_enrichment", callback=es_process_analysis, inputs=inputs)

    return


@phantom.playbook_block()
def add_note_identity(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_identity() called")

    assets_and_identities_enrichment_output_task_note_identity = phantom.collect2(container=container, datapath=["assets_and_identities_enrichment:playbook_output:task_note_identity"])

    assets_and_identities_enrichment_output_task_note_identity_values = [item[0] for item in assets_and_identities_enrichment_output_task_note_identity]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    assets_and_identities_enrichment_output_task_note_identity_values = assets_and_identities_enrichment_output_task_note_identity_values[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=assets_and_identities_enrichment_output_task_note_identity_values, note_format="markdown", note_type="general", title="Identity details")

    add_note_assets(container=container)

    return


@phantom.playbook_block()
def add_note_assets(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_assets() called")

    assets_and_identities_enrichment_output_task_note_assets = phantom.collect2(container=container, datapath=["assets_and_identities_enrichment:playbook_output:task_note_assets"])

    assets_and_identities_enrichment_output_task_note_assets_values = [item[0] for item in assets_and_identities_enrichment_output_task_note_assets]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    assets_and_identities_enrichment_output_task_note_assets_values = assets_and_identities_enrichment_output_task_note_assets_values[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=assets_and_identities_enrichment_output_task_note_assets_values, note_format="markdown", note_type="general", title="Asset details")

    send_htmlemail_1(container=container)

    return


@phantom.playbook_block()
def es_process_analysis(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("es_process_analysis() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "uob_poc/ES Process Analysis Copy", returns the playbook_run_id
    playbook_run_id = phantom.playbook("uob_poc/ES Process Analysis Copy", container=container, name="es_process_analysis", callback=es_indicator_reputation_analysis)

    return


@phantom.playbook_block()
def es_indicator_reputation_analysis(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("es_indicator_reputation_analysis() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "uob_poc/ES Indicator Reputation Analysis Copy", returns the playbook_run_id
    playbook_run_id = phantom.playbook("uob_poc/ES Indicator Reputation Analysis Copy", container=container, name="es_indicator_reputation_analysis", callback=add_note_identity)

    return


@phantom.playbook_block()
def send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    subject_formatted_string = phantom.format(
        container=container,
        template="""Suspicious activity found on User computer: {0}\n""",
        parameters=[
            "artifact:*.cef.dest_nt_host"
        ])
    html_body_formatted_string = phantom.format(
        container=container,
        template="""<p>Hi {0},</p>\n\n<p>Please find below details of the suspicious activity found on your computer: {1}</p>\n\n<p>{2} </p>\n<p>{3} </p>\n<p>{5} </p>\n\n<p><strong>Action required </strong> Click on one of the links below to respond to this notification. This will create an email response and then you can click send without making any changes:</p>\n\n<p><a href=\"mailto:splunksoarpoc@gmail.com?subject={4}-User-{0}%20Response&body=Expected%20behaviour\">Expected behaviour</a></p>\n\n<p><a href=\"mailto:splunksoarpoc@gmail.com?subject={4}-User-{0}%20Response&body=Not%20expected%20behaviour\">Not expected behaviour</a></p>\n\n<p></p>""",
        parameters=[
            "artifact:*.cef.normalized_risk_object",
            "artifact:*.cef.dest_nt_host",
            "es_process_analysis:playbook_output:note_title",
            "es_process_analysis:playbook_output:note_content_process_info_first",
            "container:id",
            "es_process_analysis:playbook_output:note_content_process_info_second"
        ])

    id_value = container.get("id", None)
    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.dest_nt_host","artifact:*.cef.normalized_risk_object","artifact:*.id"])
    es_process_analysis_output_note_title = phantom.collect2(container=container, datapath=["es_process_analysis:playbook_output:note_title"])
    es_process_analysis_output_note_content_process_info_first = phantom.collect2(container=container, datapath=["es_process_analysis:playbook_output:note_content_process_info_first"])
    es_process_analysis_output_note_content_process_info_second = phantom.collect2(container=container, datapath=["es_process_analysis:playbook_output:note_content_process_info_second"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for container_artifact_item in container_artifact_data:
        for es_process_analysis_output_note_title_item in es_process_analysis_output_note_title:
            for es_process_analysis_output_note_content_process_info_first_item in es_process_analysis_output_note_content_process_info_first:
                for es_process_analysis_output_note_content_process_info_second_item in es_process_analysis_output_note_content_process_info_second:
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

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_1", assets=["soar_poc"], callback=decision_1)

    return


@phantom.playbook_block()
def playbook_user_response_outcome_v2_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_user_response_outcome_v2_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/User response outcome v2", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/User response outcome v2", container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["send_htmlemail_1:action_result.status", "==", "success"]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        set_label_2(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def set_label_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_label_2() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_label(container=container, label="process_analysed")

    container = phantom.get_container(container.get('id', None))

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