"""
asd
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_2' block
    filter_2(container=container)

    return

@phantom.playbook_block()
def add_ip_listitem(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_ip_listitem() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceAddress","artifact:*.id"])
    ip_custom_list_format = phantom.get_format_data(name="ip_custom_list_format")

    parameters = []

    # build parameters list for 'add_ip_listitem' call
    for container_artifact_item in container_artifact_data:
        if ip_custom_list_format is not None and container_artifact_item[0] is not None:
            parameters.append({
                "list": ip_custom_list_format,
                "create": True,
                "new_row": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add listitem", parameters=parameters, name="add_ip_listitem", assets=["soar_poc_phantom"], callback=spl_search_put_to_lookup_local_ip_soar_poc)

    return


@phantom.playbook_block()
def ip_custom_list_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ip_custom_list_format() called")

    template = """IP Artifacts """

    # parameter list for template variable replacement
    parameters = [
        "container:start_time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="ip_custom_list_format")

    add_ip_listitem(container=container)

    return


@phantom.playbook_block()
def domain_list_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("domain_list_format() called")

    template = """Domain Artifacts\n"""

    # parameter list for template variable replacement
    parameters = [
        "container:start_time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="domain_list_format")

    add_domain_listitem(container=container)

    return


@phantom.playbook_block()
def add_domain_listitem(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_domain_listitem() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.destinationDnsDomain","artifact:*.id"])
    domain_list_format = phantom.get_format_data(name="domain_list_format")

    parameters = []

    # build parameters list for 'add_domain_listitem' call
    for container_artifact_item in container_artifact_data:
        if domain_list_format is not None and container_artifact_item[0] is not None:
            parameters.append({
                "list": domain_list_format,
                "create": True,
                "new_row": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add listitem", parameters=parameters, name="add_domain_listitem", assets=["soar_poc_phantom"], callback=spl_search_put_to_lookup_local_domain_soar_poc)

    return


@phantom.playbook_block()
def md5_list_format(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("md5_list_format() called")

    template = """MD5 Hash Artifacts """

    # parameter list for template variable replacement
    parameters = [
        "container:start_time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="md5_list_format")

    add_md5_listitem(container=container)

    return


@phantom.playbook_block()
def add_md5_listitem(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_md5_listitem() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.fileHash","artifact:*.id"])
    md5_list_format = phantom.get_format_data(name="md5_list_format")

    parameters = []

    # build parameters list for 'add_md5_listitem' call
    for container_artifact_item in container_artifact_data:
        if md5_list_format is not None and container_artifact_item[0] is not None:
            parameters.append({
                "list": md5_list_format,
                "create": True,
                "new_row": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add listitem", parameters=parameters, name="add_md5_listitem", assets=["soar_poc_phantom"], callback=spl_search_put_to_lookup_local_md5_soar_poc)

    return


@phantom.playbook_block()
def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_2() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "IP Artifact"],
            ["artifact:*.description", "==", "Artifact added by Parser"]
        ],
        name="filter_2:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        ip_custom_list_format(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Domain Artifact"],
            ["artifact:*.description", "==", "Artifact added by Parser"]
        ],
        name="filter_2:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        domain_list_format(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    # collect filtered artifact ids and results for 'if' condition 3
    matched_artifacts_3, matched_results_3 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["artifact:*.name", "==", "Hash Artifact"],
            ["artifact:*.description", "==", "Artifact added by Parser"]
        ],
        name="filter_2:condition_3",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_3 or matched_results_3:
        md5_list_format(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_3, filtered_results=matched_results_3)

    return


@phantom.playbook_block()
def spl_search_put_to_lookup_local_ip_soar_poc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("spl_search_put_to_lookup_local_ip_soar_poc() called")

    template = """%%\n|makeresults | eval ip= \"{0}\", threat_key=\"ip\" | table ip threat_key | inputlookup  local_ip_soar_poc.csv append=true | dedup ip threat_key | outputlookup local_ip_soar_poc  \n%%"""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.sourceAddress"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="spl_search_put_to_lookup_local_ip_soar_poc", drop_none=True)

    add_to_lookup_local_ip_soar_poc(container=container)

    return


@phantom.playbook_block()
def add_to_lookup_local_ip_soar_poc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_to_lookup_local_ip_soar_poc() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    spl_search_put_to_lookup_local_ip_soar_poc__as_list = phantom.get_format_data(name="spl_search_put_to_lookup_local_ip_soar_poc__as_list")

    parameters = []

    # build parameters list for 'add_to_lookup_local_ip_soar_poc' call
    for spl_search_put_to_lookup_local_ip_soar_poc__item in spl_search_put_to_lookup_local_ip_soar_poc__as_list:
        if spl_search_put_to_lookup_local_ip_soar_poc__item is not None:
            parameters.append({
                "query": spl_search_put_to_lookup_local_ip_soar_poc__item,
                "command": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="add_to_lookup_local_ip_soar_poc", assets=["splunk"], callback=join_noop_1)

    return


@phantom.playbook_block()
def spl_search_put_to_lookup_local_domain_soar_poc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("spl_search_put_to_lookup_local_domain_soar_poc() called")

    template = """%%\n|makeresults | eval domain= \"{0}\", threat_key=\"domain\" | table domain threat_key | inputlookup  local_domain_soar_poc.csv append=true | dedup domain threat_key | outputlookup local_domain_soar_poc  \n%%"""

    # parameter list for template variable replacement
    parameters = [
        "add_domain_listitem:action_result.parameter.new_row"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="spl_search_put_to_lookup_local_domain_soar_poc", drop_none=True)

    add_to_lookup_local_domain_soar_poc(container=container)

    return


@phantom.playbook_block()
def add_to_lookup_local_domain_soar_poc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_to_lookup_local_domain_soar_poc() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    spl_search_put_to_lookup_local_domain_soar_poc__as_list = phantom.get_format_data(name="spl_search_put_to_lookup_local_domain_soar_poc__as_list")

    parameters = []

    # build parameters list for 'add_to_lookup_local_domain_soar_poc' call
    for spl_search_put_to_lookup_local_domain_soar_poc__item in spl_search_put_to_lookup_local_domain_soar_poc__as_list:
        if spl_search_put_to_lookup_local_domain_soar_poc__item is not None:
            parameters.append({
                "query": spl_search_put_to_lookup_local_domain_soar_poc__item,
                "command": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="add_to_lookup_local_domain_soar_poc", assets=["splunk"], callback=join_noop_1)

    return


@phantom.playbook_block()
def spl_search_put_to_lookup_local_md5_soar_poc(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("spl_search_put_to_lookup_local_md5_soar_poc() called")

    template = """%%\n|makeresults | eval md5= \"{0}\", threat_key=\"md5\" | table md5 threat_key | inputlookup  local_md5_soar_poc.csv append=true | dedup md5 threat_key | outputlookup local_md5_soar_poc  \n%%"""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.fileHash"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="spl_search_put_to_lookup_local_md5_soar_poc", drop_none=True)

    run_query_3(container=container)

    return


@phantom.playbook_block()
def run_query_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("run_query_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    spl_search_put_to_lookup_local_md5_soar_poc__as_list = phantom.get_format_data(name="spl_search_put_to_lookup_local_md5_soar_poc__as_list")

    parameters = []

    # build parameters list for 'run_query_3' call
    for spl_search_put_to_lookup_local_md5_soar_poc__item in spl_search_put_to_lookup_local_md5_soar_poc__as_list:
        if spl_search_put_to_lookup_local_md5_soar_poc__item is not None:
            parameters.append({
                "query": spl_search_put_to_lookup_local_md5_soar_poc__item,
                "command": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="run_query_3", assets=["splunk"], callback=join_noop_1)

    return


@phantom.playbook_block()
def join_noop_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_noop_1() called")

    if phantom.completed(action_names=["add_to_lookup_local_ip_soar_poc", "add_to_lookup_local_domain_soar_poc", "run_query_3"]):
        # call connected block "noop_1"
        noop_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def noop_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("noop_1() called")

    parameters = [{}]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/noop", parameters=parameters, name="noop_1")

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