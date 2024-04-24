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
        "query": "index=botsv* sourcetype=pan:traffic | lookup local_ip_soar_poc ip as dest OUTPUT threat_key ip as match | search threat_key = ip |table _time src dest threat_key match",
        "command": "search",
        "display": "_time,src,dest,match,threat_key",
        "start_time": "-3d",
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
    phantom.act("run query", parameters=parameters, name="run_query_1", start_time=start_time, assets=["splunk"], callback=run_query_2)

    return


@phantom.playbook_block()
def run_query_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("run_query_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "query": "index=botsv* sourcetype=pan:traffic | lookup local_ip_soar_poc ip as dest OUTPUT threat_key ip as match | search threat_key = ip |table _time src dest threat_key match | dedup match | table match",
        "command": "search",
        "start_time": "-3d",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="run_query_2", assets=["splunk_result_internal"], callback=format_4)

    return


@phantom.playbook_block()
def format_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_4() called")

    template = """%%\n{0}\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "run_query_2:action_result.data"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_4", drop_none=True)

    regex_extract_ipv4_8(container=container)

    return


@phantom.playbook_block()
def regex_extract_ipv4_8(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_extract_ipv4_8() called")

    format_4__as_list = phantom.get_format_data(name="format_4__as_list")

    parameters = []

    # build parameters list for 'regex_extract_ipv4_8' call
    for format_4__item in format_4__as_list:
        parameters.append({
            "input_string": format_4__item,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_extract_ipv4", parameters=parameters, name="regex_extract_ipv4_8", callback=regex_extract_ipv4_8_callback)

    return


@phantom.playbook_block()
def regex_extract_ipv4_8_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_extract_ipv4_8_callback() called")

    
    ip_reputation_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    whois_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    geolocate_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def ip_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ip_reputation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    regex_extract_ipv4_8__result = phantom.collect2(container=container, datapath=["regex_extract_ipv4_8:custom_function_result.data.extracted_ipv4"])

    parameters = []

    # build parameters list for 'ip_reputation_1' call
    for regex_extract_ipv4_8__result_item in regex_extract_ipv4_8__result:
        if regex_extract_ipv4_8__result_item[0] is not None:
            parameters.append({
                "ip": regex_extract_ipv4_8__result_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("ip reputation", parameters=parameters, name="ip_reputation_1", assets=["soar_poc_virustotal"])

    return


@phantom.playbook_block()
def whois_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("whois_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    regex_extract_ipv4_8__result = phantom.collect2(container=container, datapath=["regex_extract_ipv4_8:custom_function_result.data.extracted_ipv4"])

    parameters = []

    # build parameters list for 'whois_ip_1' call
    for regex_extract_ipv4_8__result_item in regex_extract_ipv4_8__result:
        if regex_extract_ipv4_8__result_item[0] is not None:
            parameters.append({
                "ip": regex_extract_ipv4_8__result_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("whois ip", parameters=parameters, name="whois_ip_1", assets=["whois"])

    return


@phantom.playbook_block()
def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("geolocate_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    regex_extract_ipv4_8__result = phantom.collect2(container=container, datapath=["regex_extract_ipv4_8:custom_function_result.data.extracted_ipv4"])

    parameters = []

    # build parameters list for 'geolocate_ip_1' call
    for regex_extract_ipv4_8__result_item in regex_extract_ipv4_8__result:
        if regex_extract_ipv4_8__result_item[0] is not None:
            parameters.append({
                "ip": regex_extract_ipv4_8__result_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("geolocate ip", parameters=parameters, name="geolocate_ip_1", assets=["maxmind"])

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