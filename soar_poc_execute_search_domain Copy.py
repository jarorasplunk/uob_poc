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
        "query": "index=botsv* sourcetype=\"o365:management:activity\" | lookup local_domain_soar_poc domain as dvc OUTPUT threat_key domain as match| search threat_key = domain |table _time user dvc threat_key match action",
        "command": "search",
        "display": "_time,user,dvc,threat_key,match,action",
        "start_time": "-2m",
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
        "query": "index=botsv* sourcetype=\"o365:management:activity\" | lookup local_domain_soar_poc domain as dvc OUTPUT threat_key domain as match| search threat_key = domain |table _time user dvc threat_key match action | dedup match|table match",
        "command": "search",
        "start_time": "-2m",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="query_unique_character", assets=["splunk_result_internal"], callback=get_the_domain_name)

    return


@phantom.playbook_block()
def get_the_domain_name(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_the_domain_name() called")

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

    phantom.format(container=container, template=template, parameters=parameters, name="get_the_domain_name", drop_none=True)

    string_split_3(container=container)

    return


@phantom.playbook_block()
def domain_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("domain_reputation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    string_split_3_data = phantom.collect2(container=container, datapath=["string_split_3:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'domain_reputation_1' call
    for string_split_3_data_item in string_split_3_data:
        if string_split_3_data_item[0] is not None:
            parameters.append({
                "domain": string_split_3_data_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("domain reputation", parameters=parameters, name="domain_reputation_1", assets=["soar_poc_virustotal"])

    return


@phantom.playbook_block()
def string_split_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("string_split_3() called")

    get_the_domain_name = phantom.get_format_data(name="get_the_domain_name")

    parameters = []

    parameters.append({
        "delimiter": ",",
        "input_string": get_the_domain_name,
        "strip_whitespace": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/string_split", parameters=parameters, name="string_split_3", callback=string_split_3_callback)

    return


@phantom.playbook_block()
def string_split_3_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("string_split_3_callback() called")

    
    domain_reputation_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    whois_domain_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def whois_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("whois_domain_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    string_split_3_data = phantom.collect2(container=container, datapath=["string_split_3:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'whois_domain_1' call
    for string_split_3_data_item in string_split_3_data:
        if string_split_3_data_item[0] is not None:
            parameters.append({
                "domain": string_split_3_data_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("whois domain", parameters=parameters, name="whois_domain_1", assets=["whois"])

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