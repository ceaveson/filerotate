from filerotate import filerotate
import pytest
import os
import yaml


data = "first"
data1 = {"name": "data1", "data": data}

rotate_dirs = ["latest", "previous"]


# Check that the required rotate_dirs are created on initial script run
@pytest.mark.parametrize("test_dir", rotate_dirs)
def test_create_rotate_dirs(tmp_path, test_dir):
    d = tmp_path
    filerotate(data1["name"], data1, d)
    assert test_dir in os.listdir(d)


# Check that a yaml file is created in both latest and previous dirs
# on the first run
@pytest.mark.parametrize("test_dir", rotate_dirs)
def test_yamls_created_when_no_initial_files(tmp_path, test_dir):
    d = tmp_path
    filerotate(data1["name"], data1, d)
    assert data1["name"] in os.listdir(str(d) + "/" + test_dir)


# After the first run, if the input dicts contents are different then we
# should the output yaml files in 'latest' and 'previous' dirs are also
# different
def test_yamls_have_different_content_on_subsequent_runs(tmp_path):
    d = tmp_path
    filerotate(data1["name"], data1, d)
    data1["data"] = "second"
    filerotate(data1["name"], data1, d)
    with open(str(d) + "/previous/" + data1["name"]) as stream:
        first = yaml.safe_load(stream)
    with open(str(d) + "/latest/" + data1["name"]) as stream:
        second = yaml.safe_load(stream)
    assert first["data"] == "first" and second["data"] == "second"
