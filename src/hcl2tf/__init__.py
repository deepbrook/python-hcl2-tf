"""# Terraform HCL2 Dialect Loader

Loads Terraform configuration files written in HCL2 and wrangles them into expected shapes,
making them easier to access during further processing.

"""
__version__ = "0.1.0"

import hcl2

from hcl2tf import compact


def _compact(config):
    for block_type in (
        "resource",
        "data",
        "variable",
        "output",
        "module",
        "provider",
        "terraform",
        "import",
        "moved",
        "check",
    ):
        compactor_func = getattr(compact, f"compact_{block_type}_block_array")
        config[block_type] = compactor_func(config[block_type])
    return config


def load(*args, **kwargs):
    config = hcl2.load(*args, **kwargs)
    return _compact(config)


def loads(*args, **kwargs):
    config = hcl2.loads(*args, **kwargs)
    return _compact(config)
