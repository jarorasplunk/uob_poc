"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_indicator' block
    filter_indicator(container=container)

    return

@phantom.playbook_block()
def filter_indicator(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_indicator() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:ip", "!=", ""]
        ],
        name="filter_indicator:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        hunt_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:domain", "!=", ""]
        ],
        name="filter_indicator:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        pass

    # collect filtered artifact ids and results for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:url", "!=", ""]
        ],
        name="filter_indicator:condition_3",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        pass

    # collect filtered artifact ids and results for 'if' condition 4
    matched_artifacts_4, matched_results_4 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:hash", "!=", ""]
        ],
        name="filter_indicator:condition_4",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_4 or matched_results_4:
        pass

    return


@phantom.playbook_block()
def hunt_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("hunt_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_input_0_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_indicator:condition_1:playbook_input:ip"])

    parameters = []

    # build parameters list for 'hunt_ip_1' call
    for filtered_input_0_ip_item in filtered_input_0_ip:
        if filtered_input_0_ip_item[0] is not None:
            parameters.append({
                "ip": filtered_input_0_ip_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("hunt ip", parameters=parameters, name="hunt_ip_1", assets=["trustar - abc"], callback=indicator_reputation_1)

    return


@phantom.playbook_block()
def check_for_report(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("check_for_report() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["hunt_ip_1:action_result.data.*.report_id", "!=", ""]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        conditions=[
            ["indicator_reputation_1:action_result.summary.indicators_found", "!=", 0]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        return

    # check for 'elif' condition 3
    found_match_3 = phantom.decision(
        container=container,
        conditions=[
            ["get_indicator_summary_1:action_result.status", "==", "success"]
        ],
        delimiter=None)

    # call connected blocks if condition 3 matched
    if found_match_3:
        return

    return


@phantom.playbook_block()
def get_report_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_report_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_enrich_indicator = phantom.collect2(container=container, datapath=["filtered-data:enrich_indicator:condition_1:hunt_ip_1:action_result.data.*.report_id"])

    parameters = []

    # build parameters list for 'get_report_1' call
    for filtered_result_0_item_enrich_indicator in filtered_result_0_data_enrich_indicator:
        if filtered_result_0_item_enrich_indicator[0] is not None:
            parameters.append({
                "report_id": filtered_result_0_item_enrich_indicator[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get report", parameters=parameters, name="get_report_1", assets=["trustar - abc"], callback=find_indicator)

    return


@phantom.playbook_block()
def get_indicator_summary_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_indicator_summary_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_input_0_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_indicator:condition_1:playbook_input:ip"])

    parameters = []

    # build parameters list for 'get_indicator_summary_1' call
    for filtered_input_0_ip_item in filtered_input_0_ip:
        if filtered_input_0_ip_item[0] is not None:
            parameters.append({
                "enclave_ids": "38658197-4e9b-4651-9381-1c62c9d2cca0,77033ea5-3b8b-45ad-9120-7e0ea35baed5,ddc86a8b-9d8b-4cd4-8a55-96670b504df1,109940b7-1004-4b23-bfb0-c4df740d82f9,0f9fe120-f904-4750-baf7-731f8552016f,be86dc88-50c8-447f-b4ed-14797ed9ba4b,e100e42a-0550-46e5-b9e6-c99b405a7200,7e09b124-b631-44e2-b261-57d53dd727d0,11125bbd-ca70-4f16-bce2-7e361693ceb2,27f5a1a3-faf6-4cf6-93bf-8ab0cfd008a8,b85b0cfc-3be1-44ef-9077-5d7d8c049991,cb0f3a77-122d-4c9e-a2c6-f832369ad2e9,5ff109d4-a5b7-434a-8397-eef28ac05d67,8f7b34f8-9e99-4cc4-91eb-9f014e82f1bc",
                "indicator_values": filtered_input_0_ip_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get indicator summary", parameters=parameters, name="get_indicator_summary_1", assets=["trustar - abc"], callback=enrich_indicator)

    return


@phantom.playbook_block()
def trustar_report_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("trustar_report_details() called")

    template = """# Trustar Report: Associated Reports and Extracted Indicators Details:\n%%\nReport ID: {0}\nReport Title: {1}\n\n%%\n\n\n{2}\n"""

    # parameter list for template variable replacement
    parameters = [
        "get_report_1:action_result.parameter.report_id",
        "get_report_1:action_result.data.*.title",
        "report_output_format:custom_function:report_output"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="trustar_report_details")

    join_create_output(container=container)

    return


@phantom.playbook_block()
def join_create_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_create_output() called")

    if phantom.completed(action_names=["get_report_1", "get_indicator_summary_1"]):
        # call connected block "create_output"
        create_output(container=container, handle=handle)

    return


@phantom.playbook_block()
def create_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("create_output() called")

    indicator_summary_details = phantom.get_format_data(name="indicator_summary_details")
    indicator_reputation_details = phantom.get_format_data(name="indicator_reputation_details")
    trustar_report_details = phantom.get_format_data(name="trustar_report_details")

    create_output__output_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    
    phantom.debug(type(trustar_report_details))
    phantom.debug(trustar_report_details)

    phantom.debug(type(indicator_reputation_details))
    phantom.debug(indicator_reputation_details)
    
    phantom.debug(type(indicator_summary_details))
    phantom.debug(indicator_summary_details)
    
    create_output__output_note = "\n"
    if indicator_summary_details:
        create_output__output_note += indicator_summary_details + "\n" 

    if trustar_report_details:
        create_output__output_note += trustar_report_details + "\n"

    if indicator_reputation_details:
        create_output__output_note += indicator_reputation_details
    
    #phantom.debug(create_output__output_note)
        
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="create_output:output_note", value=json.dumps(create_output__output_note))

    add_note_2(container=container)

    return


@phantom.playbook_block()
def add_note_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_note_2() called")

    create_output__output_note = json.loads(_ if (_ := phantom.get_run_data(key="create_output:output_note")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_note(container=container, content=create_output__output_note, note_format="markdown", note_type="general", title="trustar enrichment details")

    return


@phantom.playbook_block()
def indicator_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_reputation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_input_0_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_indicator:condition_1:playbook_input:ip"])

    parameters = []

    # build parameters list for 'indicator_reputation_1' call
    for filtered_input_0_ip_item in filtered_input_0_ip:
        if filtered_input_0_ip_item[0] is not None:
            parameters.append({
                "limit": 10000,
                "enclave_ids": "38658197-4e9b-4651-9381-1c62c9d2cca0,77033ea5-3b8b-45ad-9120-7e0ea35baed5,ddc86a8b-9d8b-4cd4-8a55-96670b504df1,109940b7-1004-4b23-bfb0-c4df740d82f9,0f9fe120-f904-4750-baf7-731f8552016f,be86dc88-50c8-447f-b4ed-14797ed9ba4b,e100e42a-0550-46e5-b9e6-c99b405a7200,7e09b124-b631-44e2-b261-57d53dd727d0,11125bbd-ca70-4f16-bce2-7e361693ceb2,27f5a1a3-faf6-4cf6-93bf-8ab0cfd008a8,b85b0cfc-3be1-44ef-9077-5d7d8c049991,cb0f3a77-122d-4c9e-a2c6-f832369ad2e9,5ff109d4-a5b7-434a-8397-eef28ac05d67,8f7b34f8-9e99-4cc4-91eb-9f014e82f1bc",
                "indicator_value": filtered_input_0_ip_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("indicator reputation", parameters=parameters, name="indicator_reputation_1", assets=["trustar - abc"], callback=get_indicator_summary_1)

    return


@phantom.playbook_block()
def find_indicator(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("find_indicator() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["get_report_1:action_result.summary.extracted_indicators_count", "==", 0]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        report_output_format(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def report_output_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("report_output_format() called")

    get_report_1_result_data = phantom.collect2(container=container, datapath=["get_report_1:action_result.data.*.reportBody"], action_results=results)

    get_report_1_result_item_0 = [item[0] for item in get_report_1_result_data]

    report_output_format__report_output = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import re
    import json
    
    note = (
            "| Observable | Valid From | Confidence Score | Attributes | Related Observables | Tags | Properties |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
    
    phantom.debug(str(get_report_1_result_item_0))
    report = str(get_report_1_result_item_0)
    indicators = []
    indicators = re.findall(r"indicators\"\:(.*?)\}\'", report)
    phantom.debug(indicators)
    for item in indicators:
        phantom.debug("item")
        phantom.debug(item)
        phantom.debug(type(item))
        related = json.loads(item)
        for values in related:
            phantom.debug(type(values))
            observable = values['observable']
            phantom.debug(observable)
            validFrom = values['validFrom']
            phantom.debug(validFrom)
            confidenceScore = values['confidenceScore']
            phantom.debug(confidenceScore)
            attributes = values['attributes']
            phantom.debug(attributes)
            relatedObservables = values['relatedObservables']
            phantom.debug(relatedObservables)
            tags = values['tags']
            phantom.debug(tags)
            properties = values['properties']
            phantom.debug(properties)
            note += "|{}|{}|{}|{}|{}|{}|{}|\n".format(observable, validFrom, confidenceScore, attributes, relatedObservables, tags, properties)
        
        phantom.debug(note)
        report_output_format__report_output = note
        """item = item[1:-1]
        item = "'" + item + "'"
        item = '{"observable":{"value":"198.185.159.144","type":"IP4"},"validFrom":1695994622167,"confidenceScore":"HIGH","attributes":[],"relatedObservables":[{"entity":{"value":"ecoledesalsa.com","type":"DOMAIN"}},{"entity":{"value":"http://ecoledesalsa.com/cekmh","type":"URL"}}],"tags":["misp-object: object--fb7fc80a-fade-4482-bab8-cdc"],"properties":{}},{"observable":{"value":"ecoledesalsa.com","type":"DOMAIN"},"validFrom":1695994622167,"confidenceScore":"HIGH","attributes":[],"relatedObservables":[{"entity":{"value":"198.185.159.144","type":"IP4"}},{"entity":{"value":"http://ecoledesalsa.com/cekmh","type":"URL"}}],"tags":["misp-object: object--fb7fc80a-fade-4482-bab8-cdc"],"properties":{}},{"observable":{"value":"http://ecoledesalsa.com/cekmh","type":"URL"},"validFrom":1695994622167,"confidenceScore":"HIGH","attributes":[],"relatedObservables":[{"entity":{"value":"198.185.159.144","type":"IP4"}},{"entity":{"value":"ecoledesalsa.com","type":"DOMAIN"}}],"tags":["misp-object: object--fb7fc80a-fade-4482-bab8-cdc"],"properties":{}}'
        phantom.debug("newitem")
        phantom.debug(item)
        data  = json.loads(item)
        phantom.debug("data")
        phantom.debug(data)
        phantom.debug(data['observable'])
        validfrom = data['validFrom']
        phantom.debug(validfrom)
        
        #values = item.split(',')
        #for parameters in values:
        #    phantom.debug(parameters)
    
    
    array = '{"fruits": ["apple", "banana", "orange"]}'
    data2  = json.loads(array)
    fruits_list = data2['fruits']
    phantom.debug(fruits_list)
    
    
    #indicators = get_report_1_result_item_0['indicators']
    #phantom.debug(indicators)"""

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="report_output_format:report_output", value=json.dumps(report_output_format__report_output))

    trustar_report_details(container=container)

    return


@phantom.playbook_block()
def indicator_reputation_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_reputation_format() called")

    filtered_result_0_data_enrich_indicator = phantom.collect2(container=container, datapath=["filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.parameter.indicator_value","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.observable.type","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.priorityScore","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.submissionTags","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.attributes","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.safelisted","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.scoreContexts.*.sourceName","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.data.*.enclaveGuid","filtered-data:enrich_indicator:condition_2:indicator_reputation_1:action_result.summary.indicators_found"])

    filtered_result_0_parameter_indicator_value = [item[0] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___observable_type = [item[1] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___priorityscore = [item[2] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___submissiontags = [item[3] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___attributes = [item[4] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___safelisted = [item[5] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___scorecontexts___sourcename = [item[6] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___enclaveguid = [item[7] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_summary_indicators_found = [item[8] for item in filtered_result_0_data_enrich_indicator]

    indicator_reputation_format__indicator_reputation_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import urllib.parse
    
    note = (
            "| Indicator | Type | Priority Score | Submission Tags | Attributes | Safe Listed? | Sources | Enclave ID |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
    if filtered_result_0_summary_indicators_found != 0:
        for item in filtered_result_0_data_enrich_indicator:
            # for the first column, use the indicator as the text and the trustar query as the href
            trustar_link = 'https://station.trustar.co/browse/search?q={}'.format(urllib.parse.quote(item[0]))
            indicator_markdown = '[{}]({})'.format(item[0], trustar_link)
            indicator_type = item[1]
            priority = item[2]
            if item[3]:
                submission_tags = json.dumps(item[3]).replace('[', '').replace(']', '')
            else:
                submission_tags = "None"
            if item[4]:
                attributes = json.dumps(item[4]).replace('{', '').replace('}', '').replace('[', '').replace(']', '')
            else:
                attributes = "None"
            safe_listed = item[5]
            sources = item[6]
            enclaveGuid = item[7]
            note += "|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(indicator_markdown, indicator_type, priority, submission_tags, attributes, safe_listed, sources, enclaveGuid)
    else:
        note += "|{}|Not found in TruSTAR||||||\n".format(item[0])
    
    indicator_reputation_format__indicator_reputation_note = note
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="indicator_reputation_format:indicator_reputation_note", value=json.dumps(indicator_reputation_format__indicator_reputation_note))

    indicator_reputation_details(container=container)

    return


@phantom.playbook_block()
def indicator_summary_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_summary_format() called")

    filtered_result_0_data_enrich_indicator = phantom.collect2(container=container, datapath=["filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.value","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.type","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.description","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.enclaveId","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.reportId","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.score.name","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.score.value","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.data.*.source.name","filtered-data:enrich_indicator:condition_3:get_indicator_summary_1:action_result.summary.indicator_summaries"])

    filtered_result_0_data___value = [item[0] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___type = [item[1] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___description = [item[2] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___enclaveid = [item[3] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___reportid = [item[4] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___score_name = [item[5] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___score_value = [item[6] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_data___source_name = [item[7] for item in filtered_result_0_data_enrich_indicator]
    filtered_result_0_summary_indicator_summaries = [item[8] for item in filtered_result_0_data_enrich_indicator]

    indicator_summary_format__indicator_summary_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import urllib.parse
    
    note = (
            "| Indicator | Type | Description | Source | Category | Score | Enclave ID | Report ID |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
    if filtered_result_0_summary_indicator_summaries != 0:
        for item in filtered_result_0_data_enrich_indicator:
            trustar_link = 'https://station.trustar.co/browse/search?q={}'.format(urllib.parse.quote(item[0]))
            indicator_markdown = '[{}]({})'.format(item[0], trustar_link)
            indicator_type = item[1]
            description = item[2]
            enclaveid = item[3]
            reportid = item[4]
            score_name = item[5]
            score_value = item[6]
            source = item[7]
            #attributes = json.dumps(item[4]).replace('{', '').replace('}', '').replace('[', '').replace(']', '')
            note += "|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(indicator_markdown, indicator_type, description, source, score_name, score_value, enclaveid, reportid)
    else:
        note += "|{}|Not found in TruSTAR||||||\n".format(item[0])
    
    indicator_summary_format__indicator_summary_note = note
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="indicator_summary_format:indicator_summary_note", value=json.dumps(indicator_summary_format__indicator_summary_note))

    indicator_summary_details(container=container)

    return


@phantom.playbook_block()
def enrich_indicator(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("enrich_indicator() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["hunt_ip_1:action_result.data.*.report_id", "!=", ""]
        ],
        name="enrich_indicator:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        get_report_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["indicator_reputation_1:action_result.summary.indicators_found", "!=", 0]
        ],
        name="enrich_indicator:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        indicator_reputation_format(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids and results for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        conditions=[
            ["get_indicator_summary_1:action_result.status", "==", "success"]
        ],
        name="enrich_indicator:condition_3",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        indicator_summary_format(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    return


@phantom.playbook_block()
def indicator_summary_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_summary_details() called")

    template = """# Indicator Summary:\n\n{0}\n"""

    # parameter list for template variable replacement
    parameters = [
        "indicator_summary_format:custom_function:indicator_summary_note"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="indicator_summary_details")

    join_create_output(container=container)

    return


@phantom.playbook_block()
def indicator_reputation_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("indicator_reputation_details() called")

    template = """# Indicator reputation details\n\n{0}\n"""

    # parameter list for template variable replacement
    parameters = [
        "indicator_reputation_format:custom_function:indicator_reputation_note"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="indicator_reputation_details")

    join_create_output(container=container)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    create_output__output_note = json.loads(_ if (_ := phantom.get_run_data(key="create_output:output_note")) != "" else "null")  # pylint: disable=used-before-assignment

    output = {
        "note_title": ["TruSTAR Indicator Enrichment"],
        "note_content": create_output__output_note,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return