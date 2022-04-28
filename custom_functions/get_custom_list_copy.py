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
    success, message, list_data = phantom.get_list(list_name=list_name)
    
    if not success:
        phantom.debug(f'Failed to get decided_list.  Response from server: {message}')
        outputs = {
            "list_of_items": [],
            "status": "failure",
            "message": message
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
