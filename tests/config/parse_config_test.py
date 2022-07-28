import pytest
from config.parse_config import determine_who_to_notify, handle_filter_attributes


@pytest.mark.parametrize("single_filter, expected_result", [
    ({"notify": ["1580989241"]}, ["1580989241"]),
    ({"includes": ["wts"]}, []),
    ({"notify": ["1580989241", "345234523"]}, ["1580989241", "345234523"]),
    ({"notify": []}, []),
    ({}, [])
    ])
def test_determine_who_to_notify_output(single_filter, expected_result):
    assert expected_result == determine_who_to_notify(single_filter)


@pytest.mark.parametrize("attribute, title, val, expected_result", [
    ("includes", "this is an example", ["example"], True),
    ("includes", "this is an example", ["keyboard"], False),
    ("excludes", "this is an example", ["keyboard"], True),
    ("excludes", "this is an example", ["example"], False),
    ("have", "[h] this is an example [w] this is nothing", ["example"], True),
    ("have", "[h] this is an example [w] this is nothing", ["nothing"], False),
    ("want", "[h] this is an example [w] this is nothing", ["example"], False),
    ("want", "[h] this is an example [w] this is nothing", ["nothing"], True),
])
def test_handle_filter_attributes_output(attribute, title, val, expected_result):
    assert handle_filter_attributes(attribute, title, val) == expected_result


# def test_handle_filter_attributes_throws_key_error():
#     with pytest.raises(KeyError):
#         handle_filter_attributes('', 'example title', ['attribute_value'])
