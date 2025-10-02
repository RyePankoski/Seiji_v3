def has_val_at_key(dictionary, key):
    """
    Return True only if key exists in dictionary AND its value is not None or [].
    """
    return key in dictionary and dictionary[key] not in (None, [])
