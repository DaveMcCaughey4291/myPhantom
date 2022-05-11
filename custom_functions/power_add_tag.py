def power_add_tag(tag_list=None, container_id=None, container_list=None, **kwargs):
    """
    Allows adding multiple tags to a container or containers.  If no container(s) are provided then the current container is assumed.
    
    Args:
        tag_list: A mandatory list of tag strings
        container_id (CEF type: phantom container id): An optional ID of another container
        container_list: An optional list of container IDs
    
    Returns a JSON-serializable object that implements the configured data paths:
        status: The result of the custom function -success or failure
        message: Result message from the custom function
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Input validation
    if not tag_list:
        phantom.debug('No tag list supplied')
        outputs = {
            "status": "failure",
            "message": "Custom function failed - no tag list provided"
        }
        return outputs
    
    success_count = 0
    failure_count = 0
    
    if container_id:
        # Single other container ID provided
        phantom.debug(f'Adding tags "{tag_list}" to container {container_id}')
        success, message = phantom.add_tags(tags=tag_list, container=container_id)
        if success:
            success_count += 1
        else:
            failure_count += 1
            phantom.debug(f'Failed to add tags to container {container_id}.  Message from Phantom: {message}')
    elif container_list:
        # List of container IDs provided
        phantom.debug(f'Adding tags "{tag_list}" to containers: {container_list}')
        for container in container_list:
            success, message = phantom.add_tags(tags=tag_list, container=container)
            if success:
                success_count += 1
            else:
                failure_count += 1
                phantom.debug(f'Failed to add tags to container {container}.  Message from Phantom: {message}')
    else:
        # No conainer supplied - assuming current container
        phantom.debug(f'Adding tags "{tag_list}" to current container')
        success, message = phantom.add_tags(tags=tag_list)
        if success:
            success_count += 1
        else:
            failure_count += 1
            phantom.debug(f'Failed to add tags to current container.  Message from Phantom: {message}')
            
    if not success or failure_count > 0:
        status = "failure"
        message = f'Failed to add tags to one or more containers.  See previous debug messages for details. Success: {success_count} Failed: {failure_count}'
    else:
        status = "success"
        message = f'Successfully added all tags to {success_count} containers'
        
    outputs['status'] = status
    outputs['message'] = message
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
