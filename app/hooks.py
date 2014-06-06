hooks = {}

def add(hook_type, fn):
    """Adds a hook of the specified type."""
    if hook_type in hooks:
        hooks[hook_type].append(fn)
    else:
        hooks[hook_type] = [fn]


def run(hook_type, *args, **kwargs):
    """Runs a hook of the specified type, with the specified arguments.
    Returns whatever was returned by the last hook which didn't return None"""
    if hook_type not in hooks:
        pass
    else:
        retval = None
        
        for hook in hooks[hook_type]:
            new_retval = hook(*args, **kwargs)
            if retval is not None:
                retval = new_retval

    return retval

class add_hook:
    """A decorator class for adding a hook."""
    def __init__(self, hook_type):
        self.hook_type = hook_type
        
    def __call__(self, fn):
        add(self.hook_type, fn)
        return fn
