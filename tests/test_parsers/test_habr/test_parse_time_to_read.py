def test_parse_time_to_read_successfull(parser_instance, soup_instance):
    expected = "5 min"
    html = f'<span class="tm-article-reading-time__label">{expected}</span>'
    soup = soup_instance(html)
    assert parser_instance._parse_time_to_read(soup) == expected


def test_parse_time_to_read_fail(parser_instance, soup_instance):
    expected = "0 min."
    html = ""
    soup = soup_instance(html)
    assert parser_instance._parse_time_to_read(soup) == expected
