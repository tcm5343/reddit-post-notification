def parse_title_for_have(post_title: str) -> str:
    post_title = post_title.lower()
    return post_title[post_title.find("[h]") + 3:post_title.find("[w]")]


def parse_title_for_want(post_title: str) -> str:
    post_title = post_title.lower()
    return post_title[post_title.find("[w]") + 3:]
