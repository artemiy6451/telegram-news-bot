def test_parse_name_succsessfull(parser_instance, soup_instance):
    expected_name = "test"
    html = f'<h2 class="tm-title"><span>{expected_name}</span></h2>'
    soup = soup_instance(html)
    assert parser_instance._parse_name(soup) == expected_name


def test_parse_name_fail(parser_instance, soup_instance):
    expected_name = "Name"
    html = ""
    soup = soup_instance(html)
    assert parser_instance._parse_name(soup) == expected_name
