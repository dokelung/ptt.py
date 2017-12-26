# ptt.py

* [Quick Start](#quick-start)
* [[class] ArticleSummary (alias: Summary)](#class-articlesummary-alias-to-summary)
  * [example](#example)
  * [attribute](#attribute)
  * [API](#api)
* [[class] ArticleListPage](#class-articlelistpage)
  * [example](#example-1)
  * [attribute](#attribute-1)
  * [API](#api-1)
* [[class] ArticlePage (alias to Article)](#class-articlepage-alias-to-article)
  * [example](#example-2)
  * [attribute](#attribute-2)
  * [API](#api-2)
* [[class] Pushes](#class-pushes)
  * [example](#example-3)
  * [attribute](#attribute-3)
* [[namedtuple] Msg](#namedtuple-msg)
* [Self-defined Exceptions](#self-defined-exceptions)
* [Utility Functions](#utility-functions)

## Quick Start

```python
from ptt import Board

latest_page = Board('gossiping')

for summary in latest_page:
    if summary.isremoved:
        continue
    article = summary.read()
    print(article.dump_json())
```

## class ArticleSummary: alias to Summary

### example

```python
# iterate all article summaries from specified board
for summary in Board('gossiping'):
    print(summary.title, summary.url)
    
# read article from summary
if not summary.isremoved:
    article = summary.read()
```

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| title | str | title of Article | `'[協尋] 12月18日 晚上9點前後  高雄市明誠路 鼎'` |
| category | str | string in syntax `'['` and `']'` of title | `'協尋'` |
| url | str | url of the Article without ptt domain name | `'/bbs/Gossiping/M.1513683634.A.2F5.html'` |
| board | str | board name of Article | `'Gossiping'` |
| aid | str | Article ID | `'M.1513683634.A.2F5'` |
| date | str | string of Article date | `'7/24'` |
| author | str | string of Article author (only author id) | `'jokerndmc'` |
| score | str | string of score or `'爆'` for score>99 or `'X'` for score<0 | `'20'` |
| mark | str | Article mark | `'M'` |
| removeinfo | str | remove infomation written in title | `'(本文已被刪除) [SamuraiJack]'` |
| isreply | bool | `True` if `'Re:'` in title else `False` | `True` |
| isforward | bool | `True` if `'Fw:'` in title else `False` | `False` |
| isremoved | bool | `True` if Article has been removed else `False` | `True` |

### API

| API Name | Return Type | Note |
|---|---|---|
| read() | ArticlePage | return corresponding `ArticlePage` if it is not removed |

## class ArticleListPage

### example

```python
# get page-20 of specified board
lst_page = ArticleListPage.from_board('gossiping', 20)

# you can also use the alias "Board" instead
lst_page = Board('gossiping', 20)

# get the newest page of specified board by given no page index
lst_page = Board('gossiping')

# iterate all article summaries of a article list page
for summary in lst_page:
    print(summary)
    
# get first article summary
summary = lst_page.get_article_summary(0)
```

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| board | str | board name of this ArticleListPage | `'Gossiping'` |
| idx | int | index of ArticleListPage | `29585` |
| related_urls['board'] | str | latest article list page url of the board | `'/bbs/Gossiping/index.html'` |
| related_urls['man'] | str | 精華區 url of the board | `'/man/Gossiping/index.html'` |
| related_urls['previous'] | str | preivious article list page url (`None` if not exists) | `'/man/Gossiping/index29584.html'` |
| related_urls['next'] | str | next article list page url (`None` if not exists) | `None` |
| related_urls['oldest'] | str | oldest article list page url | `'/bbs/Gossiping/index1.html'` |
| related_urls['newest'] | str | newest article list page url | `'/bbs/Gossiping/index.html'` |
| previous | ArticleListPage | `ArticleListPage` of `related_urls['previous']` | |
| next | ArticleListPage | `ArticleListPage` of `related_urls['next']` | |
| oldest | ArticleListPage | `ArticleListPage` of `related_urls['oldest']` | |
| newest | ArticleListPage | `ArticleListPage` of `related_urls['newest']` | |
| article_summaries | generator of ArticleSummary | ArticleSummary generator of this ArticleListPage | |

### API

| API Name | Return Type | Note |
|---|---|---|
| get_article_summary(index) | ArticleSummary | get `AritcleSummary` by given index |

## class ArticlePage: alias to Article

### example

```python
# get article by board name and aid
article = ArticlePage.from_board_aid('gossiping', 'M.1513683634.A.2F5')

# you can also use the alias "Article" instead
article = Article.from_board_aid('gossiping', 'M.1513683634.A.2F5')

# dump json string with aid and author
string = article.dump_json('aid', 'author')
print(string)
```

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| title | str | title of Article | `'[協尋] 12月19日 晚上9點前後  高雄市明誠路 鼎'` |
| category | str | string in `'['` and `']'` of title | `'協尋'` |
| board | str | board name of Article | `'Gossiping'` |
| aid | str | Article ID | `'M.1513683634.A.2F5'` |
| date | str | string of Article date | `'Tue Feb 16 20:15:23 2016'` |
| datetime | datetime | datetime format of date | `datetime.datetime(2017, 12, 19, 19, 40, 31)` |
| author | str | string of Article author | `'jokerndmc (小人物)'` |
| ip | str | author's ip | `'115.82.209.7'` |
| signature | str | signature string of the author | |
| pushes | Pushes | Pushes is a class which collects all pushes in article | |
| content | str | main content of article using html format | |
| isreply | bool | `True` if `'Re:'` in title else `False` | `False` |
| isforward | bool | `True` if `'Fw:'` in title else `False` | `False` |

### API

| API Name | Return Type | Note |
|---|---|---|
| dump_json(*attrs, flat=False) | str | dump json string with specified attrs |

## class Pushes

### example

```python
# get simple expression (list of dictionary) of a Pushes
>>> pushes.simple_expression
[...
 {'content': '幫高調，雖然機會不高但還是希望可以找到！',
  'ipdatetime': '12/19 22:22',
  'type': '推',
  'user': 'aquami'},
 {'content': '住附近 突然發現有鼎吉路',
  'ipdatetime': '12/21 01:34',
  'type': '推',
  'user': 'sh981215'},
  ...
]
```

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| article | `ArticlePage` | ArticlePage of these pushes | |
| msgs | list | list of `Msg`(self-defined namedtuple) | |
| count['all'] | int | total msg in Pushes | `38` |
| count['score'] | int | positive msg count - negative msg count | `23` |
| count['like'] | int | positive msg count | `26` |
| count['boo'] | int | negative msg count | `3` |
| count['neutral'] | int | neutral msg count | `9` |
| simple_expression | list | list of dictionaries which are used to model every `Msg` | |

## namedtuple Msg

```python
collections.namedtuple('Msg', ['type', 'user', 'content', 'ipdatetime'])
```

## Self-defined Exceptions

* `Error`: Base class for all exceptions raised by this module
* `InValidBeautifulSoupTag`: Can not create ArticleSummary because of invalid bs tag
* `NoGivenURLForPage`: Given None or empty url when build page
* `PageNotFound`: Can not fetch page by given url
* `ArtitcleIsRemove`: Can not read removed article from ArticleSummary

## Utility Functions

* `parse_std_url`: Parse standard ptt url
* `parse_title`: Parse article title to get more info
* `parse_username`: Parse user name to get its user account and nickname

### example

```python
>>> parse_std_url('https://www.ptt.cc/bbs/Gossiping/M.1512057611.A.16B.html')
('https://www.ptt.cc/bbs', 'Gossiping', 'M.1512057611.A.16B')

>>> parse_title('Re: [問卦] 睡覺到底可不可以穿襪子')
('問卦', True, False)

>>> parse_username('seabox (歐陽盒盒)')
('seabox', '歐陽盒盒')
```
