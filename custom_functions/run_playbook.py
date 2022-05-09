def run_playbook(container_list=None, playbook_name=None, scope=None, scope_list=None, **kwargs):
    """
    Run the specified playbook on the given containers
    
    Args:
        container_list: A list of container I
        playbook_name: Name of the playbook to run
        scope: Scope of the playbook execution - should be "all" or "new"
        scope_list: A list of artifact IDs to run the playbook against
    
    Returns a JSON-serializable object that implements the configured data paths:
        status: The status of the action, success or failed
        message: Status message
        total_success: Number of successful playbook executions
        playbook_run_ids: A list of playbook run IDs for the successful executions
        failure_list: A list of JSON objects with the container ID and error message
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Setup variables
    num_success = 0
    num_failed = 0
    run_ids = []
    failure_list = []
    
    for item in container_list[0]:
        container = phantom.get_container(item)
        if not container:
            num_failed += 1
            fail_item = {
                "containerid": item,
                "message": f"No container with ID {item} found"
            }
            failure_list.append(fail_item)
            continue
        container_id = container['id']
        runUrl = phantom.build_phantom_rest_url("playbook_run")
        if scope:
            # Scope set to string
            params = {
                "container_id": container_id,
                "playbook_id": playbook_name,
                "scope": scope,
                "run": True
            }
        elif scope_list:
            # Scope set to list of integers
            params = {
                "container_id": container_id,
                "playbook_id": playbook_name,
                "scope": scope_list,
                "run": True
            }
        else:
            # No scope provided so default to "new"
            params = {
                "container_id": container_id,
                "playbook_id": playbook_name,
                "scope": "new",
                "run": True
            }
        phantom.debug(f'Making a HTTP POST request to {runUrl} with parameters: {params}')
        response = phantom.requests.post(runUrl, json=params, verify=False)
        phantom.debug(f'Phantom returned status code: {response.status_code} and content: {response.text}')
        if response.status_code == phantom.requests.codes.ok:
            responseJSON = response.json()
            run_id = responseJSON['playbook_run_id']
            run_ids.append(run_id)
            num_success += 1
        else:
            num_failed += 1
            fail_item = {
                "containerid": item,
                "message": response.text
            }
            failure_list.append(fail_item)
            
    if num_failed > 0:
        message = f'One or more playbook executions failed to run. Success: {num_success} Failed: {num_failed}'
        status = 'failure'
    else:
        message = f'Successfully ran playbook on {num_success} containers.'
        status = 'success'
    outputs = {
        "status": status,
        "message": message,
        "total_success": num_success,
        "playbook_run_ids": run_ids,
        "failure_list": failure_list
    }
    phantom.debug(f'Function completed with output: {outputs}')
        
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
