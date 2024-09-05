from flask import request

def get_event_type():
    return request.headers.get('X-GitHub-Event')

def get_push_action_object():
    request_json = request.get_json()
    object = {
        "request_id": request_json['head_commit']['id'],
        "author": request_json['head_commit']['author']['name'],
        "action": "PUSH",
        "from_branch": request_json['ref'].split('/')[-1],
        "to_branch": request_json['ref'].split('/')[-1],
        "timestamp": request_json['head_commit']['timestamp']
    }
    return object

def get_pull_action_object():
    object = {}
    return object

def get_merge_action_object():
    object = {}
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
        object = {
            "event": event
        }

    return object