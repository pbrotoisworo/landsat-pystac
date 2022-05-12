from landsatpystac.errors import TypeError

def check_if_string(val):
    """
    Helper function to check if a value is a string or not.

    Parameters
    ----------
    val
        Input object to check if it is a string or not.

    Returns
    -------
    bool
        True if it is a string. False if it is not a string.
    
    """
    if isinstance(val, str):
        return True
    else:
        raise TypeError(f'Input value "{val}" is not a string type.')

def check_if_int(val):
    """
    Helper function to check if a value is an integer or not.

    Parameters
    ----------
    val
        Input object to check if it is an integer or not.

    Returns
    -------
    bool
        True if it is an int. False if it is not an int.
    """
    if isinstance(val, int):
        return True
    else:
        raise TypeError(f'Input value "{val}" is not an integer type.')