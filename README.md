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

-----------------------------------------------------------

## class ArticleSummary: alias to Summary

### attr

```python
(string) ArticleSummary.title          title of Article
(string) ArticleSummary.category       string in syntax "[" and "]" of title

(string) ArticleSummary.url            url of the Article without ptt domain name
(string) ArticleSummary.board          board name of Article
(string) ArticleSummary.aid            Article ID

(string) ArticleSummary.date           string of Article date (e.g. '7/24')
(string) ArticleSummary.author         string of Article author (only author id)

(string) ArticleSummary.score          string of score or '爆' for score>99 or 'X' for score<0
(string) ArticleSummary.mark           Article mark (e.g. M)

(string) ArticleSummary.removeinfo     remove infomation written in title

( bool ) ArticleSummary.isreply        True if 'Re:' in title else False
( bool ) ArticleSummary.isforward      True if 'Fw:' in title else False
( bool ) ArticleSummary.isremoved      True if Article has been removed else False
```

### API

```python
(ArticlePage) ArticleSummary.read() 
    return corresponding ArticlePage if it is not removed
```

### classmethod

```python
(ArticleSummary) ArticleSummary.from_bs_tag(tag)
    return ArticleSummary by summary tag
```

-----------------------------------------------------------

## class Page [DO NOT USE IT DIRECTLY]

### class attr

```python
(string) Page.ptt_domain                'https://www.ptt.cc'
(string) Page.ask_over_18_url           '/ask/over18'
```

### attr
 
```python
(string) Page.url                       Page url without ptt domain name
(string) Page.html                      html of Page
```

-----------------------------------------------------------

## class ArticleListPage(Page)

### attr

```python
(string) ArticleListPage.board                  board name of this ArticleListPage
( int  ) ArticleListPage.idx                    index of ArticleListPage

( list ) ArticleListPage.article_summary_tags   bs tags of ArticleSummary

( dict ) ArticleListPage.related_urls           urls of related pages        
            ArticleListPage.related_urls['board']
            ArticleListPage.related_urls['man']
            ArticleListPage.related_urls['previous']
            ArticleListPage.related_urls['next']
            ArticleListPage.related_urls['oldest']
            ArticleListPage.related_urls['newest']

( generator ) ArticleListPage.article_summaries list of ArticleSummary of this ArticleListPage

(ArticleListPage) ArticleListPage.previous ArticleListPage of related_urls['previous']
(ArticleListPage) ArticleListPage.next     ArticleListPage of related_urls['next']
(ArticleListPage) ArticleListPage.oldest   ArticleListPage of related_urls['oldest']
(ArticleListPage) ArticleListPage.newest   ArticleListPage of related_urls['newest']
```

### classmethod ----------------------------------------------------------------------------------

```python
# alias to Board(board, index)
(ArticleListPage) ArticleListPage.from_board(board, index)
    return ArticleListPage by board name (and index)
```

### iter -----------------------------------------------------------------------------------------
    
```python
for ArticleSummary in ArticleListPage:
    do something with ArticleSummary
```

-----------------------------------------------------------

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

-----------------------------------------------------------

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

-----------------------------------------------------------

## nameedtuple Msg

```python
collections.namedtuple('Msg', ['type', 'user', 'content', 'ipdatetime'])
```

-----------------------------------------------------------

## self defined Exceptions

* InValidBeautifulSoupTag
* NoGivenURLForPage
* PageNotFound
* ArtitcleIsRemove

-----------------------------------------------------------

## utility functions

* parse_std_url
* parse_title
* parse_username
