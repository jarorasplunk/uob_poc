"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_job_forensics_1' block
    get_job_forensics_1(container=container)

    return

@phantom.playbook_block()
def get_job_forensics_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_job_forensics_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "job_id": "1fbc2149-4b51-445f-a301-656e02a6c7db",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get job forensics", parameters=parameters, name="get_job_forensics_1", assets=["saa_uob_poc"], callback=code_1)

    return


@phantom.playbook_block()
def code_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("code_1() called")

    get_job_forensics_1_result_data = phantom.collect2(container=container, datapath=["get_job_forensics_1:action_result.data","get_job_forensics_1:action_result.data.*.WhoisResults"], action_results=results)

    get_job_forensics_1_result_item_0 = [item[0] for item in get_job_forensics_1_result_data]
    get_job_forensics_1_result_item_1 = [item[1] for item in get_job_forensics_1_result_data]

    code_1__whois_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import json
    
    #phantom.debug(get_job_forensics_1_result_item_0)
    whois_data_json = get_job_forensics_1_result_item_1[0][0]
    phantom.debug(whois_data_json)
    phantom.debug(whois_data_json['Emails'])
    note = (
        "| Key | Value |\n"
        "| :--- | :--- |\n"
    )

    note += "|{}|{}|\n".format("Org", whois_data_json['Org'])
    note += "|{}|{}|\n".format("City", whois_data_json['City'])
    note += "|{}|{}|\n".format("Name", whois_data_json['Name'])
    note += "|{}|{}|\n".format("State", whois_data_json['State'])
    note += "|{}|{}|\n".format("DNSSec", whois_data_json['DNSSec'])
    note += "|{}|{}|\n".format("Emails", whois_data_json['Emails'])
    note += "|{}|{}|\n".format("Address", whois_data_json['Address'])
    note += "|{}|{}|\n".format("Country", whois_data_json['Country'])
    note += "|{}|{}|\n".format("Engines", whois_data_json['Engines'])
    note += "|{}|{}|\n".format("ZipCode", whois_data_json['ZipCode'])
    note += "|{}|{}|\n".format("CreatedAt", whois_data_json['CreatedAt'])
    note += "|{}|{}|\n".format("ExpiresAt", whois_data_json['ExpiresAt'])
    note += "|{}|{}|\n".format("Registrar", whois_data_json['Registrar'])
    note += "|{}|{}|\n".format("UpdatedAt", whois_data_json['UpdatedAt'])
    note += "|{}|{}|\n".format("DomainName", whois_data_json['DomainName'])
    note += "|{}|{}|\n".format("NameServers", whois_data_json['NameServers'])
    note += "|{}|{}|\n".format("WhoisServer", whois_data_json['WhoisServer'])
    note += "|{}|{}|\n".format("WhoisServer", whois_data_json['WhoisServer'])
    note += "|{}|{}|\n".format("WhoisServer", whois_data_json['WhoisServer'])
    
    code_1__whois_note = note

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="code_1:whois_note", value=json.dumps(code_1__whois_note))

    add_note_1(container=container)

    return


@phantom.playbook_block()
def add_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_1() called")

    code_1__whois_note = json.loads(_ if (_ := phantom.get_run_data(key="code_1:whois_note")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=code_1__whois_note, note_format="markdown", note_type="general", title="Whois information")

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