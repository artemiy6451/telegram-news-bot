from telegram_news_bot.schemas import Post


def test_transform_articles_successfully(parser_instance, soup_instance):
    expected = Post(name="Test", time_to_read="5 min", url="https://habr.com/test")
    html = f"""
        <article class="tm-articles-list__item">
            <h2 class="tm-title"><span>{expected.name}</span></h2>
            <span class="tm-article-reading-time__label">{expected.time_to_read}</span>
            <a
                class="tm-title__link"
                href="{expected.url.replace('https://habr.com', '')}"></a>
        </article>
        """
    soup = soup_instance(html)
    assert parser_instance._transform_articles(soup) == [expected]


def test_transform_articles_failed(parser_instance, soup_instance):
    expected = []
    html = ""
    soup = soup_instance(html)
    assert parser_instance._transform_articles(soup) == expected
