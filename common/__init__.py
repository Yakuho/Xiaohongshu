from urllib.parse import quote
from js.app_sign import get_sign
from pprint import pprint
import requests
import json


class Base:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'accept': 'application/json, text/plain, */*',
                        'origin': 'https://pages.xiaohongshu.com',
                        'accept-encoding': 'br, gzip, deflate',
                        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit'
                                      '/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
                        'accept-language': 'zh-cn'}
        # 需要登陆后才能看的headers
        self.headers_login = {'accept': '*/*',
                              'accept-type': 'application/json',
                              'authorization': '95b02f9f-597f-4123-89bb-8e0119186e5a',
                              'device-fingerprint': '2019070511014360c1095e3a9c5b2b125182ac4ef9047e01e4b93ed21011a2',
                              'referer': 'https://servicewechat.com/wxffc08ac7df482a27/271/page-frame.html',
                              'accept-encoding': 'br, gzip, deflate',
                              'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit'
                                            '/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
                              'accept-language': 'zh-cn'}

    # 搜索商品列表
    def goods_list(self, keyword, page=1):
        keyword = quote(keyword)

        url = 'http://www.xiaohongshu.com/api/store/ps/products/v1?keyword={}&page={}&per_page=20'.format(keyword, page)
        try:
            response = self.session.get(url=url, headers=self.headers).text
        except requests.exceptions.ConnectionError:
            raise Exception('网络错误.')

        try:
            data = json.loads(response)['data']['items']

            for item in data:
                try:
                    yield {'商品url': item['link'].replace('xhsdiscover://webview/', ''),
                           '商品id': item['id'],
                           '商品图片url': item['image'],
                           '商品原价': item['price'],
                           '商品折扣价': item['discount_price'],  # 可能会因为没有折扣价而出错
                           '商品广告': item['pd_name'],
                           '商品名': item['desc'],
                           '卖家id': item['seller_id'],
                           '品牌': item['brand'],
                           '种类id': item['category_ids'],
                           'spl_id': item['spl_id'],
                           'spu_id': item['spu_id'],
                           'spv_id': item['spv_id']
                           }
                except KeyError:
                    yield {'商品url': item['link'].replace('xhsdiscover://webview/', ''),
                           '商品id': item['id'],
                           '商品图片url': item['image'],
                           '商品原价': '',
                           '商品折扣价': item['discount_price'],  # 可能会因为没有折扣价而出错
                           '商品广告': item['pd_name'],
                           '商品名': item['desc'],
                           '卖家id': item['seller_id'],
                           '品牌': item['brand'],
                           '种类id': item['category_ids'],
                           'spl_id': item['spl_id'],
                           'spu_id': item['spu_id'],
                           'spv_id': item['spv_id']
                           }
        except KeyError:
            print('Not find key-name.')
            return []

    # 搜索笔记列表
    def notes_list(self, keyword, page=1):
        keyword = quote(keyword)

        url = 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/search/notes?' \
              'keyword={}&sort=general&page={}&per_page=20'.format(keyword, page)

        try:
            items = json.loads(self.session.get(url=url, headers=self.headers_login).text)['data']['notes']
            for item in items:
                yield {'笔记id': item['id'],
                       '笔记题目': item['title'],
                       '点赞数': item['likes'],
                       '用户头像': item['user']['images'],
                       '用户名字': item['user']['nickname'],
                       '用户id': item['user']['userid']
                       }
        except KeyError:
            return []

    # 笔记详情页
    def note_detail(self, _id):
        url = 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/{}/single_feed?'.format(_id)

        data = json.loads(self.session.get(url=url, headers=self.headers_login).text)['data'][0]
        comment_list = [{'评论': item['content'], '用户名称': item['user']['nickname']} for item in data['comment_list']]
        note_list = data['note_list'][0]
        collected_count, comments_count = note_list['collected_count'], note_list['comments_count']
        desc = note_list['desc']
        return {'收藏数': collected_count, '评论数': comments_count, '评论列表': comment_list, '笔记': desc}

    # 商品内笔记 (一般最大只有16页)
    def note(self, _id, page=1, per_page=10):
        url = 'https://www.xiaohongshu.com/api/store/' \
              'jpd/notes/{}/notes_detail?page={}&per_page={}'.format(_id, page, per_page)

        try:
            items = json.loads(self.session.get(url=url, headers=self.headers).text)['data']
            for item in items:
                yield {'笔记': item['desc'],
                       '商品名字': item['title'],
                       '用户名字': item['user']['nickname'],
                       '用户id': item['user']['id'],
                       '点赞数': item['likes'],
                       '收藏数': item['collects']
                       }
        except KeyError:
            return []

    # 用户详情页
    def user(self, _id):
        url = 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/user/{}/info?'.format(_id)
        response = json.loads(self.session.get(url=url, headers=self.headers_login).text)['data']
        return {'收藏': response['collected'],
                '获赞': response['liked'],
                '粉丝': response['fans'],
                '关注': response['follows'],
                '性别': '女' if response['gender'] == 1 else '男',
                '用户名': response['nickname'],
                '等级名称': response['level']['level_name']
                }


