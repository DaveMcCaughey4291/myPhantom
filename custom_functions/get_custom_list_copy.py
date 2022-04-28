def get_custom_list_copy(list_name=None, **kwargs):
    """
    This custom function retrieves the elements of a custom list.
    
    Args:
        list_name: Name of the custom list
    
    Returns a JSON-serializable object that implements the configured data paths:
        status: Outcome of action
        message: Message returned by the action
        list_of_items: A list of the elements from the custom list
    """
    ############################ Custom Code Goes Below This Line #################################
    import json
    import phantom.rules as phantom
    
    outputs = {}
    
    # Prepare list
    list_of_items = []
    
    # Build url to get custom list ID
    url = phantom.build_phantom_rest_url('decided_list')
    # Build parameters
    params = [('_filter_name__icontains', "\""+list_name+"\"")]
    
    phantom.debug(params)
    
    response = phantom.requests.get(url, params=params, verify=False)
    
    phantom.debug(response.text)
    
    # Try and parse the response
    try:
        data = response.json['data'][0]
        
        custom_list_id = data['id']
        
    except Exception as e:
        phantom.debug(f'Failed to get decided_list.  Response from server: {e}')
        outputs = {
            "list_of_items": [],
            "status": "failure",
            "message": str(e)
        }
        return outputs
        
    # Get custom list contents
    
    # Build URL to get contents
    url = phantom.build_phantom_rest_url('decided_list', custom_list_id)
    # Build params
    params = [
        (
            "page_size", 0
        )
    ]
    
    phantom.debug(params)
    
    response = phantom.requests.get(url, params=params, verify=False)
    phantom.debug(response.text)
    
    # Parse the response
    try:
        list_data = response.json['content']
        
    except Exception as e:
        phantom.debug(f'Failed to get list contents.  Response from server: {e}')
        outputs = {
            "list_of_items": [],
            "status": "failed",
            "message": str(e)
        }
        return outputs
        
    # Remove blank or null entries from list
    
    for custom_list_items in list_data:
        for item in custom_list_items:
            if (item != "" and item is not None):
                # if element is not blank or null then add to list
                list_of_items.append(item)
                
    phantom.debug(f'List of items: {list_of_items}')
    
    # Setup outputs
    outputs = {
        "list_of_items": list_of_items,
        "status": "success",
        "message": f"Found {len(list_of_items)} items"
    }
    
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs
