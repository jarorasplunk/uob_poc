"""
Accepts a URL or vault_id and does detonation analysis on the objects. Generates a global report and a per observable sub-report and normalized score. The score can be customized based on a variety of factors.\n\n
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'saa_input_filter' block
    saa_input_filter(container=container)

    return

@phantom.playbook_block()
def saa_input_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("saa_input_filter() called")

    ################################################################################
    # Determine branches based on provided inputs.
    ################################################################################

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["playbook_input:vault_id", "!=", ""]
        ],
        name="saa_input_filter:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        file_detonation(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def detonation_status_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("detonation_status_filter() called")

    ################################################################################
    # Filters successful file  detonation results.
    ################################################################################

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["file_detonation:action_result.status", "==", "success"]
        ],
        name="detonation_status_filter:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        get_file_summary_output(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def file_detonation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("file_detonation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Queries SAA for information about the provided vault_id(s)
    ################################################################################

    filtered_input_0_vault_id = phantom.collect2(container=container, datapath=["filtered-data:saa_input_filter:condition_1:playbook_input:vault_id"])

    parameters = []

    # build parameters list for 'file_detonation' call
    for filtered_input_0_vault_id_item in filtered_input_0_vault_id:
        if filtered_input_0_vault_id_item[0] is not None:
            parameters.append({
                "file": filtered_input_0_vault_id_item[0],
                "user_agent": "Default",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("detonate file", parameters=parameters, name="file_detonation", assets=["saa_uob_poc"], callback=detonation_status_filter)

    return


@phantom.playbook_block()
def loop_get_file_summary_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("loop_get_file_summary_output() called")

    loop_state = phantom.LoopState(state=loop_state_json)

    if loop_state.should_continue(container=container, results=results): # should_continue evaluates iteration/timeout/conditions
        loop_state.increment() # increments iteration count
        get_file_summary_output(container=container, loop_state_json=loop_state.to_json())
    else:
        get_job_forensics_1(container=container)

    return


@phantom.playbook_block()
def get_file_summary_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_file_summary_output() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Queries SAA Forensics data relative to the JobID of URL(s) or File(s) needs 
    # to be detonated.
    ################################################################################

    filtered_result_0_data_detonation_status_filter = phantom.collect2(container=container, datapath=["filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.data.*.JobID"])

    parameters = []

    # build parameters list for 'get_file_summary_output' call
    for filtered_result_0_item_detonation_status_filter in filtered_result_0_data_detonation_status_filter:
        if filtered_result_0_item_detonation_status_filter[0] is not None:
            parameters.append({
                "job_id": filtered_result_0_item_detonation_status_filter[0],
                "timeout": "",
            })

    if not loop_state_json:
        # Loop state is empty. We are creating a new one from the inputs
        loop_state_json = {
            # Looping configs
            "current_iteration": 1,
            "max_iterations": 15,
            "conditions": [
                ["get_file_summary_output:action_result.data.*.State", "==", "done"]
            ],
            "max_ttl": 1800,
            "delay_time": 120,
        }

    # Load state from the JSON passed to it
    loop_state = phantom.LoopState(state=loop_state_json)

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    #parameters = []
    #for job_ids in file_jobid_detonation_output__jobid:
    #    for job in job_ids:
    #        if job is not None:
    #            parameters.append({
    #                "job_id": job,
    #                "timeout": 5,
    #            })
    #phantom.debug(parameters)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get job summary", parameters=parameters, name="get_file_summary_output", assets=["saa_uob_poc"], callback=loop_get_file_summary_output, loop_state=loop_state.to_json())

    return


@phantom.playbook_block()
def normalized_file_summary_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("normalized_file_summary_output() called")

    ################################################################################
    # This block uses custom code for normalizing score. Adjust the logic as desired 
    # in the documented sections.
    ################################################################################

    filtered_result_0_data_detonation_status_filter = phantom.collect2(container=container, datapath=["filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.parameter.file","filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.data.*.JobID"])
    filtered_result_1_data_file_summary_filter = phantom.collect2(container=container, datapath=["filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.parameter.job_id","filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.data.*.Submission.Name","filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.summary.Score","filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.data.*.Resources","filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.data.*.Verdict","filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.data.*.Tasks"])

    filtered_result_0_parameter_file = [item[0] for item in filtered_result_0_data_detonation_status_filter]
    filtered_result_0_data___jobid = [item[1] for item in filtered_result_0_data_detonation_status_filter]
    filtered_result_1_parameter_job_id = [item[0] for item in filtered_result_1_data_file_summary_filter]
    filtered_result_1_data___submission_name = [item[1] for item in filtered_result_1_data_file_summary_filter]
    filtered_result_1_summary_score = [item[2] for item in filtered_result_1_data_file_summary_filter]
    filtered_result_1_data___resources = [item[3] for item in filtered_result_1_data_file_summary_filter]
    filtered_result_1_data___verdict = [item[4] for item in filtered_result_1_data_file_summary_filter]
    filtered_result_1_data___tasks = [item[5] for item in filtered_result_1_data_file_summary_filter]

    normalized_file_summary_output__file_score_object = None
    normalized_file_summary_output__scores = None
    normalized_file_summary_output__categories = None
    normalized_file_summary_output__score_id = None
    normalized_file_summary_output__file = None
    normalized_file_summary_output__job_id = None
    normalized_file_summary_output__classifications = None
    normalized_file_summary_output__file_name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    
    score_table = {
        "0":"Unknown",
        "1":"Very_Safe",
        "2":"Safe",
        "3":"Probably_Safe",
        "4":"Leans_Safe",
        "5":"May_not_be_Safe",
        "6":"Exercise_Caution",
        "7":"Suspicious_or_Risky",
        "8":"Possibly_Malicious",
        "9":"Probably_Malicious",
        "10":"Malicious"
    }

    classification_ids = {
        "Unknown": 0,
        "Adware": 1,
        "Backdoor": 2,
        "Bot": 3,
        "Bootkit": 4,
        "DDOS": 5,
        "Downloader": 6,
        "Dropper": 7,
        "Exploit-Kit": 8,
        "Keylogger": 9,
        "Ransomware": 10,
        "Remote-Access-Trojan": 11,
        "Resource-Exploitation": 13,
        "Rogue-Security-Software": 14,
        "Rootkit": 15,
        "Screen-Capture": 16,
        "Spyware": 17,
        "Trojan": 18,
        "Virus": 19,
        "Webshell": 20,
        "Wiper": 21,
        "Worm": 22,
        "Other": 99
    }

    normalized_file_summary_output__file_score_object = []
    normalized_file_summary_output__scores = []
    normalized_file_summary_output__categories = []
    normalized_file_summary_output__score_id = []
    normalized_file_summary_output__file = []
    normalized_file_summary_output__job_id = []
    normalized_file_summary_output__classifications = []
    normalized_file_summary_output__file_name = []
    
    
    def find_sha1_details(target_id, task_list):
        '''
        Attempt to find the detail object with a sha1
        '''
        for task in task_list:
            if (target_id == task.get('ResourceID')
                and task.get('Results',{}).get('Details', {}).get('sha1')):
                task_result_details = task['Results']['Details']
                task_result_details.pop('RootTaskID', None)
                return task_result_details
        return None

        
    ## pair forensic job results with url detonated
    job_file_dict = {}
    for orig_file, orig_job, filtered_job in zip(filtered_result_0_parameter_file, filtered_result_0_data___jobid, filtered_result_1_parameter_job_id):
        if orig_job == filtered_job:
            job_file_dict[filtered_job] = orig_file
    
    for job, file_name, score_num, resources, verdict, tasks in zip(
        filtered_result_1_parameter_job_id, 
        filtered_result_1_data___submission_name, 
        filtered_result_1_summary_score, 
        filtered_result_1_data___resources, 
        filtered_result_1_data___verdict,
        filtered_result_1_data___tasks
    ):
        
        ## translate scores
        score_id = int(score_num/10) if score_num > 0 else 0
        score = score_table[str(score_id)]
        file = job_file_dict[job]
        attributes = {}
        
        ## build.a sub dictionary of high priority related observables
        related_observables = []
        for sub_observ in resources:
            if sub_observ['Name'] != file_name:
                        
                details = find_sha1_details(sub_observ['ID'], tasks)
                second_num = sub_observ['DisplayScore']
                second_num_id = int(second_num/10) if second_num > 0 else 0
                sub_observ_dict = {
                    'value': sub_observ['Name'],
                    'type': sub_observ['Type'].lower(),
                    'reputation': {
                        'score': score_table[str(second_num_id)],
                        'orig_score': second_num,
                        'score_id': second_num_id
                    },
                    'source': 'Splunk Attack Analyzer'
                }
                if details:
                    details['name'] = sub_observ['Name']
                    details.pop('exiftool', None)
                    sub_observ_dict['attributes'] = details
                # check if observ is already in related_observables
                skip_observ = False
                for idx, item in enumerate(related_observables):
                    if (sub_observ.get('FileMetadata', {}).get('SHA256', 'null_one') 
                        == item.get('attributes', {}).get('sha256', 'null_two')
                        and sub_observ['DisplayScore'] > item['reputation']['orig_score']):
                        related_observables[idx] = sub_observ_dict
                        skip_observ = True
                    elif sub_observ['Name'] == item['value']:
                        skip_observ = True
                if not skip_observ:
                    related_observables.append(sub_observ_dict)
            elif sub_observ['Name'] == file_name:
                details = find_sha1_details(sub_observ['ID'], tasks)
                if details:
                    details.pop('exiftool', None)
                    details['name'] = file_name
                    attributes = details
                else:
                    file_metadata = sub_observ.get('FileMetadata', {})
                    attributes = {
                        'name': file_name,
                        'sha256': file_metadata.get('SHA256'),
                        'md5': file_metadata.get('MD5'),
                        'size': file_metadata.get('Size')
                    }
                    if file_metadata.get('MimeType'):
                        attributes['mime_type'] = file_metadata['MimeType']
        
        normalized_file_summary_output__file_score_object.append({
            'value': file, 
            'orig_score': score_num, 
            'score': score, 
            'score_id': score_id, 
            'classifications': [verdict if verdict else "Unknown"],
            'classification_ids': [classification_ids.get(verdict, 99) if verdict else 0],
            'related_observables': related_observables,
            'attributes': attributes
                
        })
        normalized_file_summary_output__scores.append(score)
        normalized_file_summary_output__score_id.append(score_id)
        normalized_file_summary_output__file.append(file)
        normalized_file_summary_output__file_name.append(file_name)
        normalized_file_summary_output__job_id.append(job)
        normalized_file_summary_output__classifications.append([verdict if verdict else "Unknown"])
    
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="normalized_file_summary_output:file_score_object", value=json.dumps(normalized_file_summary_output__file_score_object))
    phantom.save_run_data(key="normalized_file_summary_output:scores", value=json.dumps(normalized_file_summary_output__scores))
    phantom.save_run_data(key="normalized_file_summary_output:categories", value=json.dumps(normalized_file_summary_output__categories))
    phantom.save_run_data(key="normalized_file_summary_output:score_id", value=json.dumps(normalized_file_summary_output__score_id))
    phantom.save_run_data(key="normalized_file_summary_output:file", value=json.dumps(normalized_file_summary_output__file))
    phantom.save_run_data(key="normalized_file_summary_output:job_id", value=json.dumps(normalized_file_summary_output__job_id))
    phantom.save_run_data(key="normalized_file_summary_output:classifications", value=json.dumps(normalized_file_summary_output__classifications))
    phantom.save_run_data(key="normalized_file_summary_output:file_name", value=json.dumps(normalized_file_summary_output__file_name))

    join_format_file_report(container=container)

    return


@phantom.playbook_block()
def join_format_file_report(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_format_file_report() called")

    if phantom.completed(action_names=["get_file_job_screenshots"]):
        # call connected block "format_file_report"
        format_file_report(container=container, handle=handle)

    return


@phantom.playbook_block()
def format_file_report(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_file_report() called")

    ################################################################################
    # Format a summary table with the information gathered from the playbook.
    ################################################################################

    template = """SOAR analyzed File(s) using Splunk Attack Analyzer.  The table below shows a summary of the information gathered.\n\n| File Name | Normalized Score | Score Id  | Classifications | Report Link | Source |\n| --- | --- | --- | --- | --- | --- |\n%%\n| `{0}` | {1} | {2} | {3} | {6} | Splunk Attack Analyzer (SAA) |\n%%\n\nScreenshots associated with the detonated Files are shown below (if available):\n\n{5}\n\n"""

    # parameter list for template variable replacement
    parameters = [
        "normalized_file_summary_output:custom_function:file_name",
        "normalized_file_summary_output:custom_function:scores",
        "normalized_file_summary_output:custom_function:score_id",
        "normalized_file_summary_output:custom_function:classifications",
        "normalized_file_summary_output:custom_function:job_id",
        "file_screenshot_formatting:custom_function:report",
        "get_file_summary_output:action_result.summary.AppURL"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    #phantom.debug(phantom.format(container=container, template=template, parameters=parameters, name="format_report_file"))
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_file_report", drop_none=True)

    format_file_report_no_screenshot(container=container)

    return


@phantom.playbook_block()
def build_file_output(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("build_file_output() called")

    ################################################################################
    # This block uses custom code to generate an observable dictionary to output into 
    # the observables data path.
    ################################################################################

    get_file_summary_output_result_data = phantom.collect2(container=container, datapath=["get_file_summary_output:action_result.summary.AppURL"], action_results=results)
    normalized_file_summary_output__file = json.loads(_ if (_ := phantom.get_run_data(key="normalized_file_summary_output:file")) != "" else "null")  # pylint: disable=used-before-assignment
    normalized_file_summary_output__job_id = json.loads(_ if (_ := phantom.get_run_data(key="normalized_file_summary_output:job_id")) != "" else "null")  # pylint: disable=used-before-assignment
    normalized_file_summary_output__file_score_object = json.loads(_ if (_ := phantom.get_run_data(key="normalized_file_summary_output:file_score_object")) != "" else "null")  # pylint: disable=used-before-assignment

    get_file_summary_output_summary_appurl = [item[0] for item in get_file_summary_output_result_data]

    build_file_output__observable_array = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    build_file_output__observable_array = []
    for _vault_id, external_id, file_object, app_url in zip(normalized_file_summary_output__file, normalized_file_summary_output__job_id, normalized_file_summary_output__file_score_object, get_file_summary_output_summary_appurl):
        #phantom.debug("vault: {} id: {}".format(_vault_id, external_id))
        observable_object = {
            "value": _vault_id,
            "type": "hash",
            "attributes": file_object['attributes'],
            "reputation": {
                "orig_score": file_object['orig_score'],
                "score": file_object['score'],
                "score_id": file_object['score_id']
            },
            "malware": {
                "classifications": file_object['classifications'],
                "classification_ids": file_object['classification_ids']
            },
            "source": "Splunk Attack Analyzer",
            "source_link":f"{app_url}"
        }
        if file_object.get('related_observables'):
            observable_object["related_observables"] = file_object['related_observables']
            
        build_file_output__observable_array.append(observable_object)
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="build_file_output:observable_array", value=json.dumps(build_file_output__observable_array))

    return


@phantom.playbook_block()
def file_summary_filter(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("file_summary_filter() called")

    ################################################################################
    # Filters successful file detonation job forensic results.
    ################################################################################

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["get_file_summary_output:action_result.status", "==", "success"]
        ],
        name="file_summary_filter:condition_1",
        delimiter=",")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        get_file_job_screenshots(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def get_file_job_screenshots(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_file_job_screenshots() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Add the job screenshots to the vault
    ################################################################################

    filtered_result_0_data_file_summary_filter = phantom.collect2(container=container, datapath=["filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.parameter.job_id"])

    parameters = []

    # build parameters list for 'get_file_job_screenshots' call
    for filtered_result_0_item_file_summary_filter in filtered_result_0_data_file_summary_filter:
        if filtered_result_0_item_file_summary_filter[0] is not None:
            parameters.append({
                "job_id": filtered_result_0_item_file_summary_filter[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get job screenshots", parameters=parameters, name="get_file_job_screenshots", assets=["saa_uob_poc"], callback=get_file_job_screenshots_callback)

    return


@phantom.playbook_block()
def get_file_job_screenshots_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_file_job_screenshots_callback() called")

    
    normalized_file_summary_output(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    file_screenshot_formatting(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def file_screenshot_formatting(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("file_screenshot_formatting() called")

    ################################################################################
    # Custom formatting for the markdown report that shows screenshots grouped by 
    # detonated file.
    ################################################################################

    filtered_result_0_data_detonation_status_filter = phantom.collect2(container=container, datapath=["filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.parameter.file","filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.data.*.JobID"])
    get_file_job_screenshots_result_data = phantom.collect2(container=container, datapath=["get_file_job_screenshots:action_result.parameter.job_id","get_file_job_screenshots:action_result.data.*.file_name","get_file_job_screenshots:action_result.data.*.id"], action_results=results)

    filtered_result_0_parameter_file = [item[0] for item in filtered_result_0_data_detonation_status_filter]
    filtered_result_0_data___jobid = [item[1] for item in filtered_result_0_data_detonation_status_filter]
    get_file_job_screenshots_parameter_job_id = [item[0] for item in get_file_job_screenshots_result_data]
    get_file_job_screenshots_result_item_1 = [item[1] for item in get_file_job_screenshots_result_data]
    get_file_job_screenshots_result_item_2 = [item[2] for item in get_file_job_screenshots_result_data]

    file_screenshot_formatting__report = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    file_screenshot_formatting__report = ""
    
    for file, job_id in zip(filtered_result_0_parameter_file, filtered_result_0_data___jobid):
        file_screenshot_formatting__report += f"#### {file}\n"
        for screenshot_job, screenshot_name, screenshot_id in zip(get_file_job_screenshots_parameter_job_id, get_file_job_screenshots_result_item_1, get_file_job_screenshots_result_item_2):
            if job_id == screenshot_job:
                file_screenshot_formatting__report += f"![{screenshot_name}](/view?id={screenshot_id})\n"

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="file_screenshot_formatting:report", value=json.dumps(file_screenshot_formatting__report))

    join_format_file_report(container=container)

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    get_file_summary_output_result_data = phantom.collect2(container=container, datapath=["get_file_summary_output:action_result.data.*.Tasks.*.Results.Details.Headers","get_file_summary_output:action_result.parameter.context.artifact_id"], action_results=results)

    get_file_summary_output_result_item_0 = [item[0] for item in get_file_summary_output_result_data]

    parameters = []

    parameters.append({
        "input_1": get_file_summary_output_result_item_0,
        "input_2": None,
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

    return


@phantom.playbook_block()
def get_job_forensics_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_job_forensics_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_detonation_status_filter = phantom.collect2(container=container, datapath=["filtered-data:detonation_status_filter:condition_1:file_detonation:action_result.data.*.JobID"])

    parameters = []

    # build parameters list for 'get_job_forensics_1' call
    for filtered_result_0_item_detonation_status_filter in filtered_result_0_data_detonation_status_filter:
        if filtered_result_0_item_detonation_status_filter[0] is not None:
            parameters.append({
                "job_id": filtered_result_0_item_detonation_status_filter[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get job forensics", parameters=parameters, name="get_job_forensics_1", assets=["saa_uob_poc"], callback=format_whois_note)

    return


@phantom.playbook_block()
def format_whois_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_whois_note() called")

    get_job_forensics_1_result_data = phantom.collect2(container=container, datapath=["get_job_forensics_1:action_result.data.*.WhoisResults"], action_results=results)

    get_job_forensics_1_result_item_0 = [item[0] for item in get_job_forensics_1_result_data]

    format_whois_note__whois_format_note = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    import json
    
    #phantom.debug(get_job_forensics_1_result_item_0)
    whois_data_json = get_job_forensics_1_result_item_0[0][0]
    phantom.debug(whois_data_json)
    phantom.debug(whois_data_json['Emails'])
    note = (
        "| Key | Value |\n"
        "| :--- | :--- |\n"
    )

    note += "|{}|{}|\n".format("DomainName", whois_data_json['DomainName'])
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
    note += "|{}|{}|\n".format("NameServers", whois_data_json['NameServers'])
    note += "|{}|{}|\n".format("WhoisServer", whois_data_json['WhoisServer'])

    
    format_whois_note__whois_format_note = note

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="format_whois_note:whois_format_note", value=json.dumps(format_whois_note__whois_format_note))

    file_summary_filter(container=container)

    return


@phantom.playbook_block()
def format_file_report_no_screenshot(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_file_report_no_screenshot() called")

    template = """SOAR analyzed File(s) using Splunk Attack Analyzer.  The table below shows a summary of the information gathered.\n\n| File Name | Normalized Score | Score Id  | Classifications | Report Link | Source |\n| --- | --- | --- | --- | --- | --- |\n%%\n| `{0}` | {1} | {2} | {3} | {4} | Splunk Attack Analyzer (SAA) |\n%%\n"""

    # parameter list for template variable replacement
    parameters = [
        "normalized_file_summary_output:custom_function:file_name",
        "normalized_file_summary_output:custom_function:scores",
        "normalized_file_summary_output:custom_function:score_id",
        "normalized_file_summary_output:custom_function:classifications",
        "get_file_summary_output:action_result.summary.AppURL"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_file_report_no_screenshot")

    build_file_output(container=container)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    filtered_result_0_data_file_summary_filter = phantom.collect2(container=container, datapath=["filtered-data:file_summary_filter:condition_1:get_file_summary_output:action_result.data.*.Verdict"])
    format_url_report = phantom.get_format_data(name="format_url_report")
    format_file_report = phantom.get_format_data(name="format_file_report")
    format_file_report_no_screenshot = phantom.get_format_data(name="format_file_report_no_screenshot")
    build_url_output__observable_array = json.loads(_ if (_ := phantom.get_run_data(key="build_url_output:observable_array")) != "" else "null")  # pylint: disable=used-before-assignment
    build_file_output__observable_array = json.loads(_ if (_ := phantom.get_run_data(key="build_file_output:observable_array")) != "" else "null")  # pylint: disable=used-before-assignment
    format_whois_note__whois_format_note = json.loads(_ if (_ := phantom.get_run_data(key="format_whois_note:whois_format_note")) != "" else "null")  # pylint: disable=used-before-assignment

    filtered_result_0_data___verdict = [item[0] for item in filtered_result_0_data_file_summary_filter]

    observable_combined_value = phantom.concatenate(build_url_output__observable_array, build_file_output__observable_array)
    report_combined_value = phantom.concatenate(format_url_report, format_file_report)

    output = {
        "observable": observable_combined_value,
        "report": report_combined_value,
        "verdict": filtered_result_0_data___verdict,
        "whois_note": format_whois_note__whois_format_note,
        "analysis_summary_only": format_file_report_no_screenshot,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    #phantom.debug(output)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return