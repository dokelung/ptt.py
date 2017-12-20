from datetime import datetime
import unittest

from ptt import Page, ArticleListPage
from ptt import Pushes
from ptt import PageNotFound


class TestPage(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        self.ic_url = 'https://www.ptt.cc/bbs/Boo/index.html'
        self.page = Page(self.url)

    def test_url(self): 
        self.assertEqual(self.page.url, self.url, 'incorrect page url')

    def test_page_not_found(self):
        self.assertRaises(PageNotFound, Page, self.ic_url)


class TestOthers(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
        self.board = 'Gossiping'
        self.lst_page = ArticleListPage.from_board(self.board)

    def test_list_page(self):
        self.assertEqual(self.lst_page.board, self.board, 'incorrect board')
        self.assertIsInstance(self.lst_page.idx, int)

    def test_list_page_iter_and_summary(self):
        for idx, s in enumerate(self.lst_page):
            if s.isremoved:
                continue
            if idx == 0:
                _, _, thing = s.title.rpartition('月')
                self.assertEqual(thing, '八卦板置底閒聊文')
                self.assertEqual(s.board, self.board)
                score_lst = [str(i) for i in range(0, 100)]
                score_lst.extend(['', '爆', 'X'])
                self.assertIn(s.score, score_lst)

    def test_read_and_article_page(self):
        for idx, s in enumerate(self.lst_page):
            if s.isremoved:
                continue
            elif idx == 0:
                continue
            else:
                apage = s.read()
                self.assertIsInstance(apage.datetime, datetime)
                self.assertIsInstance(apage.pushes, Pushes)
                break


if __name__ == '__main__':
    unittest.main()