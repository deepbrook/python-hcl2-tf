# noqa: D400,D415
"""# Terraform HCL2 Dialect Loader

Loads Terraform configuration files written in HCL2 and wrangles them into expected shapes,
making them easier to access during further processing.

"""
__version__ = "0.1.0"

from typing import Mapping

import hcl2

from hcl2tf import compact
from hcl2tf.utils import BLOCK_TYPES, AddressableDict


def _compact(config: Mapping) -> Mapping:
    for block_type in BLOCK_TYPES:
        compactor_func = getattr(compact, f"compact_{block_type}_block_array")
        config[block_type] = compactor_func(config)
    return AddressableDict(config)


def load(*args, **kwargs) -> Mapping:
    """Load HCL2 configuration from a file pointer and compact the result.

    Any `args` and `kwargs` are passed through directly to :func:`hcl2.load`.
    """
    config = hcl2.load(*args, **kwargs)
    return _compact(config)


def loads(*args, **kwargs) -> Mapping:
    """Load HCL2 configuration from a string and compact the result.

    Any `args` and `kwargs` are passed through directly to :func:`hcl2.loads`.
    """
    config = hcl2.loads(*args, **kwargs)
    return _compact(config)
