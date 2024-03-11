def test_parse_raw_articles_successfully(parser_instance):
    expected = "test"
    page_number = 1
    html = f"<article class='tm-articles-list__item'>{expected}</article>"
    raw_articles = parser_instance._parse_raw_articles(html, page_number)
    assert len(raw_articles) == 1
    assert raw_articles[0].text == expected


def test_parse_raw_articles_with_no_articles(parser_instance):
    expected = []
    page_number = 1
    html = ""
    raw_articles = parser_instance._parse_raw_articles(html, page_number)
    assert raw_articles == expected
