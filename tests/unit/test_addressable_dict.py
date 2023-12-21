from hcl2tf import loads
from hcl2tf.utils import AddressableDict

import pytest
import json
import hcl2

from fixtures import sample_dir


def test_invalid_address_raises_key_error():
    d = AddressableDict({})
    with pytest.raises(KeyError):
        d["invalid:address"]


def test_unknown_address_raises_key_error():
    d = AddressableDict({"unknown": {"foo": "bar"}})
    with pytest.raises(KeyError):
        d["unknown.address"]


def test_regular_key_access_works():
    d = AddressableDict({"someKey": True})
    try:
        d["someKey"]
    except KeyError as e:
        raise AssertionError("Could not access top-level key") from e

def test_abc_methods_are_implemented_and_work_as_expected():
    d = AddressableDict({"test": True})
    assert len(d) == 1, "__len__ returned incorrect length!"
    for k in iter(d):
        assert k == "test", "iterator did not yield expected value!"
    d["test"] = False
    assert d["test"] is False, "__setitem__ creates unexpected result!"
    del d["test"]
    assert d == {}, "__delitem__ did not delete key!"


def test_regular_key_access_using_an_address_like_string_works():
    d = AddressableDict({"data.aws_s3_bucket.my_bucket": True})
    try:
        d["data.aws_s3_bucket.my_bucket"]
    except KeyError as e:
        raise AssertionError("Could not access top-level key") from e


def test_address_based_access_correctly_retrieves_value():
    d = AddressableDict({"data": {"aws_s3_bucket": {"my_bucket": True}}})
    assert d.get("data.aws_s3_bucket.my_bucket", False)


def test_address_based_access_handles_special_resource_case():
    """Ensure addresses not starting with a block type are treated as addresses in the resource obejct."""
    d = AddressableDict({"resource": {"aws_s3_bucket": {"my_bucket": True}}})
    assert d.get("aws_s3_bucket.my_bucket", False)


def test_variable_address_can_be_used_as_key_during_dict_lookup(sample_dir):
    """Variable references in terraform configs use `var` instead of `variable`. 
    
    This test ensures we can use this declaration to look up a variable's config.
    """
    config_tf = sample_dir.joinpath("variable", "config.tf").read_text()
    config = loads(config_tf)
    assert config["var.locked"] == config["variable"]["locked"]


def test_local_address_can_be_used_as_key_during_dict_lookup(sample_dir):
    """Local variable references in terraform configs use `local` instead of `locals` as block type. 
    
    This test ensures we can use this declaration to look up a variable's config.
    """
    config_tf = sample_dir.joinpath("locals", "config.tf").read_text()
    config = loads(config_tf)
    assert config["local.something"] == config["locals"]["something"]


def test_fetch_raises_keyError_if_path_causes_accessing_invalid_type():
    with pytest.raises(KeyError):
        AddressableDict({"test": True})._fetch(["test", "result"])
    
def test_fetch_does_exits_early_if_a_None_value_is_encountered():
    with pytest.raises(ValueError):
        AddressableDict({"test": True})._fetch([None])