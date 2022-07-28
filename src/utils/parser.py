def string_contains_every_element_in_list(keyword_list: list, string: str) -> bool:
    in_list = True
    # if list is empty
    if not keyword_list:
        in_list = False
    else:
        for keyword in [x.lower() for x in keyword_list]:
            if keyword not in string.lower():
                in_list = False
    return in_list


def string_contains_an_element_in_list(keyword_list: list, string: str) -> bool:
    in_list = False
    for keyword in [x.lower() for x in keyword_list]:
        if keyword in string.lower():
            return True
    return in_list
