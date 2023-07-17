# This is a sample Python script.
import apis.instance


def get_me():
    tweepy_instance = apis.instance.getinstance()
    me = tweepy_instance.get_me()
    user = me.data
    print(f'{user.id}')


def get_bookmarks():
    tweepy_instance = apis.instance.getinstance()
    bookmarks = tweepy_instance.get_bookmarks()
    print(f'{bookmarks}')


if __name__ == '__main__':
    get_me()
    get_bookmarks()
