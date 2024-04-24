"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_1' block
    filter_1(container=container)

    return

@phantom.playbook_block()
def normalise_user_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("normalise_user_list() called")

    playbook_input_user = phantom.collect2(container=container, datapath=["playbook_input:user"])
    playbook_input_src_user = phantom.collect2(container=container, datapath=["playbook_input:src_user"])

    playbook_input_user_values = [item[0] for item in playbook_input_user]
    playbook_input_src_user_values = [item[0] for item in playbook_input_src_user]

    normalise_user_list__user_list = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
        
    if playbook_input_user_values and playbook_input_src_user_values:
        normalise_user_list__user_list = playbook_input_user_values + playbook_input_src_user_values
    if not playbook_input_user_values and playbook_input_src_user_values:
        normalise_user_list__user_list = playbook_input_src_user_values
    if playbook_input_user_values and not playbook_input_src_user_values:
        normalise_user_list__user_list = playbook_input_user_values
    if not playbook_input_user_values and not playbook_input_src_user_values:
        normalise_user_list__user_list = None
    remove_list = ["unknown", "None", ""]
    normalise_user_list__user_list = [x for x in normalise_user_list__user_list if x not in remove_list]
    normalise_user_list__user_list = [i for i in normalise_user_list__user_list if i is not None]
        
    phantom.debug("before dedup user list")
    phantom.debug(normalise_user_list__user_list)
    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="normalise_user_list:user_list", value=json.dumps(normalise_user_list__user_list))

    dedup_users(container=container)

    return


@phantom.playbook_block()
def dedup_users(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("dedup_users() called")

    normalise_user_list__user_list = json.loads(_ if (_ := phantom.get_run_data(key="normalise_user_list:user_list")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    parameters.append({
        "input_list": normalise_user_list__user_list,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/list_deduplicate", parameters=parameters, name="dedup_users", callback=get_identity_details)

    return


@phantom.playbook_block()
def get_identity_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_identity_details() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    query_formatted_string = phantom.format(
        container=container,
        template="""| makeresults\n| eval user_input=\"{0}\" \n| rex mode=sed field=user_input \"s/aus\\\\\\//g\" \n| rex mode=sed field=user_input \"s/ //g\" \n| makemv delim=\",\" user_input \n| mvexpand user_input \n| dedup user_input\n| where user_input!=\"None\" OR user_input!=\"unknown\"\n| rename user_input as identity \n| lookup identity_lookup_expanded identity\n| table _time\tbunit\tcategory\tcim_entity_zone\temail\tendDate\tfirst\tidentity\tidentity_tag\tlast\tmanagedBy\tnick\tphone\tprefix\tpriority\tstartDate\tsuffix\ttable_format\tvalue\twatchlist\twork_city\twork_country\twork_lat\twork_long\n""",
        parameters=[
            "dedup_users:custom_function_result.data.*.item"
        ])

    dedup_users_data = phantom.collect2(container=container, datapath=["dedup_users:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'get_identity_details' call
    for dedup_users_data_item in dedup_users_data:
        if query_formatted_string is not None:
            parameters.append({
                "query": query_formatted_string,
                "command": "",
                "display": "identity_id,bunit,category,email,endDate,first,identity,identity_tag,last,managedBy,nick,phone,prefix,priority,startDate,suffix,watchlist,work_city,work_country,work_lat,work_long",
                "end_time": "now",
                "start_time": "-24h",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="get_identity_details", assets=["splunk"], callback=identity_details_tasknote)

    return


@phantom.playbook_block()
def identity_details_tasknote(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("identity_details_tasknote() called")

    get_identity_details_result_data = phantom.collect2(container=container, datapath=["get_identity_details:action_result.data.*.identity_id","get_identity_details:action_result.data.*.identity","get_identity_details:action_result.data.*.email","get_identity_details:action_result.data.*.first","get_identity_details:action_result.data.*.last","get_identity_details:action_result.data.*.nick","get_identity_details:action_result.data.*.bunit","get_identity_details:action_result.data.*.priority","get_identity_details:action_result.data.*.category","get_identity_details:action_result.data.*.identity_tag","get_identity_details:action_result.data.*.managedBy","get_identity_details:action_result.data.*.phone","get_identity_details:action_result.data.*.startDate","get_identity_details:action_result.data.*.endDate","get_identity_details:action_result.data.*.prefix","get_identity_details:action_result.data.*.suffix","get_identity_details:action_result.data.*.watchlist","get_identity_details:action_result.data.*.work_city","get_identity_details:action_result.data.*.work_country","get_identity_details:action_result.data.*.work_lat","get_identity_details:action_result.data.*.work_long"], action_results=results)

    get_identity_details_result_item_0 = [item[0] for item in get_identity_details_result_data]
    get_identity_details_result_item_1 = [item[1] for item in get_identity_details_result_data]
    get_identity_details_result_item_2 = [item[2] for item in get_identity_details_result_data]
    get_identity_details_result_item_3 = [item[3] for item in get_identity_details_result_data]
    get_identity_details_result_item_4 = [item[4] for item in get_identity_details_result_data]
    get_identity_details_result_item_5 = [item[5] for item in get_identity_details_result_data]
    get_identity_details_result_item_6 = [item[6] for item in get_identity_details_result_data]
    get_identity_details_result_item_7 = [item[7] for item in get_identity_details_result_data]
    get_identity_details_result_item_8 = [item[8] for item in get_identity_details_result_data]
    get_identity_details_result_item_9 = [item[9] for item in get_identity_details_result_data]
    get_identity_details_result_item_10 = [item[10] for item in get_identity_details_result_data]
    get_identity_details_result_item_11 = [item[11] for item in get_identity_details_result_data]
    get_identity_details_result_item_12 = [item[12] for item in get_identity_details_result_data]
    get_identity_details_result_item_13 = [item[13] for item in get_identity_details_result_data]
    get_identity_details_result_item_14 = [item[14] for item in get_identity_details_result_data]
    get_identity_details_result_item_15 = [item[15] for item in get_identity_details_result_data]
    get_identity_details_result_item_16 = [item[16] for item in get_identity_details_result_data]
    get_identity_details_result_item_17 = [item[17] for item in get_identity_details_result_data]
    get_identity_details_result_item_18 = [item[18] for item in get_identity_details_result_data]
    get_identity_details_result_item_19 = [item[19] for item in get_identity_details_result_data]
    get_identity_details_result_item_20 = [item[20] for item in get_identity_details_result_data]

    identity_details_tasknote__identity_note_content = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    #phantom.debug(get_identity_details_result_data)
    phantom.debug(get_identity_details_result_item_0)
    phantom.debug(get_identity_details_result_item_1)
    phantom.debug(type(get_identity_details_result_item_1))
    phantom.debug(get_identity_details_result_item_2)
    phantom.debug(get_identity_details_result_item_3)
    phantom.debug(get_identity_details_result_item_4)
    phantom.debug(get_identity_details_result_item_5)
    phantom.debug(get_identity_details_result_item_6)
    phantom.debug(get_identity_details_result_item_7)
    phantom.debug(get_identity_details_result_item_8)
    phantom.debug(get_identity_details_result_item_9)
    phantom.debug(get_identity_details_result_item_10)
    phantom.debug(get_identity_details_result_item_11)
    phantom.debug(get_identity_details_result_item_12)
    phantom.debug(get_identity_details_result_item_13)
    phantom.debug(get_identity_details_result_item_14)
    phantom.debug(get_identity_details_result_item_15)
    phantom.debug(get_identity_details_result_item_16)
    phantom.debug(get_identity_details_result_item_17)
    phantom.debug(get_identity_details_result_item_18)
    phantom.debug(get_identity_details_result_item_19)
    phantom.debug(get_identity_details_result_item_20)
    
    note = (
        "\n**Identity details**\n"
        "| identity_id | identity | email | first | last | nick | bunit | priority | category | identity_tag | managedBy | phone | startDate | endDate | prefix | suffix | watchlist | work_city | work_country | work_lat | work_long |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
    if get_identity_details_result_data:
        for i in range(len(get_identity_details_result_item_1)):
            identity_id = get_identity_details_result_item_0[i]
            identity = get_identity_details_result_item_1[i]
            email = get_identity_details_result_item_2[i]
            first = get_identity_details_result_item_3[i]
            last = get_identity_details_result_item_4[i]
            nick = get_identity_details_result_item_5[i]
            bunit = get_identity_details_result_item_6[i]
            priority = get_identity_details_result_item_7[i]
            category = get_identity_details_result_item_8[i]
            identity_tag = get_identity_details_result_item_9[i]
            managedBy = get_identity_details_result_item_10[i]
            phone = get_identity_details_result_item_11[i]
            startDate = get_identity_details_result_item_12[i]
            endDate = get_identity_details_result_item_13[i]
            prefix = get_identity_details_result_item_14[i]
            suffix = get_identity_details_result_item_15[i]
            watchlist = get_identity_details_result_item_16[i]
            work_city = get_identity_details_result_item_17[i]
            work_country = get_identity_details_result_item_18[i]
            work_lat = get_identity_details_result_item_19[i]
            work_long = get_identity_details_result_item_20[i]
            note += "|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(identity_id, identity, email, first, last, nick, bunit, priority, category, identity_tag, managedBy, phone, startDate, endDate, prefix, suffix, watchlist, work_city, work_country, work_lat, work_long)
    else:
        note += "|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|\n".format("No identities found", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        
    identity_details_tasknote__identity_note_content = note

    phantom.debug("identity task note")
    phantom.debug(identity_details_tasknote__identity_note_content)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="identity_details_tasknote:identity_note_content", value=json.dumps(identity_details_tasknote__identity_note_content))

    join_noop_9(container=container)

    return


@phantom.playbook_block()
def normalise_asset_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("normalise_asset_list() called")

    playbook_input_src = phantom.collect2(container=container, datapath=["playbook_input:src"])
    playbook_input_dest = phantom.collect2(container=container, datapath=["playbook_input:dest"])
    playbook_input_src_ip = phantom.collect2(container=container, datapath=["playbook_input:src_ip"])
    playbook_input_dest_hostname = phantom.collect2(container=container, datapath=["playbook_input:dest_hostname"])
    playbook_input_computername = phantom.collect2(container=container, datapath=["playbook_input:computername"])

    playbook_input_src_values = [item[0] for item in playbook_input_src]
    playbook_input_dest_values = [item[0] for item in playbook_input_dest]
    playbook_input_src_ip_values = [item[0] for item in playbook_input_src_ip]
    playbook_input_dest_hostname_values = [item[0] for item in playbook_input_dest_hostname]
    playbook_input_computername_values = [item[0] for item in playbook_input_computername]

    normalise_asset_list__asset_ip_list = None
    normalise_asset_list__asset_hostname_list = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    normalise_asset_list__asset_ip_list = playbook_input_src_values + playbook_input_dest_values + playbook_input_src_ip_values
    normalise_asset_list__asset_hostname_list = playbook_input_dest_hostname_values + playbook_input_computername_values
    
    remove_list = ["unknown", "None", ""]
    normalise_asset_list__asset_ip_list = [x for x in normalise_asset_list__asset_ip_list if x not in remove_list]
    normalise_asset_list__asset_ip_list = [x for x in normalise_asset_list__asset_ip_list if x is not None]
    normalise_asset_list__asset_hostname_list = [x for x in normalise_asset_list__asset_hostname_list if x not in remove_list]
    normalise_asset_list__asset_hostname_list = [x for x in normalise_asset_list__asset_hostname_list if x is not None]
    
        
    phantom.debug("before dedup asset list ip")
    phantom.debug(normalise_asset_list__asset_ip_list)
    
    phantom.debug("before dedup asset list hostname")
    phantom.debug(normalise_asset_list__asset_hostname_list)
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="normalise_asset_list:asset_ip_list", value=json.dumps(normalise_asset_list__asset_ip_list))
    phantom.save_run_data(key="normalise_asset_list:asset_hostname_list", value=json.dumps(normalise_asset_list__asset_hostname_list))

    dedup_asset_ip(container=container)

    return


@phantom.playbook_block()
def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_1() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="or",
        conditions=[
            ["playbook_input:user", "!=", None],
            ["playbook_input:src_user", "!=", None]
        ],
        name="filter_1:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        normalise_user_list(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        logical_operator="or",
        conditions=[
            ["playbook_input:src", "!=", None],
            ["playbook_input:dest", "!=", None],
            ["playbook_input:src_ip", "!=", None],
            ["playbook_input:dest_hostname", "!=", None],
            ["playbook_input:computername", "!=", None]
        ],
        name="filter_1:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        normalise_asset_list(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def dedup_asset_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("dedup_asset_ip() called")

    normalise_asset_list__asset_ip_list = json.loads(_ if (_ := phantom.get_run_data(key="normalise_asset_list:asset_ip_list")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    parameters.append({
        "input_list": normalise_asset_list__asset_ip_list,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/list_deduplicate", parameters=parameters, name="dedup_asset_ip", callback=dedup_asset_hostname)

    return


@phantom.playbook_block()
def dedup_asset_hostname(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("dedup_asset_hostname() called")

    normalise_asset_list__asset_hostname_list = json.loads(_ if (_ := phantom.get_run_data(key="normalise_asset_list:asset_hostname_list")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    parameters.append({
        "input_list": normalise_asset_list__asset_hostname_list,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/list_deduplicate", parameters=parameters, name="dedup_asset_hostname", callback=dedup_asset_hostname_callback)

    return


@phantom.playbook_block()
def dedup_asset_hostname_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("dedup_asset_hostname_callback() called")

    
    decision_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    code_7(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def asset_by_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("asset_by_ip() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    query_formatted_string = phantom.format(
        container=container,
        template="""| inputlookup append=T asset_lookup_by_str \n| inputlookup append=T asset_lookup_by_cidr \n| rename _key as asset_id,asset_tag as tag \n| search ip IN ({0})\n| table CrowdStrikeActive,DNSDomain,LastSeen_CStrike_epoch,LastSeen_Splunk_epoch,LastSeen_epoch,SplunkActive,asset,asset_id,category,city,dns,ip,is_expected,mac,nt_host,owner,pci_domain,priority,tag\n\n""",
        parameters=[
            "dedup_asset_ip:custom_function_result.data.*.item"
        ])

    dedup_asset_ip_data = phantom.collect2(container=container, datapath=["dedup_asset_ip:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'asset_by_ip' call
    for dedup_asset_ip_data_item in dedup_asset_ip_data:
        if query_formatted_string is not None:
            parameters.append({
                "query": query_formatted_string,
                "command": "",
                "display": "CrowdStrikeActive,DNSDomain,LastSeen_CStrike_epoch,LastSeen_Splunk_epoch,LastSeen_epoch,SplunkActive,asset,asset_id,category,city,dns,ip,is_expected,mac,nt_host,owner,pci_domain,priority,tag",
                "end_time": "now",
                "start_time": "-24h",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="asset_by_ip", assets=["splunk"], callback=join_asset_by_ip_tasknote)

    return


@phantom.playbook_block()
def asset_by_hostname(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("asset_by_hostname() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    query_formatted_string = phantom.format(
        container=container,
        template="""| inputlookup append=T asset_lookup_by_str \n| inputlookup append=T asset_lookup_by_cidr \n| rename _key as asset_id,asset_tag as tag \n| search nt_host IN ({0})\n| table CrowdStrikeActive,DNSDomain,LastSeen_CStrike_epoch,LastSeen_Splunk_epoch,LastSeen_epoch,SplunkActive,asset,asset_id,category,city,dns,ip,is_expected,mac,nt_host,owner,pci_domain,priority,tag\n\n\n""",
        parameters=[
            "dedup_asset_hostname:custom_function_result.data.*.item"
        ])

    dedup_asset_hostname_data = phantom.collect2(container=container, datapath=["dedup_asset_hostname:custom_function_result.data.*.item"])

    parameters = []

    # build parameters list for 'asset_by_hostname' call
    for dedup_asset_hostname_data_item in dedup_asset_hostname_data:
        if query_formatted_string is not None:
            parameters.append({
                "query": query_formatted_string,
                "command": "",
                "display": "CrowdStrikeActive,DNSDomain,LastSeen_CStrike_epoch,LastSeen_Splunk_epoch,LastSeen_epoch,SplunkActive,asset,asset_id,category,city,dns,ip,is_expected,mac,nt_host,owner,pci_domain,priority,tag",
                "end_time": "now",
                "start_time": "-24h",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="asset_by_hostname", assets=["splunk"], callback=join_asset_by_ip_tasknote)

    return


@phantom.playbook_block()
def join_asset_by_ip_tasknote(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_asset_by_ip_tasknote() called")

    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key="join_asset_by_ip_tasknote_called"):
        return

    # save the state that the joined function has now been called
    phantom.save_run_data(key="join_asset_by_ip_tasknote_called", value="asset_by_ip_tasknote")

    # call connected block "asset_by_ip_tasknote"
    asset_by_ip_tasknote(container=container, handle=handle)

    return


@phantom.playbook_block()
def asset_by_ip_tasknote(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("asset_by_ip_tasknote() called")

    asset_by_ip_result_data = phantom.collect2(container=container, datapath=["asset_by_ip:action_result.data.*.asset","asset_by_ip:action_result.data.*.asset_id","asset_by_ip:action_result.data.*.nt_host","asset_by_ip:action_result.data.*.ip","asset_by_ip:action_result.data.*.mac","asset_by_ip:action_result.data.*.category","asset_by_ip:action_result.data.*.priority","asset_by_ip:action_result.data.*.owner","asset_by_ip:action_result.data.*.city","asset_by_ip:action_result.data.*.DNSDomain","asset_by_ip:action_result.data.*.dns","asset_by_ip:action_result.data.*.tag","asset_by_ip:action_result.data.*.CrowdStrikeActive","asset_by_ip:action_result.data.*.LastSeen_CStrike_epoch","asset_by_ip:action_result.data.*.LastSeen_Splunk_epoch","asset_by_ip:action_result.data.*.LastSeen_epoch","asset_by_ip:action_result.data.*.SplunkActive","asset_by_ip:action_result.data.*.is_expected","asset_by_ip:action_result.data.*.pci_domain","asset_by_ip:action_result.status"], action_results=results)
    asset_by_hostname_result_data = phantom.collect2(container=container, datapath=["asset_by_hostname:action_result.data.*.asset","asset_by_hostname:action_result.data.*.asset_id","asset_by_hostname:action_result.data.*.nt_host","asset_by_hostname:action_result.data.*.ip","asset_by_hostname:action_result.data.*.mac","asset_by_hostname:action_result.data.*.category","asset_by_hostname:action_result.data.*.priority","asset_by_hostname:action_result.data.*.owner","asset_by_hostname:action_result.data.*.city","asset_by_hostname:action_result.data.*.DNSDomain","asset_by_hostname:action_result.data.*.dns","asset_by_hostname:action_result.data.*.tag","asset_by_hostname:action_result.data.*.CrowdStrikeActive","asset_by_hostname:action_result.data.*.LastSeen_CStrike_epoch","asset_by_hostname:action_result.data.*.LastSeen_Splunk_epoch","asset_by_hostname:action_result.data.*.LastSeen_epoch","asset_by_hostname:action_result.data.*.SplunkActive","asset_by_hostname:action_result.data.*.is_expected","asset_by_hostname:action_result.data.*.pci_domain","asset_by_hostname:action_result.status"], action_results=results)

    asset_by_ip_result_item_0 = [item[0] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_1 = [item[1] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_2 = [item[2] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_3 = [item[3] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_4 = [item[4] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_5 = [item[5] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_6 = [item[6] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_7 = [item[7] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_8 = [item[8] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_9 = [item[9] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_10 = [item[10] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_11 = [item[11] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_12 = [item[12] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_13 = [item[13] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_14 = [item[14] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_15 = [item[15] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_16 = [item[16] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_17 = [item[17] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_18 = [item[18] for item in asset_by_ip_result_data]
    asset_by_ip_result_item_19 = [item[19] for item in asset_by_ip_result_data]
    asset_by_hostname_result_item_0 = [item[0] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_1 = [item[1] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_2 = [item[2] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_3 = [item[3] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_4 = [item[4] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_5 = [item[5] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_6 = [item[6] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_7 = [item[7] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_8 = [item[8] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_9 = [item[9] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_10 = [item[10] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_11 = [item[11] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_12 = [item[12] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_13 = [item[13] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_14 = [item[14] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_15 = [item[15] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_16 = [item[16] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_17 = [item[17] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_18 = [item[18] for item in asset_by_hostname_result_data]
    asset_by_hostname_result_item_19 = [item[19] for item in asset_by_hostname_result_data]

    asset_by_ip_tasknote__asset_note_content = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug("asset_by_ip_result_data")
    phantom.debug(asset_by_ip_result_data)
    
    phantom.debug("asset_by_hostname_result_data")
    phantom.debug(asset_by_hostname_result_data)
    
    note = (
        "\n**Asset details**\n"
        "| asset | asset_id | nt_host | ip | mac | category | priority | owner | city | DNSDomain | dns | tag | CrowdStrikeActive | LastSeen_CStrike_epoch | LastSeen_Splunk_epoch | LastSeen_epoch | SplunkActive | is_expected | pci_domain |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )
    note1 = ""
    note2 = ""
    for i in range(len(asset_by_ip_result_item_0)):
        asset = asset_by_ip_result_item_0[i]
        asset_id = asset_by_ip_result_item_1[i]
        nt_host = asset_by_ip_result_item_2[i]
        ip = asset_by_ip_result_item_3[i]
        mac = asset_by_ip_result_item_4[i]
        category = asset_by_ip_result_item_5[i]
        priority = asset_by_ip_result_item_6[i]
        owner = asset_by_ip_result_item_7[i]
        city = asset_by_ip_result_item_8[i]
        DNSDomain = asset_by_ip_result_item_9[i]
        dns = asset_by_ip_result_item_10[i]
        tag = asset_by_ip_result_item_11[i]
        CrowdStrikeActive = asset_by_ip_result_item_12[i]
        LastSeen_CStrike_epoch = asset_by_ip_result_item_13[i]
        LastSeen_Splunk_epoch = asset_by_ip_result_item_14[i]
        LastSeen_epoch = asset_by_ip_result_item_15[i]
        SplunkActive = asset_by_ip_result_item_16[i]
        is_expected = asset_by_ip_result_item_17[i]
        pci_domain = asset_by_ip_result_item_18[i]
        note1 += "|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(asset, asset_id, nt_host, ip, mac, category, priority, owner, city, DNSDomain, dns, tag, CrowdStrikeActive, LastSeen_CStrike_epoch, LastSeen_Splunk_epoch, LastSeen_epoch, SplunkActive, is_expected, pci_domain)
    
    asset_by_ip_tasknote__asset_note_content_1 = note1  
    
    for i in range(len(asset_by_hostname_result_item_0)):
        asset = asset_by_hostname_result_item_0[i]
        asset_id = asset_by_hostname_result_item_1[i]
        nt_host = asset_by_hostname_result_item_2[i]
        ip = asset_by_hostname_result_item_3[i]
        mac = asset_by_hostname_result_item_4[i]
        category = asset_by_hostname_result_item_5[i]
        priority = asset_by_hostname_result_item_6[i]
        owner = asset_by_hostname_result_item_7[i]
        city = asset_by_hostname_result_item_8[i]
        DNSDomain = asset_by_hostname_result_item_9[i]
        dns = asset_by_hostname_result_item_10[i]
        tag = asset_by_hostname_result_item_11[i]
        CrowdStrikeActive = asset_by_hostname_result_item_12[i]
        LastSeen_CStrike_epoch = asset_by_hostname_result_item_13[i]
        LastSeen_Splunk_epoch = asset_by_hostname_result_item_14[i]
        LastSeen_epoch = asset_by_hostname_result_item_15[i]
        SplunkActive = asset_by_hostname_result_item_16[i]
        is_expected = asset_by_hostname_result_item_17[i]
        pci_domain = asset_by_hostname_result_item_18[i]
        note2 += "|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|\n".format(asset, asset_id, nt_host, ip, mac, category, priority, owner, city, DNSDomain, dns, tag, CrowdStrikeActive, LastSeen_CStrike_epoch, LastSeen_Splunk_epoch, LastSeen_epoch, SplunkActive, is_expected, pci_domain)
        
    asset_by_ip_tasknote__asset_note_content_2 = note2
    
    phantom.debug("asset_by_ip_tasknote__asset_note_content_1")
    phantom.debug(asset_by_ip_tasknote__asset_note_content_1)
    phantom.debug("asset_by_ip_tasknote__asset_note_content_2")
    phantom.debug(asset_by_ip_tasknote__asset_note_content_2)
                
    asset_by_ip_tasknote__asset_note_content = note + asset_by_ip_tasknote__asset_note_content_1 + asset_by_ip_tasknote__asset_note_content_2
    
    phantom.debug("asset_by_ip_tasknote__asset_note_content")
    phantom.debug(asset_by_ip_tasknote__asset_note_content)

    phantom.debug("asset task note")
    phantom.debug(asset_by_ip_tasknote__asset_note_content)
    
    
    phantom.debug("asset details")
    phantom.debug(asset_by_ip_result_item_0)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="asset_by_ip_tasknote:asset_note_content", value=json.dumps(asset_by_ip_tasknote__asset_note_content))

    join_noop_9(container=container)

    return


@phantom.playbook_block()
def join_noop_9(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_noop_9() called")

    if phantom.completed(action_names=["get_identity_details", "asset_by_ip", "asset_by_hostname"]):
        # call connected block "noop_9"
        noop_9(container=container, handle=handle)

    return


@phantom.playbook_block()
def noop_9(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("noop_9() called")

    parameters = [{}]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/noop", parameters=parameters, name="noop_9")

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["dedup_asset_ip:custom_function_result.data.*.item", "!=", None]
        ],
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        asset_by_ip(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        conditions=[
            ["dedup_asset_hostname:custom_function_result.data.*.item", "!=", None]
        ],
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        asset_by_hostname(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def code_7(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("code_7() called")

    dedup_asset_ip_data = phantom.collect2(container=container, datapath=["dedup_asset_ip:custom_function_result.data.*.item"])
    dedup_asset_hostname_data = phantom.collect2(container=container, datapath=["dedup_asset_hostname:custom_function_result.data.*.item"])

    dedup_asset_ip_data___item = [item[0] for item in dedup_asset_ip_data]
    dedup_asset_hostname_data___item = [item[0] for item in dedup_asset_hostname_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug("after dedup ip list")
    phantom.debug(dedup_asset_ip_data)
    phantom.debug("after dedup hostname list")
    phantom.debug(dedup_asset_hostname_data)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    identity_details_tasknote__identity_note_content = json.loads(_ if (_ := phantom.get_run_data(key="identity_details_tasknote:identity_note_content")) != "" else "null")  # pylint: disable=used-before-assignment
    asset_by_ip_tasknote__asset_note_content = json.loads(_ if (_ := phantom.get_run_data(key="asset_by_ip_tasknote:asset_note_content")) != "" else "null")  # pylint: disable=used-before-assignment

    output = {
        "task_note_identity": identity_details_tasknote__identity_note_content,
        "task_note_assets": asset_by_ip_tasknote__asset_note_content,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    phantom.debug(identity_details_tasknote__identity_note_content)
    phantom.debug(asset_by_ip_tasknote__asset_note_content)
    
    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return