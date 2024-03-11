def test_parse_url_successful(parser_instance, soup_instance):
    input = "/test"
    expected = "https://habr.com/test"
    html = f'<a class="tm-title__link" href="{input}"></a>'
    soup = soup_instance(html)
    assert parser_instance._parse_url(soup) == expected


def test_parse_url_no_href(parser_instance, soup_instance):
    expected = "https://habr.com"
    html = '<a class="tm-title__link"></a>'
    soup = soup_instance(html)
    assert parser_instance._parse_url(soup) == expected


def test_parse_url_failed(parser_instance, soup_instance):
    expected = "https://habr.com"
    html = ""
    soup = soup_instance(html)
    assert parser_instance._parse_url(soup) == expected
