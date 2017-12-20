import urllib
import datetime
import collections
import json
import argparse
import time

import requests
from bs4 import BeautifulSoup


# exception
class InValidBeautifulSoupTag(Exception):
    pass


class NoGivenURLForPage(Exception):
    pass


class PageNotFound(Exception):
    pass


class ArtitcleIsRemove(Exception):
    pass


# utility
def parse_std_url(url):
    prefix, _,  basename = url.rpartition('/')
    basename, _, _ = basename.rpartition('.')
    bbs, _, board = prefix.rpartition('/')
    bbs = bbs[1:]
    return bbs, board, basename


def parse_title(title):
    _, _, remain = title.partition('[')
    category, _, remain = remain.rpartition(']')
    category = category if category else None
    isreply = True if 'Re:' in title else False
    isforward = True if 'Fw:' in title else False
    return category, isreply, isforward


def parse_username(full_name):
    name, nickname = full_name.split(' (')
    nickname = nickname.rstrip(')')
    return name, nickname


Msg = collections.namedtuple('Msg', ['type', 'user', 'content', 'ipdatetime'])


class ArticleSummary(object):

    def __init__(self, title, url, score, date, author, mark, removeinfo):

        # title
        self.title = title
        self.category, self.isreply, self.isforward = parse_title(title)

        # url
        self.url = url
        _, self.board, self.aid = parse_std_url(url)

        # meta
        self.score = score
        self.date = date
        self.author = author
        self.mark = mark

        # remove
        self.isremoved = True if removeinfo else False
        self.removeinfo = removeinfo

    @classmethod
    def from_bs_tag(cls, tag):

        try:
            removeinfo = None
            title_tag = tag.find('div', class_='title')
            a_tag = title_tag.find('a')

            if not a_tag:
                removeinfo = title_tag.get_text().strip()

            if not removeinfo: 
                title = a_tag.get_text().strip()
                url = a_tag.get('href').strip()
                score = tag.find('div', class_='nrec').get_text().strip()
            else:
                title = '本文章已被刪除'
                url = ''
                score = ''

            date = tag.find('div', class_='date').get_text().strip()
            author = tag.find('div', class_='author').get_text().strip()
            mark = tag.find('div', class_='mark').get_text().strip()
        except:
            # print(tag)
            raise InValidBeautifulSoupTag

        return cls(title, url, score, date, author, mark, removeinfo)

    def __repr__(self):
        return '<Summary of Article("{}")>'.format(self.url)

    def __str__(self):
        return self.title

    def read(self):
        if self.isremoved:
            raise ArtitcleIsRemove
        return ArticlePage(self.url)


class Page(object):
    
    ptt_domain = 'https://www.ptt.cc'

    def __init__(self, url):
        if not url:
            raise NoGivenURLForPage

        self.url = url

        url = urllib.parse.urljoin(self.ptt_domain, self.url)
        resp = requests.get(url=url, cookies={'over18': '1'}, verify=True, timeout=3)

        if resp.status_code == requests.codes.ok:
            self.html = resp.text
        else:
            # print(resp.status_code)
            raise PageNotFound


class ArticleListPage(Page):

    def __init__(self, url):
        super().__init__(url)

        # to set article_tags
        soup = BeautifulSoup(self.html, 'lxml')
        self.article_summary_tags = soup.find_all('div', 'r-ent')
        self.article_summary_tags.reverse()

        # to set related urls
        action_tags = soup.find('div', class_='action-bar').find_all('a')
        self.related_urls = {}
        url_names = 'board man oldest previous next newest'
        for idx, name in enumerate(url_names.split()):
            self.related_urls[name] = action_tags[idx].get('href')

        # to set board and idx
        _, self.board, basename = parse_std_url(url)
        _, _, idx = basename.partition('index')
        if idx:
            self.idx = int(idx)
        else:
            _, self.board, basename = parse_std_url(self.related_urls['previous'])
            _, _, idx = basename.partition('index')
            self.idx = int(idx)+1

    @classmethod
    def from_board(cls, board, index=''):
        url = '/'.join(['/bbs', board, 'index'+str(index)+'.html'])
        return cls(url)

    def __repr__(self):
        return 'ArticleListPage("{}")'.format(self.url)

    def __iter__(self):
        return self.article_summaries

    @property
    def article_summaries(self):
        return (ArticleSummary.from_bs_tag(tag) for tag in self.article_summary_tags)

    @property
    def previous(self):
        return ArticleListPage(self.related_urls['previous'])

    @property
    def next(self):
        return ArticleListPage(self.related_urls['next'])

    @property
    def oldest(self):
        return ArticleListPage(self.related_urls['oldest'])

    @property
    def newest(self):
        return ArticleListPage(self.related_urls['newest'])


class ArticlePage(Page):

    def __init__(self, url):
        super().__init__(url)

        _, _, self.aid = parse_std_url(url)

        # to set article_tags
        soup = BeautifulSoup(self.html, 'lxml')
        main_tag = soup.find('div', id='main-content')
        meta_name_tags = main_tag.find_all('span', class_='article-meta-tag')
        meta_value_tags = main_tag.find_all('span', class_='article-meta-value')

        # dealing meta
        try:
            self.author = meta_value_tags[0].get_text().strip()
            self.board = meta_value_tags[1].get_text().strip()
            self.title = meta_value_tags[2].get_text().strip()
            self.date = meta_value_tags[3].get_text().strip()

            self.category, self.isreply, self.isforward = parse_title(self.title)
            self.datetime = datetime.datetime.strptime(self.date, '%a %b %d %H:%M:%S %Y')
        except:
            self.author, self.board, self.title, self.date = '', '', '', ''
            self.category, self.isreply, self.isforward = '', False, False
            self.datetime = None

        # remove meta
        for tag in main_tag.select('div.article-metaline'):
            tag.extract()
        for tag in main_tag.select('div.article-metaline-right'):
            tag.extract()

        # fetch pushes and remove them
        self.pushes = Pushes(self)
        push_tags = main_tag.find_all('div', class_='push')
        for tag in push_tags:
            tag.extract()
        for tag in push_tags:
            if not tag.find('span', 'push-tag'):
                continue
            push_type = tag.find('span', class_='push-tag').string.strip(' \t\n\r')
            push_user = tag.find('span', class_='push-userid').string.strip(' \t\n\r')
            push_content = tag.find('span', class_='push-content').strings
            push_content = ' '.join(push_content)[1:].strip(' \t\n\r')
            push_ipdatetime = tag.find('span', class_='push-ipdatetime').string.strip(' \t\n\r')
            msg = Msg(type=push_type, user=push_user, content=push_content, ipdatetime=push_ipdatetime)
            self.pushes.addmsg(msg)
        self.pushes.countit()

        # handle special item
        ip_tags = main_tag.find_all('span', class_='f2')
        dic = {}
        for tag in ip_tags:
            if '※' in tag.get_text():
                key, _, value = tag.get_text().partition(':')
                key = key.strip('※').strip()
                value = value.strip()
                if '引述' in key:
                    continue
                else:
                    dic.setdefault(key, []).append(value)
                    tag.extract()
        self.ip = dic['發信站'][0].split()[-1]

        # remove richcontent
        for tag in main_tag.find_all('div', class_='richcontent'):
            tag.extract()

        # handle trans
        trans = []
        for tag in main_tag.find_all('span', class_='f2'):
            if '轉錄至看板' in tag.get_text():
                trans.append(tag.previous_element.parent)
                trans.append(tag.get_text())
                trans.append(tag.next_sibling)
                tag.previous_element.parent.extract()
                tag.next_sibling.extract()
                tag.extract()

        # split main content and signature
        self.content, self.signature = str(main_tag).split('--')[:2]
        self.content = self.content.strip()

        contents = self.content.split('\n')
        self.content = '\n'.join(content for content in contents if not ('<div' in content and 'main-content' in content))

        contents = self.signature.split('\n')
        self.signature = '\n'.join(content for content in contents if not ('</div' in content))

    @classmethod
    def from_board_aid(cls, board, aid):
        url = '/'.join(['/bbs', board, aid+'.html'])
        return cls(url)

    def __repr__(self):
        return 'ArticlePage("{}")'.format(self.url)

    def __str__(self):
        return self.title

    def dump_json(self):
        data = {
            'board': self.board,
            'aid': self.aid,
            'author': self.author,
            'date': self.date,
            'content': self.content,
            'ip': self.ip,
            'pushes_count': self.pushes.count,
            'pushes': self.pushes.simple_expression
        }
        return json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)


class Pushes:

    def __init__(self, article):
        self.article = article
        self.msgs = []
        self.count = 0

    def __repr__(self):
        return 'Pushes({})'.format(repr(self.article))

    def __str__(self):
        return 'Pushes of Article {}'.format(self.Article)

    def addmsg(self, msg):
        self.msgs.append(msg)

    def countit(self):
        count_types = 'all abs like boo neutral'.split()
        self.count = dict(zip(count_types, [0, 0, 0, 0, 0]))
        for msg in self.msgs:
            if msg.type == '推':
                self.count['like'] += 1
            elif msg.type == '噓':
                self.count['boo'] += 1
            else:
                self.count['neutral'] += 1

        self.count['all'] = self.count['like'] + self.count['boo'] + self.count['neutral']
        self.count['score'] = self.count['like'] - self.count['boo']

    @property
    def simple_expression(self):
        msgs = []
        attrs = ['type', 'user', 'content', 'ipdatetime']
        for msg in self.msgs:
            msgs.append(dict(zip(attrs, list(msg))))
        return msgs


# alias
Summary = ArticleSummary
Article = ArticlePage
Board = ArticleListPage.from_board


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ptt.py')


    parser.add_argument('-b', '--board', metavar='Board', type=str, required=True, help='board name')
    parser.add_argument('-d', '--destination', metavar='DIR', type=str, default='.', help='destination')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--aid', metavar='ID', type=str, help='article id')

    args = parser.parse_args()

    t1 = time.time()
    if args.aid:
        article = Article.from_board_aid(args.board, args.aid)
        print(article.aid, article.title, article.content)
    else:
        lst_page = Board(args.board)
        for summary in lst_page:
            if summary.isremoved:
                continue
            article = summary.read()
            print(article.aid, article.title if article.title else summary.title)
    elapsed = time.time()-t1
    print('total in {:.3} sec.'.format(elapsed))
