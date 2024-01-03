# noqa: D100
from collections import defaultdict
from typing import Mapping


def _compact_type_label_label_block_array(array: list) -> Mapping:
    """Compact list of blocks with a `type "label" "label" {}` signature."""
    compacted = defaultdict(dict)
    for definition in array:
        assert len(definition.keys()) == 1

        kind, *_ = definition.keys()
        children = definition[kind]

        name, *_ = children.keys()
        block_definition = dict(**children[name])

        compacted[kind][name] = _compact_lifecycle_block_array(block_definition)

    return dict(**compacted)


def _compact_type_label_block_array(array: list) -> Mapping:
    """Compact list of blocks with a `type "label" {}` signature."""
    compacted = defaultdict(dict)
    for definition in array:
        assert len(definition.keys()) == 1

        name, *_ = definition.keys()
        block_definition = definition[name]

        compacted[name] = _compact_lifecycle_block_array(block_definition)
    return dict(**compacted)


def _compact_type_block_array(array: list) -> Mapping:
    """Compact list of blocks with a `type {}` signature."""
    compacted = {}
    for d in array:
        compacted.update(d)
    return compacted


def _compact_lifecycle_block_array(block_definition: Mapping) -> Mapping:
    """Compact a block's `lifecycle` array.

    This is a simple replace operation if the `lifecycle` key is present in the
    given `block_definition`.

    Lifecycle blocks may only be declared *once*, allowing us the simple conversion
     of :mod:`hcl2`'s parser result of a single-item list of dicts to a dict.
    """
    if "lifecycle" in block_definition:
        block_definition["lifecycle"] = block_definition["lifecycle"][0]
    return block_definition


def compact_resource_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "resource" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "resource" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_label_block_array(config.get("resource", []))


def compact_data_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "data" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "data" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_label_block_array(config.get("data", []))


def compact_output_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "output" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "output" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_block_array(config.get("output", []))


def compact_variable_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "variable" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "variable" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_block_array(config.get("variable", []))


def compact_locals_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "locals" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "locals" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_block_array(config.get("locals", []))


def compact_module_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "module" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "module" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_block_array(config.get("module", []))


def compact_provider_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "provider" key value, converting it from list to mapping.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "provider" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    return _compact_type_label_block_array(config.get("provider", []))


def compact_check_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "check" key value, converting it from list to mapping.

    We also take care of compacting each check block definition's `data` sub-block, if
    it's present.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "check" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    initial = _compact_type_label_block_array(config.get("check", []))
    compacted = {}
    for check, config in initial.items():
        if "data" in config:
            config["data"] = _compact_type_label_label_block_array(config["data"])
        compacted[check] = config
    return compacted


def compact_moved_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "moved" key value, converting it from list to mapping.

    To make it easier to traverse a blocks migration path, the items are merged into
    a single mapping, with each block's `to` and `from` attributes used as key and value,
    respectively. This way, you can traverse the migration path backwards using the following
    snippet:

    ```python
    previous_addr = compacted["moved"].get(current_addr)
    while previous_addr in compacted["moved"]:
        previous_addr = compacted["moved"][current_addr]
    print("oldest known addr for {current_addr} is {previous_addr}")
    ```

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "moved" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    compacted = {}
    for block in config.get("moved", []):
        compacted[block["to"]] = block["from"]
    return compacted


def compact_import_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "import" key value, converting it from list to mapping.

    To make it easier to look up the ID used to import a resource block, the list items are
    merged into a single mapping; their attributes (`to` and `id`) being used as key and value
    (respectively).

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "import" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    compacted = {}
    for block in config.get("import", []):
        compacted[block["to"]] = block["id"]
    return compacted


def compact_terraform_block_array(config: Mapping) -> Mapping:
    """Compact the given `config`'s "terraform" key value, converting it from list to mapping.

    In addition to the list-to-mapping conversion, it also compacts at deeper levels. For example,
    the `required_providers` and `backend` blocks are compacted as well, removing the need to
    access their values via index 0.

    :param config: A mapping describing HCL2 files, e.g. as parsed by :func:`hcl2.loads`.
    :type config: Mapping
    :return: `config`'s "terraform" value, assumed to be a block array, converted to a Mapping
    :rtype: Mapping
    """
    compacted = _compact_type_block_array(config.get("terraform", []))

    if "required_providers" in compacted:
        compacted["required_providers"] = _compact_type_block_array(compacted["required_providers"])
    if "backend" in compacted:
        backend_type, *_ = compacted["backend"][0].keys()
        backend_config = compacted["backend"][0].pop(backend_type)
        backend_config = {"backend": dict(type=backend_type, **backend_config)}
        compacted.update(backend_config)
    return compacted
