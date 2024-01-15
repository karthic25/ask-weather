def check_param_empty(params, key):
    if key in params and len(params[key]) != 0:
        return False
    return True

def check_param_none(params, key):
    if key in params and params[key] is not None:
        return False
    return True

