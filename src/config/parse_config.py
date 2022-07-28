from utils.parser import string_contains_every_element_in_list, \
    string_contains_an_element_in_list
from post.parse_post import parse_title_for_have, parse_title_for_want


def determine_who_to_notify(single_filter: dict) -> list:
    result = []
    if single_filter.get("notify"):
        for user in list(single_filter["notify"]):
            result.append(user)
    return result


def handle_filter_attributes(attribute: str, title: str, val: list) -> bool:
    try:
        return {
            "includes": string_contains_every_element_in_list(val, title),
            "excludes": not string_contains_an_element_in_list(val, title),
            "have": string_contains_every_element_in_list(val, parse_title_for_have(title)),
            "want": string_contains_every_element_in_list(val, parse_title_for_want(title)),
            "notify": True,
        }[attribute]
    except KeyError as err:
        raise KeyError("The config includes unsupported attributes:", attribute, '\n', err) from err
