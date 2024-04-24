"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'regex_split_1' block
    regex_split_1(container=container)

    return

@phantom.playbook_block()
def regex_split_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("regex_split_1() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.emailHeaders.From","artifact:*.id"])

    parameters = []

    # build parameters list for 'regex_split_1' call
    for container_artifact_item in container_artifact_data:
        parameters.append({
            "regex": "\\s\\<",
            "input_string": container_artifact_item[0],
            "strip_whitespace": True,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/regex_split", parameters=parameters, name="regex_split_1", callback=debug_2)

    return


@phantom.playbook_block()
def debug_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_2() called")

    regex_split_1__result = phantom.collect2(container=container, datapath=["regex_split_1:custom_function_result.data.0.item"])

    regex_split_1_data_0_item = [item[0] for item in regex_split_1__result]

    parameters = []

    parameters.append({
        "input_1": regex_split_1_data_0_item,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_2", callback=send_htmlemail_1)

    return


@phantom.playbook_block()
def send_htmlemail_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_htmlemail_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    html_body_formatted_string = phantom.format(
        container=container,
        template="""Hello {0}\n""",
        parameters=[
            "regex_split_1:custom_function_result.data.0.item"
        ])

    regex_split_1__result = phantom.collect2(container=container, datapath=["regex_split_1:custom_function_result.data.0.item"])

    parameters = []

    # build parameters list for 'send_htmlemail_1' call
    for regex_split_1__result_item in regex_split_1__result:
        if html_body_formatted_string is not None:
            parameters.append({
                "to": "fwinata@splunk.com",
                "from": "splunksoarpoc@gmail.com",
                "subject": "testing",
                "html_body": html_body_formatted_string,
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