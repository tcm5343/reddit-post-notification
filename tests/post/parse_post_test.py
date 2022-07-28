from post.parse_post import parse_title_for_have, parse_title_for_want
import pytest


@pytest.mark.parametrize("post_title, expected_result", [
    ("[USA-TX] [H] 5700 XT 50th Anniversary Edition, Ryzen 7 2700x [W] Local Cash",
     " 5700 xt 50th anniversary edition, ryzen 7 2700x "),
    ("[USA-MS] [H] Paypal [W] Arctic Liquid Freezer II 360", " paypal "),
    ("[USA-GA][H] Lots of SSDs, G4400, 2x i5-6500, i3-6100, E5-2609V4, SATA HDDs, SAS HDDs [W] PayPal",
     " lots of ssds, g4400, 2x i5-6500, i3-6100, e5-2609v4, sata hdds, sas hdds "),
    ("[USA-VA] [H] RTX 3060 White [W] Local Cash / Possibly Asus G14",
     " rtx 3060 white "),
    ("[USA-TX] this doesn't have it [w] this won't be scanned", "sa-tx] this doesn't have it ")
])
def test_parse_title_for_have(post_title, expected_result):
    assert expected_result == parse_title_for_have(post_title)


@pytest.mark.parametrize("post_title, expected_result", [
    ("[USA-TX] [H] 5700 XT 50th Anniversary Edition, Ryzen 7 2700x [W] Local Cash",
     " local cash"),
    ("[USA-MS] [H] Paypal [W] Arctic Liquid Freezer II 360", " arctic liquid freezer ii 360"),
    ("[USA-GA][H] Lots of SSDs, G4400, 2x i5-6500, i3-6100, E5-2609V4, SATA HDDs, SAS HDDs [W] PayPal",
     " paypal"),
    ("[USA-VA] [H] RTX 3060 White [W] Local Cash / Possibly Asus G14",
     " local cash / possibly asus g14"),
    ("[USA-TX] this doesn't have it", "sa-tx] this doesn't have it")
])
def test_parse_title_for_want(post_title, expected_result):
    assert expected_result == parse_title_for_want(post_title)
