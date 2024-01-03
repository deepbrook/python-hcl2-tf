from hcl2tf import compact

import pytest
import json
import hcl2


class TestGenericCompactFuncs:
    """Assert behaviour of generic compactor functions."""

    def test_compact_type_label_label_block_array(_):
        config = 'type "first" "second" {\nattribute = "value"\n}\n'
        raw_hcl2 = hcl2.loads(config)
        expected = {"first": {"second": {"attribute": "value"}}}
        compacted = compact._compact_type_label_label_block_array(raw_hcl2["type"])
        assert compacted == expected

    def test_compact_type_label_block_array(_):
        config = 'type "first" {\nattribute = "value"\n}\n'
        raw_hcl2 = hcl2.loads(config)
        expected = {"first": {"attribute": "value"}}
        compacted = compact._compact_type_label_block_array(raw_hcl2["type"])
        assert compacted == expected

    def test_compact_type_block_array(_):
        config = 'type {\nattribute = "value"\n}\n'
        raw_hcl2 = hcl2.loads(config)
        expected = {"attribute": "value"}
        compacted = compact._compact_type_block_array(raw_hcl2["type"])
        assert compacted == expected

    def test_compact_lifecycle_block_array(_):
        block_def = {"lifecycle": [{"ignore_changes": ["some_attr"]}]}
        expected = {"lifecycle": {"ignore_changes": ["some_attr"]}}
        assert compact._compact_lifecycle_block_array(block_def) == expected


class TestBlockSpecificCompactFuncs:
    """Assert behaviour for block-specific compactor functions."""

    @pytest.mark.parametrize(
        "block_type",
        argvalues=[
            "resource",
            "data",
            "variable",
            "locals",
            "output",
            "module",
            "provider",
            "terraform",
            "import",
            "moved",
            "check",
        ],
    )
    def test_compact_resource_block_array(self, sample_dir, block_type):
        config_path = sample_dir.joinpath(block_type, "config.tf")
        json_path = sample_dir.joinpath(block_type, "compacted.json")

        config = hcl2.loads(config_path.read_text())
        compactor_func = getattr(compact, f"compact_{block_type}_block_array")

        actual = compactor_func(config)
        expected = json.loads(json_path.read_text())

        assert actual == expected
