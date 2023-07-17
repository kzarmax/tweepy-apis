# This is a sample Python script.
import apis.instance


def get_me():
    _, client = apis.instance.getinstance()
    me = client.get_me()
    user = me.data
    print(f'{user.id}')


def get_bookmarks():
    _, client = apis.instance.getinstance()
    bookmarks = client.get_bookmarks()
    print(f'{bookmarks}')


if __name__ == '__main__':
    get_me()
    get_bookmarks()
