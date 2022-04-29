def run_playbook(container_list=None, playbook_name=None, **kwargs):
    """
    Run the specified playbook on the given containers
    
    Args:
        container_list: A list of container IDs
        playbook_name: Name of the playbook to run
    
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
    
    for item in container_list:
        success, message, run_id = phantom.playbook(playbook=playbook_name, container = item)
        if success:
            run_ids.append(run_id)
            num_success += 1
        else:
            num_failed += 1
            fail_item = {
                "containerid": item,
                "message": message
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
        
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
