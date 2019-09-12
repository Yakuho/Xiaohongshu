# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2019/9/6
from common import Base
from queue import Queue
from pprint import pprint
import threading


class Note(Base):
    def __init__(self):
        super(Note, self).__init__()
        self.exit = False


if __name__ == '__main__':
    a = Note()

    # data1 = a.goods_list(keyword='施华洛世奇', page=1)
    # for item in data1:
    #     pprint(item)

    # data2 = a.note('5b02548a4628396c56faddcd', page=1, per_page=10)
    # for item in data2:
    #     pprint(item)

    # data3 = a.notes_list(keyword='施华洛世奇', page=1)
    # for item in data3:
    #     pprint(item)

    # note_detail_one = a.note_detail('5d54108b000000002701f3b2')
    # pprint(note_detail_one)

    comments = a.comments(goods_id='5d118cb243e55b002b2606b4', page=3)
    for comment in comments:
        pprint(comment)
