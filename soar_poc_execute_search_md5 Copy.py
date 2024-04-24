"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'run_query_1' block
    run_query_1(container=container)

    return

@phantom.playbook_block()
def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("run_query_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "query": "index=botsv* sourcetype=\"XmlWinEventLog\" | lookup local_md5_soar_poc md5 as MD5 OUTPUT threat_key md5 as match | search threat_key = md5 |table _time user MD5 threat_key match",
        "command": "search",
        "display": "_time,user,MD5,threat_key,match",
        "start_time": "-1d",
        "attach_result": False,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # calculate start time using delay of 1.5 minutes
    start_time = datetime.now() + timedelta(minutes=1.5)
    phantom.act("run query", parameters=parameters, name="run_query_1", start_time=start_time, assets=["splunk"], callback=query_unique_character)

    return


@phantom.playbook_block()
def query_unique_character(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("query_unique_character() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "query": "index=botsv* sourcetype=\"XmlWinEventLog\" | lookup local_md5_soar_poc md5 as MD5 OUTPUT threat_key md5 as match | search threat_key = md5 |table _time user MD5 threat_key match |dedup match | table match",
        "command": "search",
        "start_time": "-1d",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="query_unique_character", assets=["splunk_result_internal"], callback=get_the_md5)

    return


@phantom.playbook_block()
def get_the_md5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_the_md5() called")

    template = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "query_unique_character:action_result.data.*.match"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="get_the_md5", drop_none=True)

    string_split_3(container=container)

    return


@phantom.playbook_block()
def file_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("file_reputation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    string_split_3_data = phantom.collect2(container=container, datapath=["string_split_3:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'file_reputation_1' call
    for string_split_3_data_item in string_split_3_data:
        if string_split_3_data_item[0] is not None:
            parameters.append({
                "hash": string_split_3_data_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("file reputation", parameters=parameters, name="file_reputation_1", assets=["soar_poc_virustotal"])

    return


@phantom.playbook_block()
def string_split_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("string_split_3() called")

    get_the_md5 = phantom.get_format_data(name="get_the_md5")

    parameters = []

    parameters.append({
        "delimiter": ",",
        "input_string": get_the_md5,
        "strip_whitespace": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/string_split", parameters=parameters, name="string_split_3", callback=file_reputation_1)

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