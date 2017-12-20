# ptt.py

## QuickStart

```python
from ptt import ArticleListPage

page = ArticleListPage.from_board('gossiping')

for s in page:
    if s.isremoved:
        continue
    a = s.read()
    print(a.dump_json())
```

## class ArticleSummary: alias to Summary

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| ArticleSummary.title | str | title of Article | `'[協尋] 12月18日 晚上9點前後  高雄市明誠路 鼎'` |
| ArticleSummary.category | str | string in syntax `'['` and `']'` of title | `'協尋'` |
| ArticleSummary.url | str | url of the Article without ptt domain name | `'/bbs/Gossiping/M.1513683634.A.2F5.html'` |
| ArticleSummary.board | str | board name of Article | `'Gossiping'` |
| ArticleSummary.aid | str | Article ID | `'M.1513683634.A.2F5'` |
| ArticleSummary.date | str | string of Article date | `'7/24'` |
| ArticleSummary.author | str | string of Article author (only author id) | `'jokerndmc'` |
| ArticleSummary.score | str | string of score or `'爆'` for score>99 or `'X'` for score<0 | `'爆'`, `'X'`, `'20'`|
| ArticleSummary.mark | str | Article mark | `'M'` |
| ArticleSummary.removeinfo | str | remove infomation written in title | |
| ArticleSummary.isreply | bool | `True` if `'Re:'` in title else `False` | |
| ArticleSummary.isforward | bool | `True` if `'Fw:'` in title else `False` | |
| ArticleSummary.isremoved | bool | `True` if Article has been removed else `False` | |

### API

| API Name | Return Type | Note |
|---|---|---|
| ArticleSummary.read() | `ArticlePage` | return corresponding ArticlePage if it is not removed |

### classmethod (Constructor)

| classmethod Name | Return Type | Note |
|---|---|---|
| ArticleSummary.from_bs_tag(tag) | `ArticleSummary` | return ArticleSummary by summary tag |

## class ArticleListPage(Page)

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| ArticleListPage.board | str | board name of this ArticleListPage | `'Gossiping'` |
| ArticleListPage.idx | int | index of ArticleListPage | `29585` |
| ArticleListPage.related_urls | dict | urls of related pages, keys = `['board', 'man', 'previous', 'next', 'oldest', 'newest']` | |
| ArticleListPage.related_urls['board'] | str | latest article list page url of the board | `'/bbs/Gossiping/index.html'` |
| ArticleListPage.related_urls['man'] | str | 精華區 url of the board | `'/man/Gossiping/index.html'` |
| ArticleListPage.related_urls['previous'] | str | preivious article list page url (`None` if not exists) | `'/man/Gossiping/index29584.html'` |
| ArticleListPage.related_urls['next'] | str | next article list page url (`None` if not exists) | `None` |
| ArticleListPage.related_urls['oldest'] | str | oldest article list page url | `/bbs/Gossiping/index1.html` |
| ArticleListPage.related_urls['newest'] | str | newest article list page url | `/bbs/Gossiping/index.html` |
| ArticleListPage.previous | ArticleListPage | `ArticleListPage` of `related_urls['previous']` |
| ArticleListPage.next | ArticleListPage | `ArticleListPage` of `related_urls['next']` |
| ArticleListPage.oldest | ArticleListPage | `ArticleListPage` of `related_urls['oldest']` |
| ArticleListPage.newest | ArticleListPage | `ArticleListPage` of `related_urls['newest']` |
| ArticleListPage.article_summaries | generator of ArticleSummary | ArticleSummary generator of this ArticleListPage | |

### classmethod (Constructor)

| classmethod Name | Return Type | Note |
|---|---|---|
| ArticleListPage.from_board(board, index) | `ArticleListPage` | return ArticleListPage by board name (and index), alias to `Board(board, index)` |

### as iterator

Example:

```python
for ArticleSummary in ArticleListPage:
    # do something with ArticleSummary
```

## class ArticlePage(Page): alias to Article

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| ArticlePage.title | str | title of Article | |
| ArticlePage.category | str | string in `'['` and `']'` of title | |
| ArticlePage.board | str | board name of Article | |
| ArticlePage.aid | str | Article ID | |
| ArticlePage.date | str | string of Article date | `'Tue Feb 16 20:15:23 2016'` |
| ArticlePage.datetime | datetime | datetime format of date | |
| ArticlePage.author | str | string of Article author | |
| ArticlePage.ip | str | author's ip | |
| ArticlePage.signature | str | signature string of the author | |
| ArticlePage.pushes | `Pushes` | Pushes is a class which collects all pushes in article | |
| ArticlePage.content | str | main content of article using html format | |
| ArticlePage.isreply | bool | `True` if `'Re:'` in title else `False` | |
| ArticlePage.isforward | bool | `True` if `'Fw:'` in title else `False` | |

### API

| API Name | Return Type | Note |
|---|---|---|
| ArticlePage.dump_json() | str | dump json string with data:  board, aid, author, date, content, ip, pushes_count, pushes |

### classmethod (Constructor)

| classmethod Name | Return Type | Note |
|---|---|---|
| ArticlePage.from_board_aid(board, aid) | `ArticlePage` | return `ArticlePage` by board name and aid |

## class Pushes

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| Pushes.article | `ArticlePage` | ArticlePage of these pushes | |
| Pushes.msgs | list | list of `Msg`(self defined namedtuple) | |
| Pushes.count | dict | all types of count | |
| Pushes.count['all'] | int | total msg in Pushes | |
| Pushes.count['score'] | int | positive msg count - negative msg count | |
| Pushes.count['like'] | int | positive msg count | |
| Pushes.count['boo'] | int | negative msg count | |
| Pushes.count['neutral'] | int | neutral msg count | |
| Pushes.simple_expression | str | string expression of all msgs | |

## nameedtuple Msg

```python
collections.namedtuple('Msg', ['type', 'user', 'content', 'ipdatetime'])
```

## self defined Exceptions

* `InValidBeautifulSoupTag`
* `NoGivenURLForPage`
* `PageNotFound`
* `ArtitcleIsRemove`

## utility functions

* `parse_std_url`
* `parse_title`
* `parse_username`
