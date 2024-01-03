import json

from hcl2tf import load, loads
from hcl2tf.utils import AddressableDict


def test_loads_func_loads_and_compacts_tf2_hcl_files_from_filepointer(sample_dir):
    config_tf = sample_dir.joinpath("complete/config.tf")
    expected_json = sample_dir.joinpath("complete/compacted.json")
    actual = loads(config_tf.read_text())
    assert actual.config == json.loads(expected_json.read_text())


def test_loads_func_loads_tf2_hcl_config_as_AddressableDict_instance(sample_dir):
    config_tf = sample_dir.joinpath("complete/config.tf")
    actual = loads(config_tf.read_text())
    assert isinstance(actual, AddressableDict)


def test_load_func_loads_and_compacts_tf2_hcl_files_from_string(sample_dir):
    config_tf = sample_dir.joinpath("complete/config.tf")
    expected_json = sample_dir.joinpath("complete/compacted.json")
    with config_tf.open() as fp:
        actual = load(fp)
        assert actual.config == json.loads(expected_json.read_text())


def test_load_func_loads_tf2_hcl_config_as_AddressableDict_instance(sample_dir):
    config_tf = sample_dir.joinpath("complete/config.tf")
    with config_tf.open() as fp:
        actual = load(fp)
    assert isinstance(actual, AddressableDict)
