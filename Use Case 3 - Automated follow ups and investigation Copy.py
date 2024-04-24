"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'playbook_assets_and_identities_enrichment_1' block
    playbook_assets_and_identities_enrichment_1(container=container)

    return

@phantom.playbook_block()
def playbook_assets_and_identities_enrichment_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_assets_and_identities_enrichment_1() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.normalized_risk_object","artifact:*.cef.risk_object","artifact:*.cef.dest_nt_host"], scope="all")

    container_artifact_cef_item_0 = [item[0] for item in container_artifact_data]
    container_artifact_cef_item_1 = [item[1] for item in container_artifact_data]
    container_artifact_cef_item_2 = [item[2] for item in container_artifact_data]

    inputs = {
        "src": [],
        "dest": [],
        "user": container_artifact_cef_item_0,
        "src_ip": [],
        "src_user": container_artifact_cef_item_1,
        "computername": [],
        "dest_hostname": container_artifact_cef_item_2,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/assets_and_identities_enrichment", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/assets_and_identities_enrichment", container=container, name="playbook_assets_and_identities_enrichment_1", callback=playbook_es_process_analysis_1, inputs=inputs)

    return


@phantom.playbook_block()
def add_note_identity(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_identity() called")

    playbook_assets_and_identities_enrichment_1_output_task_note_identity = phantom.collect2(container=container, datapath=["playbook_assets_and_identities_enrichment_1:playbook_output:task_note_identity"])

    playbook_assets_and_identities_enrichment_1_output_task_note_identity_values = [item[0] for item in playbook_assets_and_identities_enrichment_1_output_task_note_identity]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    playbook_assets_and_identities_enrichment_1_output_task_note_identity_values = playbook_assets_and_identities_enrichment_1_output_task_note_identity_values[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=playbook_assets_and_identities_enrichment_1_output_task_note_identity_values, note_format="markdown", note_type="general", title="Identity details")

    add_note_assets(container=container)

    return


@phantom.playbook_block()
def add_note_assets(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_assets() called")

    playbook_assets_and_identities_enrichment_1_output_task_note_assets = phantom.collect2(container=container, datapath=["playbook_assets_and_identities_enrichment_1:playbook_output:task_note_assets"])

    playbook_assets_and_identities_enrichment_1_output_task_note_assets_values = [item[0] for item in playbook_assets_and_identities_enrichment_1_output_task_note_assets]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    playbook_assets_and_identities_enrichment_1_output_task_note_assets_values = playbook_assets_and_identities_enrichment_1_output_task_note_assets_values[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=playbook_assets_and_identities_enrichment_1_output_task_note_assets_values, note_format="markdown", note_type="general", title="Asset details")

    send_htmlemail_1(container=container)

    return


@phantom.playbook_block()
def playbook_es_process_analysis_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_es_process_analysis_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/ES Process Analysis", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/ES Process Analysis", container=container, name="playbook_es_process_analysis_1", callback=playbook_es_indicator_reputation_analysis_1)

    return


@phantom.playbook_block()
def playbook_es_indicator_reputation_analysis_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_es_indicator_reputation_analysis_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/ES Indicator Reputation Analysis", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/ES Indicator Reputation Analysis", container=container, name="playbook_es_indicator_reputation_analysis_1", callback=add_note_identity)

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
            "playbook_es_process_analysis_1:playbook_output:note_title",
            "playbook_es_process_analysis_1:playbook_output:note_content_process_info_first",
            "container:id",
            "playbook_es_process_analysis_1:playbook_output:note_content_process_info_second"
        ])

    id_value = container.get("id", None)
    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.dest_nt_host","artifact:*.cef.normalized_risk_object","artifact:*.id"])
    playbook_es_process_analysis_1_output_note_title = phantom.collect2(container=container, datapath=["playbook_es_process_analysis_1:playbook_output:note_title"])
    playbook_es_process_analysis_1_output_note_content_process_info_first = phantom.collect2(container=container, datapath=["playbook_es_process_analysis_1:playbook_output:note_content_process_info_first"])
    playbook_es_process_analysis_1_output_note_content_process_info_second = phantom.collect2(container=container, datapath=["playbook_es_process_analysis_1:playbook_output:note_content_process_info_second"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for container_artifact_item in container_artifact_data:
        for playbook_es_process_analysis_1_output_note_title_item in playbook_es_process_analysis_1_output_note_title:
            for playbook_es_process_analysis_1_output_note_content_process_info_first_item in playbook_es_process_analysis_1_output_note_content_process_info_first:
                for playbook_es_process_analysis_1_output_note_content_process_info_second_item in playbook_es_process_analysis_1_output_note_content_process_info_second:
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

    phantom.act("send htmlemail", parameters=parameters, name="send_htmlemail_1", assets=["soar_poc_smtp"])

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