import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy

class InstagramcomSpider(scrapy.Spider):

    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'orca.test'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1595444151:ASxQAGv8ZqMNWnquid/Nia+d84Y5lXnpOftA0htPhRVSJiZb1OKrlfIMBcNy0E9GabWdAfYUip2eicNTnYQifnHpTeFKWvKK9Hp3OxEKftiJnijfLWzRDdJOPX3t2dpEfsQtunYoXErxAXM6gc0='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['orca.share', 'polar.bears']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):

        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            url=self.inst_login_link,
            method='POST',
            callback=self.users_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def users_parse(self, response: HtmlResponse):

        j_body = json.loads(response.text)

        if j_body['authenticated']:
            for p_u in self.parse_user:
                yield response.follow(
                    f'/{p_u}',
                    callback=self.user_follow_parse,
                    cb_kwargs={'username': p_u}
                )

    def user_follow_parse(self, response: HtmlResponse, username):

        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 50}

        followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
        yield response.follow(
            followers,
            callback=self.user_info_parse,
            cb_kwargs={'username': username,
                       'type': 'followers',
                       'variables': deepcopy(variables)}
        )

        following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'
        yield response.follow(
            following,
            callback=self.user_info_parse,
            cb_kwargs={'username': username,
                       'type': 'following',
                       'variables': deepcopy(variables)}
        )

    def user_info_parse(self, response: HtmlResponse, username, type, variables):

        j_data = json.loads(response.text)

        types = 'edge_followed_by'\
        if type == 'followers'\
        else 'edge_follow'

        page_info = j_data.get('data').get('user').get(types).get('page_info')

        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url = f'{response.url[:response.url.find("&")]}&{urlencode(variables)}'
            yield response.follow(
                url,
                callback=self.user_info_parse,
                cb_kwargs={'username': username,
                           'type': type,
                           'variables': deepcopy(variables)}
            )

            users = j_data.get('data').get('user').get(types).get('edges')
            for user in users:
                item = InstaparserItem(
                    _id=user['node']['id'],
                    user_name=user['node']['username'],
                    photos=user['node']['profile_pic_url'],
                    db_info=f'{username}_{type}'
                )

            yield item

    def fetch_csrf_token(self, text):

        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):

        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()

        return json.loads(matched).get('id')
