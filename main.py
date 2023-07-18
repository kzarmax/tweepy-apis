# This is a sample Python script.
import apis.instance


def get_me():
    client = apis.instance.getinstance()
    me = client.get_me()
    user = me.data
    print(f'{user.id}')
    return user


def get_bookmarks():
    client = apis.instance.getinstance()

    bookmarks = client.c_get_bookmarks()
    client.request()
    print(f'{bookmarks}')


def fetch_pkce():
    apis.instance.fetch_pkce_with_oauth2()


if __name__ == '__main__':
    # me = get_me()
    # get_bookmarks()
    fetch_pkce()
