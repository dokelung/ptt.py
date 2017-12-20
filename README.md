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

## class ArticleListPage(Page): alias to Board

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

### classmethod (Constructor)

| classmethod Name | Return Type | Note |
|---|---|---|
| ArticleListPage.from_board(board, index) | ArticleListPage | return `ArticleListPage` by board name (and index), alias to `Board(board, index)` |

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
| title | str | title of Article | |
| category | str | string in `'['` and `']'` of title | |
| board | str | board name of Article | |
| aid | str | Article ID | |
| date | str | string of Article date | `'Tue Feb 16 20:15:23 2016'` |
| datetime | datetime | datetime format of date | |
| author | str | string of Article author | |
| ip | str | author's ip | |
| signature | str | signature string of the author | |
| pushes | `Pushes` | Pushes is a class which collects all pushes in article | |
| content | str | main content of article using html format | |
| isreply | bool | `True` if `'Re:'` in title else `False` | |
| isforward | bool | `True` if `'Fw:'` in title else `False` | |

### API

| API Name | Return Type | Note |
|---|---|---|
| ArticlePage.dump_json() | str | dump json string with data:  board, aid, author, date, content, ip, pushes_count, pushes |

### classmethod (Constructor)

| classmethod Name | Return Type | Note |
|---|---|---|
| ArticlePage.from_board_aid(board, aid) | ArticlePage | return `ArticlePage` by board name and aid |

## class Pushes

### attribute

| Attr Name | Type | Note | Example |
|---|---|---|---|
| article | `ArticlePage` | ArticlePage of these pushes | |
| msgs | list | list of `Msg`(self defined namedtuple) | |
| count['all'] | int | total msg in Pushes | |
| count['score'] | int | positive msg count - negative msg count | |
| count['like'] | int | positive msg count | |
| count['boo'] | int | negative msg count | |
| count['neutral'] | int | neutral msg count | |
| simple_expression | str | string expression of all msgs | |

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
