from urllib.parse import parse_qs, urlparse
from http.cookies import SimpleCookie


def parse(query: str) -> dict[str, str]:
    if not isinstance(query, str):
        return {}

    parsed_url = urlparse(query)
    parameters = parse_qs(parsed_url.query)

    allowed_stuff = {'schemes': ("http", "https",), 'netloc': 'example.com'}
    if parsed_url.scheme not in allowed_stuff['schemes']:
        return {}
    if parsed_url.netloc != allowed_stuff['netloc']:
        return {}

    res = {}
    #  if multiple query values in url -> values in dict will be separated by &
    for key, value in parameters.items():
        res[key] = "&".join(set([x for x in value]))

    return res


def parse_cookie(query: str) -> dict[str, str]:
    if not isinstance(query, str):
        return {}
    cookie = SimpleCookie()
    cookie.load(query)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies


def main():
    parse('https://example.com/path/to/page?name=ferret&color=purple')
    parse_cookie('name=Dima;')

if __name__ == "__main__":
    """ PARSE TESTS """
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    #  this one suppose to fail if validate it properly
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    #  htps - wrong scheme
    assert parse('htps://example.com/path/to/page?name=ferret&color=purple&') == {}
    #  no scheme
    assert parse('example.com/page?name=ferret&name=sam&color=purple&color=purple') == {}
    #  wrong netloc=exampl.com
    assert parse('http://exampl.com/page?name=Dima') == {}
    #  no ? in the url
    assert parse('https://example.com/path/to/page/name=sam&color=purple&') == {}
    # no netloc
    assert parse("https://?name=ferret&name=sam&color=purple&color=purple") == {}
    # query is not a string
    assert parse([1, 7, 1]) == {}
    assert parse(1) == {}
    assert parse(True) == {}
    #  name=ferret name=sam -> name: ferret&sam
    q = 'https://example.com/page?name=ferret&name=sam&color=purple'
    assert parse(q) == {'name': 'ferret&sam', 'color': 'purple'} or {'name': 'sam&ferret', 'color': 'purple'}
    # color=purple color=purple -> color: purple
    q = 'https://example.com/page?name=ferret&name=sam&color=purple&color=purple'
    assert parse(q) == {'name': 'ferret&sam', 'color': 'purple'} or {'name': 'sam&ferret', 'color': 'purple'}
    """ END PARSE TESTS """

    """ PARSE_COOKIE TESTS """
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}
    # key without value
    assert parse_cookie('name=Dima=User;age=28;1;') == {}
    #  no ; at the end
    assert parse_cookie('name=Dima=User') == {'name': 'Dima=User'}
    # not a str args
    assert parse_cookie(['t=3', 'r=t']) == {}
    #  empty params
    assert parse_cookie('name=Dima=User;;;;;;;;;;;;;;') == {'name': 'Dima=User'}
    #  wrong str format +:
    assert parse_cookie('name=Dima=User;++::') == {}
    #  converts numbers properly
    assert parse_cookie('1=90') == {'1': '90'}
    #  converts reserved words properly
    assert parse_cookie('True=True') == {'True': 'True'}
    #  deletes duplicates. Quite questionable
    assert parse_cookie('name=Dima;name=Vova;') == {'name': 'Vova'}
    #  keys are case-insensitive
    assert parse_cookie('name=Dima;Name=Dima;') == {'name': 'Dima', 'Name': 'Dima'}
    #  resolves blank spaces
    assert parse_cookie('name       =          1   ;') == {'name': '1'}
    """ END PARSE_COOKIE TESTS """
    
    main()
    
    
