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
| ArticleSummary.title | str | title of Article | |
| ArticleSummary.category | str | string in syntax `'['` and `']'` of title | |
| ArticleSummary.url | str | url of the Article without ptt domain name | |
| ArticleSummary.board | str | board name of Article | |
| ArticleSummary.aid | str | Article ID | |
| ArticleSummary.date | str | string of Article date | `'7/24'` |
| ArticleSummary.author | str | string of Article author (only author id) | |
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
| ArticleListPage.board | str | board name of this ArticleListPage | |
| ArticleListPage.idx | int | index of ArticleListPage | |
| ArticleListPage.article_summary_tags | list | bs tags of ArticleSummary | |
| ArticleListPage.related_urls | dict | urls of related pages, keys = `['board', 'man', 'previous', 'next', 'oldest', 'newest']` | |
| ArticleListPage.article_summaries | generator of ArticleSummary | ArticleSummary generator of this ArticleListPage | |
| ArticleListPage.previous | ArticleListPage | `ArticleListPage` of `related_urls['previous']` |
| ArticleListPage.next | ArticleListPage | `ArticleListPage` of `related_urls['next']` |
| ArticleListPage.oldest | ArticleListPage | `ArticleListPage` of `related_urls['oldest']` |
| ArticleListPage.newest | ArticleListPage | `ArticleListPage` of `related_urls['newest']` |

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

### attr

```python
(string)   ArticlePage.title       title of Article
(string)   ArticlePage.category    string in "[" and "]" of title

(string)   ArticlePage.board       board name of Article
(string)   ArticlePage.aid         Article ID

(string)   ArticlePage.date        string of Article date (e.g. Tue Feb 16 20:15:23 2016)
(datetime) ArticlePage.datetime    datetime format of date

(string)   ArticlePage.author      string of Article author
(string)   ArticlePage.ip          author's ip
(stirng)   ArticlePage.signature   signature string of the author

(Pushes)   ArticlePage.pushes      Pushes is a class which collects all pushes in article
(string)   ArticlePage.content     main content of article using html format

( bool )   ArticlePage.isreply     True if 'Re:' in title else False
( bool )   ArticlePage.isforward   True if 'Fw:' in title else False
```

### API

```python
(string)  ArticlePage.dump_json()
    dump json string with data
        "board", "aid", "author", "date", "content", "ip", "pushes_count", "pushes"
```

### classmethod

```python
(ArticlePage) ArticlePage.from_board_aid(board, aid)
    return  ArticlePage by board name and aid
```

## class Pushes

### attr

```python
(ArticlePage) Pushes.article            ArticlePage of these pushes

( list )      Pushes.msgs               list of Msg(self defined namedtuple)

( dict )      Pushes.count              all types of count
                Pushes.count['all']       total msg in Pushes
                Pushes.count['score']     positive msg count - negative msg count
                Pushes.count['like']      positive msg count
                Pushes.count['boo']       negative msg count
                Pushes.count['neutral']   neutral msg count

(string)      Pushes.simple_expression  string expression of all msgs
```

### API

``` python
(void)        Pushes.addmsg(Msg)        add a msg to Pushes
(void)        Pushes.countit            set Pushes.count
```

## nameedtuple Msg

```python
collections.namedtuple('Msg', ['type', 'user', 'content', 'ipdatetime'])
```

## self defined Exceptions

* InValidBeautifulSoupTag
* NoGivenURLForPage
* PageNotFound
* ArtitcleIsRemove

## utility functions

* parse_std_url
* parse_title
* parse_username
