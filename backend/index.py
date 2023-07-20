import backend.apis.instance


def get_me():
    client = backend.apis.instance.getinstance()
    me = client.get_me()
    user = me.data
    print(f'{user.id}')
    return user


def get_bookmarks():
    client = backend.apis.instance.getinstance()

    bookmarks = client.c_get_bookmarks()
    client.request()
    print(f'{bookmarks}')


def fetch_pkce(username):
    return backend.apis.instance.fetch_auth_url_with_oauth2(username)
