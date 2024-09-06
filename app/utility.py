from flask import request
import datetime

def get_event_type():
    '''Function to get the github-event-type, extracted from headers / request-body'''

    # get the header event
    github_event = request.headers.get('X-GitHub-Event')
    # get the request body object
    pull_action = request.get_json()
    
    # basic return conditions
    if github_event == "push":
        return github_event
    
    if github_event != "pull_request":
        return "invalid"
    
    if pull_action['action'] == 'opened':
        return "pull"
    
    elif pull_action['pull_request']['merged_by'] is not None:
        # action is merge if merged-by exists
        return "merge"

    else:
        return "invalid"

def get_push_action_object():
    request_json = request.get_json()
    return {
        "request_id": request_json['head_commit']['id'],
        "author": request_json['head_commit']['author']['username'],
        "action": "PUSH",
        "from_branch": request_json['ref'].split('/')[-1],
        "to_branch": request_json['ref'].split('/')[-1],
        "timestamp": request_json['head_commit']['timestamp']
    }

def get_pull_action_object():
    request_json = request.get_json()
    return {
        "request_id": str(request_json['pull_request']['id']),
        "author": request_json['pull_request']['user']['login'],
        "action": "PULL_REQUEST",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "timestamp": request_json['pull_request']['created_at']
    }

def get_merge_action_object():
    request_json = request.get_json()
    return {
        "request_id": str(request_json['pull_request']['id']),
        "author": request_json['pull_request']['merged_by']['login'],
        "action": "MERGE",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "timestamp": request_json['pull_request']['merged_at']
    }

def get_action_object():
    '''Function to get the action-object (minmized), extracted from github-webhook-request-body'''
    
    # extract the event-type
    event = get_event_type()
    
    # get the action-object based on event-type
    if event == "push":
        action_object = get_push_action_object()

    elif event == "pull":
        action_object= get_pull_action_object()
    
    elif event == "merge":
        action_object = get_merge_action_object()
    
    else:
        raise Exception("Invalid event type")

    # make the timestamp standard (in utc)
    action_object['timestamp'] = datetime.datetime.fromisoformat(action_object['timestamp']).astimezone(datetime.timezone.utc)
    return action_object