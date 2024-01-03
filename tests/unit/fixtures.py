import pytest
import pathlib


@pytest.fixture
def sample_dir():
    return pathlib.Path(__file__).parent.parent.joinpath("samples")
