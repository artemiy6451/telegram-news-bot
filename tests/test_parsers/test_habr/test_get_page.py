import requests


def test_get_page_succsessfull_response(parser_instance, mock_succsessfull_response):
    expected_result = "test"
    parser_instance.session.get.return_value = mock_succsessfull_response
    parser_instance.session.get.return_value.text = "test"
    page_number = 1

    assert parser_instance._get_page(page_number) == expected_result


def test_get_page_fail_response(parser_instance, mock_fail_response):
    expected_result = None
    parser_instance.session.get.return_value = mock_fail_response
    page_number = 1

    assert parser_instance._get_page(page_number) == expected_result


def test_get_page_request_exception(parser_instance):
    expected_result = None
    parser_instance.session.get.side_effect = requests.RequestException
    page_number = 1

    assert parser_instance._get_page(page_number) == expected_result


def test_get_page_wrong_page_number(parser_instance):
    expected_result = None
    page_number = 0

    assert parser_instance._get_page(page_number) == expected_result
