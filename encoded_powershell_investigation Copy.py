"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'decode_base64' block
    decode_base64(container=container)

    return

@phantom.playbook_block()
def decode_base64(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decode_base64() called")

    playbook_input_powershell_process = phantom.collect2(container=container, datapath=["playbook_input:powershell_process"])

    parameters = []

    # build parameters list for 'decode_base64' call
    for playbook_input_powershell_process_item in playbook_input_powershell_process:
        parameters.append({
            "delimiter": "space",
            "split_input": True,
            "input_string": playbook_input_powershell_process_item[0],
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/base64_decode", parameters=parameters, name="decode_base64", callback=decision_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["decode_base64:custom_function_result.data.*.output_string", "!=", ""]
        ],
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        decode_nest_base64(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def decode_nest_base64(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decode_nest_base64() called")

    decode_base64_data = phantom.collect2(container=container, datapath=["decode_base64:custom_function_result.data.*.output_string"])

    parameters = []

    # build parameters list for 'decode_nest_base64' call
    for decode_base64_data_item in decode_base64_data:
        parameters.append({
            "delimiter": "'",
            "split_input": True,
            "input_string": decode_base64_data_item[0],
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/base64_decode", parameters=parameters, name="decode_nest_base64", callback=decode_nest_base64_callback)

    return


@phantom.playbook_block()
def decode_nest_base64_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decode_nest_base64_callback() called")

    
    regex_extract_ipv4_4(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    regex_extract_ipv4_5(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def regex_extract_ipv4_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_extract_ipv4_4() called")

    decode_base64_data = phantom.collect2(container=container, datapath=["decode_base64:custom_function_result.data.*.output_string"])

    decode_base64_data___output_string = [item[0] for item in decode_base64_data]

    parameters = []

    parameters.append({
        "input_string": decode_base64_data___output_string,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    parameters = []
    for item in decode_base64_data___output_string:
        parameters.append({
            "input_string": item,
        })

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_extract_ipv4", parameters=parameters, name="regex_extract_ipv4_4", callback=join_decision_3)

    return


@phantom.playbook_block()
def regex_extract_ipv4_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_extract_ipv4_5() called")

    decode_nest_base64_data = phantom.collect2(container=container, datapath=["decode_nest_base64:custom_function_result.data.*.output_string"])

    decode_nest_base64_data___output_string = [item[0] for item in decode_nest_base64_data]

    parameters = []

    parameters.append({
        "input_string": decode_nest_base64_data___output_string,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    parameters = []
    for item in decode_nest_base64_data___output_string:
        parameters.append({
            "input_string": item,
        })

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_extract_ipv4", parameters=parameters, name="regex_extract_ipv4_5", callback=join_decision_3)

    return


@phantom.playbook_block()
def calculate_times(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("calculate_times() called")

    create_time_value = container.get("create_time", None)

    calculate_times__earliest_time = None
    calculate_times__latest_time = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    from dateutil import parser
    
    # how much to adjust time in seconds
    time_window = 86400
    epoch_time = parser.parse(create_time_value).timestamp()
    # calculate earliest
    calculate_times__earliest_time = epoch_time - time_window

    # calculate latest
    calculate_times__latest_time = epoch_time + time_window




    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="calculate_times:earliest_time", value=json.dumps(calculate_times__earliest_time))
    phantom.save_run_data(key="calculate_times:latest_time", value=json.dumps(calculate_times__latest_time))

    format_splunk_query(container=container)

    return


@phantom.playbook_block()
def format_splunk_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_splunk_query() called")

    template = """`summariesonly` max(_time) as _time, count from datamodel=Network_Traffic.All_Traffic where All_Traffic.src IN \n(\"{0}{1}\") OR All_Traffic.src_ip IN (\"{0}{1}\") OR All_Traffic.src_translated_ip IN (\"{0}{1}\") OR All_Traffic.dest IN \n(\"{0}{1}\") OR All_Traffic.dest_ip IN (\"{0}{1}\") OR All_Traffic.dest_translated_ip IN (\"{0}{1}\") (earliest={2} latest={3}) by All_Traffic.action, All_Traffic.src All_Traffic.dest, All_Traffic.transport | `drop_dm_object_name(\"All_Traffic\")` | sort - count | fields _time,action,src,dest,transport,count """

    # parameter list for template variable replacement
    parameters = [
        "regex_extract_ipv4_4:custom_function_result.data.extracted_ipv4",
        "regex_extract_ipv4_5:custom_function_result.data.extracted_ipv4",
        "calculate_times:custom_function:earliest_time",
        "calculate_times:custom_function:latest_time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_splunk_query", drop_none=True)

    splunk_query(container=container)

    return


@phantom.playbook_block()
def join_decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_decision_3() called")

    if phantom.completed(custom_function_names=["regex_extract_ipv4_4", "regex_extract_ipv4_5"]):
        # call connected block "decision_3"
        decision_3(container=container, handle=handle)

    return


@phantom.playbook_block()
def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_3() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="or",
        conditions=[
            ["regex_extract_ipv4_4:custom_function_result.data.extracted_ipv4", "!=", ""],
            ["regex_extract_ipv4_5:custom_function_result.data.extracted_ipv4", "!=", ""]
        ],
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        calculate_times(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    format_1(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def splunk_query(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("splunk_query() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    format_splunk_query = phantom.get_format_data(name="format_splunk_query")

    parameters = []

    if format_splunk_query is not None:
        parameters.append({
            "query": format_splunk_query,
            "command": "tstats",
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="splunk_query", assets=["splunk"], callback=format_2)

    return


@phantom.playbook_block()
def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_1() called")

    template = """Splunk SOAR found a possible base64 encoded string and decoded it:\n\n```{0}```\n\nSOAR attempted a second decode. If available, the results are shown below.\n\n```{1}```\n\nThere was no match to an IP address during the second decode."""

    # parameter list for template variable replacement
    parameters = [
        "decode_base64:custom_function_result.data.*.output_string",
        "decode_nest_base64:custom_function_result.data.*.output_string"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_1", drop_none=True)

    join_format_5(container=container)

    return


@phantom.playbook_block()
def format_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_2() called")

    template = """Splunk SOAR found a possible base64 encoded string and decoded it:\n\n```{0}```\n\nSOAR attempted a second decode. If available, the results are shown below.\n\n```{1}```\n\n---\n\nThe decode action discovered an IP address in the data.\nSOAR searched a time window within Splunk based on the earliest and latest times from the artifacts.\n\nResults are shown in the table below:\n\n| _time | action | src | dest | transport | count |\n| --- | --- | --- | --- | --- | --- |\n%%\n| {2} | {3} | {4} | {5} | {6} | {7} |\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "decode_base64:custom_function_result.data.*.output_string",
        "decode_nest_base64:custom_function_result.data.*.output_string",
        "splunk_query:action_result.data.*._time",
        "splunk_query:action_result.data.*.action",
        "splunk_query:action_result.data.*.src",
        "splunk_query:action_result.data.*.dest",
        "splunk_query:action_result.data.*.transport",
        "splunk_query:action_result.data.*.count"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_2", drop_none=True)

    join_format_5(container=container)

    return


@phantom.playbook_block()
def join_format_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_format_5() called")

    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key="join_format_5_called"):
        return

    # save the state that the joined function has now been called
    phantom.save_run_data(key="join_format_5_called", value="format_5")

    # call connected block "format_5"
    format_5(container=container, handle=handle)

    return


@phantom.playbook_block()
def format_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_5() called")

    template = """{0} {1}\n"""

    # parameter list for template variable replacement
    parameters = [
        "format_1:formatted_data",
        "format_2:formatted_data"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_5", drop_none=True)

    format_6(container=container)

    return


@phantom.playbook_block()
def format_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_6() called")

    template = """First decode of base64 encoded command:\n\n```{0}```\n\n---\n\n"""

    # parameter list for template variable replacement
    parameters = [
        "decode_base64:custom_function_result.data.*.output_string"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_6")

    format_3(container=container)

    return


@phantom.playbook_block()
def format_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_3() called")

    template = """Second decode for nested base64 encoded command:\n\n```{0}```\n\n---"""

    # parameter list for template variable replacement
    parameters = [
        "decode_nest_base64:custom_function_result.data.*.output_string"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_3")

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    format_5 = phantom.get_format_data(name="format_5")
    format_6 = phantom.get_format_data(name="format_6")
    format_3 = phantom.get_format_data(name="format_3")

    output = {
        "note_title": ["Encoded Powershell Investigation"],
        "note_content": format_5,
        "note_decoded_proc_info_first": format_6,
        "note_decoded_proc_info_second": format_3,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return