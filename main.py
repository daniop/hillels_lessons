from urllib.parse import urlparse, parse_qsl
import re


def parse(query: str) -> dict:
    # take url as query and return dict of query string

    return dict(parse_qsl(urlparse(query.rstrip('/')).query))


if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}

    # My tests for parse function
    assert parse('http://validator.w3.org/feed/check.cgi?url=http://feeds.feedburner.com/domainfeed') == {
        'url': 'http://feeds.feedburner.com/domainfeed'}
    assert parse('http://twitter.com/home?status=<?php echo urlencode("Currently reading: "); ?>') == {
        'status': '<?php echo urlencode("Currently reading: "); ?>'}
    assert parse('http://example.com/customers?name=Joe%20Bloggs') == {'name': 'Joe Bloggs'}
    assert parse('example.com/') == {}
    assert parse('http://domain.com?productid=xyz') == {'productid': 'xyz'}
    assert parse('https://www.domain.com/?utm_source=twitter&utm_medium=tweet&utm_campaign=summer-sale') == {
        'utm_source': 'twitter', 'utm_medium': 'tweet', 'utm_campaign': 'summer-sale'}
    assert parse('http://example.com/?name=Dima/') == {'name': 'Dima'}
    assert parse('example.com/?name=Dima/') == {'name': 'Dima'}
    assert parse('https://writets.com/sign-up?for=membership') == {'for': 'membership'}
    assert parse('http://example.com/path?name=Branch&products=[Journeys,Email,Universal%20Ads]/') == {'name': 'Branch',
                                                                                                       'products': '[Journeys,Email,Universal Ads]'}


def parse_cookie(query: str) -> dict:
    # Take a string with key=value and return dict
    pattern = r'(\w+)=([\w|=]+)?'
    matches = re.finditer(pattern, query)
    return dict((match.group(1), match.group(2)) for match in matches)


if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}

    # My tests for parse_cookie function
    assert parse_cookie('name=Dima') == {'name': 'Dima'}
    assert parse_cookie('name=Dima/&') == {'name': 'Dima'}
    assert parse_cookie('name=Dima/gov/age=28') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima/gov/:""">age=28:";') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima_Zarubin') == {'name': 'Dima_Zarubin'}
    assert parse_cookie('name=Dima_Zarubin#age=60#') == {'name': 'Dima_Zarubin', 'age': '60'}
    assert parse_cookie('sign-up?for=membership') == {'for': 'membership'}
    assert parse_cookie('something=in=the=way') == {'something': 'in=the=way'}
    assert parse_cookie('/password=q1W2e3R4tY/') == {'password': 'q1W2e3R4tY'}
    assert parse_cookie('pretty_fly=for_a_white_guy/?name=Декстер_Холланд#age=56#') == {'pretty_fly': 'for_a_white_guy',
                                                                                        'name': 'Декстер_Холланд',
                                                                                        'age': '56'}
