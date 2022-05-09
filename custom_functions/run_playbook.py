def run_playbook(container_list=None, playbook_name=None, scope=None, scope_list=None, container=None, **kwargs):
    """
    Run the specified playbook on the given container(s).  You can use either the single value "container" or the list option "container_list" for multiple containers.  The scope parameter can be "all" or "new".  If not supplied then "new" will be assumed.
    
    Args:
        container_list: A list of container I
        playbook_name: Name of the playbook to run
        scope: Scope of the playbook execution - should be "all" or "new"
        scope_list: A list of artifact IDs to run the playbook against
        container (CEF type: phantom container id): Single container ID
    
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
    
    # Input Validation
    
    if not container and not container_list:
        outputs = {
            "status": "failed",
            "message": "Must provide a container or container list"
        }
        phantom.debug(f'No container(s) provided, output: {outputs}')
        return outputs
    
    if scope:
        # Scope set to string
        scope_param = scope
    elif scope_list:
        # Scope set to list of integers
        scope_param = scope_list
    else:
        # No scope provided so default to "new"
        scope_param = "new"
    
    # Setup variables
    num_success = 0
    num_failed = 0
    run_ids = []
    failure_list = []
    
    if container:
        # Single container ID provided
        container = phantom.get_container(container)
        if not container:
            num_failed += 1
            fail_item = {
                "containerid": container,
                "message": f"No container with ID {container} found"
            }
            failure_list.append(fail_item)
        runUrl = phantom.build_phantom_rest_url("playbook_run")
        params = {
            "container_id": container,
            "playbook_id": playbook_name,
            "scope": scope_param,
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
                "containerid": container,
                "message": response.text
            }
            failure_list.append(fail_item)
    
    if container_list:
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
            params = {
                "container_id": container_id,
                "playbook_id": playbook_name,
                "scope": scope_param,
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
