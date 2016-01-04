# -*- coding: utf-8 -*-
from twitter import Twitter, OAuth

from tokens import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class Cleaner(object):
    def __init__(self, user_id=None, screen_name=None):
        self.user_id = user_id
        self.screen_name = screen_name
        self.t = Twitter(
            auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET),
            retry=True
        )

    def followers(self, count=1000):
        count = self.__box(5000, count)
        while True:
            for _id in self.t.followerss.ids(user_id=self.user_id, count=count)['ids']:
                self.t.blocks.create(user_id=_id)
                self.t.blocks.destroy(user_id=_id)

    def favorites(self, count=200):
        count = self.__box(200, count)
        while True:
            [self.t.favorites.destroy(_id=data['id']) for data in self.t.favorites.list(count=count)]

    def friends(self, count=1000):
        count = self.__box(5000, count)
        while True:
            [self.t.friendships.destroy(_id=_id) for _id in self.t.friends.ids(user_id=self.user_id, count=count)['ids']]

    def tweets(self, count=200):
        count = self.__box(200, count)
        while True:
            [self.t.statuses.destroy(_id=data['id']) for data in self.t.statuses.user_timeline(user_id=self.user_id, count=count)]

    def __box(self, threshold, value):
        return 1 if value <= 0 else threshold if value > threshold else value


if __name__ == '__main__':
    import sys
    c = Cleaner(user_id=321961587, screen_name='mtwtkman')
    funcs = {
        'fl': c.followers,
        'fv': c.favorites,
        'fr': c.friends,
        'tw': c.tweets
    }
    funcs.get(sys.argv[1], lambda: print('invalid arguments.({})'.format(sys.argv[1])))()
