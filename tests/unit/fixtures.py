import pytest
import pathlib


@pytest.fixture(scope="function")
def terraform_module_samples(tmp_path_factory, request):
    requested_sample = None
    for mark in request.node.iter_markers():
        if mark.name == "sample":
            requested_sample, *_ = mark.args
            break
    if not requested_sample and request.node.parent:
        for mark in request.node.parent.iter_markers():
            if mark.name == "sample":
                requested_sample, *_ = mark.args
                break
    if not requested_sample:
        raise ValueError("Missing 'sample' marker on test!")

    # Load sample files
    sample_dir = pathlib.Path(__file__).parent.parent.joinpath(
        "samples", requested_sample
    )
    tf_config = sample_dir.joinpath("config.tf").read_text()
    expected_md = sample_dir.joinpath("expected.md").read_text()

    # Create a temp dir for the test run
    temp_dir = tmp_path_factory.mktemp("module") / requested_sample
    temp_dir.mkdir(exist_ok=True, parents=True)

    # Copy sample file contents to tmp dir for test
    temp_tf, temp_md = (temp_dir / "config.tf"), (temp_dir / "expected.md")
    temp_tf.write_text(tf_config)
    temp_md.write_text(expected_md)
    return temp_tf, temp_md


@pytest.fixture
def sample_dir():
    return pathlib.Path(__file__).parent.parent.joinpath("samples")
