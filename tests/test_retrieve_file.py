import pytest
from fs023.retrieve_file import validate_csv_key, list_candidate_objects, S3ObjectRef


def test_validate_csv_key_accepts_csv():
    validate_csv_key("incoming/data.csv")  # should not raise


@pytest.mark.parametrize("bad_key", ["incoming/data.json", "incoming/data.txt", "data"])
def test_validate_csv_key_rejects_non_csv(bad_key):
    with pytest.raises(ValueError):
        validate_csv_key(bad_key)


def test_validate_csv_key_blocks_path_traversal():
    with pytest.raises(ValueError):
        validate_csv_key("../secrets.csv")


def test_list_candidate_objects_returns_refs():
    objects = [
        {"Bucket": "my-raw-bucket", "Key": "incoming/file1.csv"},
        {"Bucket": "my-raw-bucket", "Key": "incoming/file2.csv"},
    ]
    refs = list_candidate_objects(objects)
    assert refs == [
        S3ObjectRef(bucket="my-raw-bucket", key="incoming/file1.csv"),
        S3ObjectRef(bucket="my-raw-bucket", key="incoming/file2.csv"),
    ]