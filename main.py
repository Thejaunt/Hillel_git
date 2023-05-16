from http.cookies import SimpleCookie


def parse(query: str) -> dict:
    pass


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
    parse_cookie('name=Dima;')


if __name__ == "__main__":
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
