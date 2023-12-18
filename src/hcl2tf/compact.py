from collections import defaultdict


def _compact_type_label_label_block_array(array: list) -> dict:
    """Compact list of blocks with a `type "label" "label" {}` signature."""
    compacted = defaultdict(dict)
    for definition in array:
        assert len(definition.keys()) == 1

        kind, *_ = definition.keys()
        children = definition[kind]

        name, *_ = children.keys()
        block_definition = dict(**children[name])

        compacted[kind][name] = block_definition

    return dict(**compacted)


def _compact_type_label_block_array(array: list):
    """Compact list of blocks with a `type "label" {}` signature."""
    compacted = defaultdict(dict)
    for definition in array:
        assert len(definition.keys()) == 1

        name, *_ = definition.keys()
        block_definition = definition[name]

        compacted[name] = block_definition
    return dict(**compacted)


def _compact_type_block_array(array: list) -> dict:
    """Compact list of blocks with a `type {}` signature."""

    # Could do: {k: v for d in array for k,v in d.items()}
    # ..but that'll gain us bragging rights and not readabilty.
    compacted = {}
    for d in array:
        compacted.update(d)
    return compacted


def _compact_lifecycle_block_array(block_definition):
    """Compact a block's `lifecycle` array.
    
    This is a simple replace operation if the `lifecycle` key is present in the
    given `block_definition`. 

    Lifecycle blocks may only be declared *once*, allowing us the simple conversion
     of :mod:`hcl2`'s parser result of a single-item list of dicts to a dict. 
    """
    if "lifecycle" in block_definition:
        block_definition["lifecycle"] = block_definition["lifecycle"][0]
    return block_definition


def _compact_type_label_label_block_array_with_lifecycle(config, block_type):
    """Compact the lifecycle array of `type  "label" "label" {}` block definitions found in `config`."""
    compacted = _compact_type_label_label_block_array(config.get(block_type, []))  # Compact
    for first_label, first_definition_array in compacted.items():  # Select dict of block definitions filed under the first label
        for second_label, block_definition in first_definition_array.items():  # Select block definitions filed under second label 
            compacted[first_label][second_label] = _compact_lifecycle_block_array(block_definition)
    return compacted


def compact_resource_block_array(config):
    return _compact_type_label_label_block_array_with_lifecycle(config, "resource")


def compact_data_block_array(config):
    return _compact_type_label_label_block_array_with_lifecycle(config, "data")


def _compact_type_label_block_array_with_lifecycle(config, block_type):
    """Compact the lifecycle array of `type "label" {}` block definitions found in `config`."""
    compacted = _compact_type_label_block_array(config.get(block_type, []))
    for label, block_definition in compacted.items():
        compacted[label] = _compact_lifecycle_block_array(block_definition)
    return compacted


def compact_output_block_array(config):
    return _compact_type_label_block_array_with_lifecycle(config, "output")


def compact_variable_block_array(config):
    return _compact_type_label_block_array_with_lifecycle(config, "variable")


def compact_module_block_array(config):
    return _compact_type_label_block_array_with_lifecycle(config, "module")


def compact_provider_block_array(config):
    return _compact_type_label_block_array_with_lifecycle(config, "provider")


def compact_check_block_array(config):
    initial = _compact_type_label_block_array(config.get("check", []))
    compacted = {}
    for check, config in initial.items():
        if "data" in config:
            config["data"] = _compact_type_label_label_block_array(config["data"])
        compacted[check] = config
    return compacted


def compact_moved_block_array(config):
    compacted = {}
    for block in config.get("moved", []):
        compacted[block["to"]] = block["from"]
    return compacted


def compact_import_block_array(config):
    compacted = {}
    for block in config.get("import", []):
        compacted[block["to"]] = block["id"]
    return compacted


def compact_terraform_block_array(config):
    compacted = _compact_type_block_array(config["terraform"])

    if "required_providers" in compacted:
        compacted["required_providers"] = _compact_type_block_array(
            compacted["required_providers"]
        )
    if "backend" in compacted:
        backend_type, *_ = compacted["backend"][0].keys()
        backend_config = compacted["backend"][0].pop(backend_type)
        backend_config = {"backend": dict(type=backend_type, **backend_config)}
        compacted.update(backend_config)
    return compacted
