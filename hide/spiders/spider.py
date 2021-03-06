# -*- coding=utf8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
import DB
class HideSpider(CrawlSpider):
    name = 'hide'

    # def __init__(self, category=None, *args, **kwargs):
    #     super(HideSpider, self).__init__(*args, **kwargs)
    #
    #     self.url = category
    #
    #     self.start_urls = ['http://'+url]
    #     deny_extensions = [
    #         # audio
    #         'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
    #
    #         # video
    #         '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    #         'm4a', 'm4v',
    #
    #         # office suites
    #         'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
    #         'odp',
    #
    #         # other
    #         'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar',
    #     ]
    #     self.rules = [
    #         Rule(LinkExtractor(allow=url + '.*'), callback='parse_new_url', follow=True),
    #         Rule(LinkExtractor(tags='img', attrs='src', deny_extensions=deny_extensions), callback='extract_img',
    #              follow=True)
    #     ]

    def __init__(self, **kw):

        deny_extensions = [
            # audio
            'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

            # video
            '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
            'm4a', 'm4v',

            # office suites
            'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
            'odp',

            # other
            'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar',
        ]

        url = kw.get('url') or kw.get('domain') or 'http://scrapinghub.com/'
        self.url = url
        url_http = None
        if not url.startswith('http://') and not url.startswith('https://'):
            url_http = 'http://%s' % url
        else:
            url_http = url
        self.start_urls = [url_http]
        self.rules = (
            Rule(LinkExtractor(allow=url + '.*'), callback='parse_new_url', follow=True),
            Rule(LinkExtractor(tags='img', attrs='src', deny_extensions=deny_extensions), callback='extract_img',
                 follow=True)
        )

        print(self.start_urls)
        super(HideSpider, self).__init__(**kw)

    ##rules meiyou shuxing
    ##rules 没有属性， 考虑直接在spider内写入所有url，然后在rule中调试规则     或者  在main函数中写入参数，来实现命令行输入参数 -a url = ……
    def parse_new_url(self, response):
        print('11111111111' + response.url)
        # open(response.url.split('/'))
        home_path = './'+self.url
        split = response.url.split('/')
        path = ''
        for name in split[3:-1]:
            path = path + name +'/'
        filename = split[-1]
        if not(os.path.exists(home_path + '/' + path)):
            print("not exists!!!!!")
            os.makedirs(home_path + '/' + path)
        if len(filename) > 254:
            filename = filename[:254]
        with open(home_path + '/' + path + filename + '.html','wb') as f:
            f.write(response.body)

    def extract_img(self,response):
        home_path = './' + self.url
        split = response.url.split('/')
        path = ''
        for name in split[3:-1]:
            path = path + name + '/'
        filename = split[-1]
        if not(os.path.exists(home_path + '/' + path)):
            print("not exists!!!!!")
            os.makedirs(home_path + '/' + path)
        if len(filename) > 254:
            filename = filename[:254]
        with open(home_path + '/' + path + filename,'wb') as f:
            f.write(response.body)
        print('22222222222'+response.url)

    def parse_start_url(self,response):
        print('index.html!!!' + response.url)
        # open(response.url.split('/'))
        home_path = './' + self.url

        if not (os.path.exists(home_path )):
            print("not exists!!!!!")
            os.makedirs(home_path )

        with open(home_path + '/' + 'index.html', 'wb') as f:
            f.write(response.body)
if '__main__' == __name__:
    # configure_logging()
    # runner = CrawlerRunner()
    # runner.crawl(HideSpider())
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()

    # def setup_crawler(domain):
    #     spider = HideSpider(domain=domain)
    #     settings = get_project_settings()
    #     print settings.__str__()
    #     crawler = Crawler(settings)
    #     crawler.configure()
    #     crawler.crawl(spider)
    #     crawler.start()



    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    """load urls from file
    """
    # urls_file = open('URLS.txt')
    # urls = urls_file.read().split()
    """load urls from checkedDB
    """
    urls = DB.selectWeekHosts()
    for index in range(len(urls)):
         print(type(urls[index][0]))
         process.crawl('hide',domain = urls[index])

    # urls = DB.selectWeekHosts
    # for index in range(len(urls)):
    #     process.crawl('hide',domain = urls[index])
    # process.crawl('hide', domain='durmansibl4r6llo.onion')
    # 'followall' is the name of one of the spiders of the project.
    # process.crawl('hide',domain='china.nba.com')
    process.start()  # the script will block here until the crawling is finished
