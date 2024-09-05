from flask import request

def get_event_type():
    '''Function to get the github-event-type, extracted from headers / request-body'''

    # get the header event
    github_event = request.headers.get('X-GitHub-Event')
    
    # basic return conditions
    if github_event == "push":
        return github_event
    
    if github_event != "pull_request":
        return "invalid"
    
    pull_action = request.get_json()

    if pull_action['action'] == 'opened':
        return "pull"
    
    elif pull_action['pull_request']['merged_by'] is not None:
        # action is merge if merged-by exists
        return "merge"

    else:
        return "invalid"

def get_push_action_object():
    request_json = request.get_json()
    object = {
        "request_id": request_json['head_commit']['id'],
        "author": request_json['head_commit']['author']['username'],
        "action": "PUSH",
        "from_branch": request_json['ref'].split('/')[-1],
        "to_branch": request_json['ref'].split('/')[-1],
        "timestamp": request_json['head_commit']['timestamp']
    }
    return object

def get_pull_action_object():
    request_json = request.get_json()
    object = {
        "request_id": request_json['pull_request']['id'],
        "author": request_json['pull_request']['user']['login'],
        "action": "PULL_REQUEST",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "timestamp": request_json['pull_request']['created_at']
    }
    return object

def get_merge_action_object():
    request_json = request.get_json()
    object = {
        "request_id": request_json['pull_request']['id'],
        "author": request_json['pull_request']['merged_by']['login'],
        "action": "MERGE",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "timestamp": request_json['pull_request']['merged_at']
    }
    return object

def get_action_object():
    '''Function to get the action-object (minmized), extracted from github-webhook-request-body'''
    
    # extract the event-type
    event = get_event_type()
    
    # get the action-object based on event-type
    if event == "push":
        object = get_push_action_object()

    elif event == "pull":
        object= get_pull_action_object()
    
    elif event == "merge":
        object = get_merge_action_object()
    
    else:
        raise Exception("Invalid event type")

    return object