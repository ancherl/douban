import scrapy

from douban.items import DoubanItem

from collections import OrderedDict

class SpiderDoubanSpider(scrapy.Spider):
    name = 'spider_douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 1
    # }

    def parse(self, response):
        baseUrl = response.url

        # 获取整个电影列表的树形结构
        movie_list = response.xpath('//ol[@class="grid_view"]/li')

        for movie in movie_list:
            # 创建Item 实例
            doubanItem = DoubanItem()
            # doubanItem['image'] = movie.xpath('.//div[@class="pic"]//img/@src').extract_first()
            # doubanItem['movie_name'] = movie.xpath('.//div[@class="info"]//a/span[@class="title"]/text()').extract_first()
            # doubanItem['average'] = movie.xpath(
            #     './/div[@class="info"]//div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            doubanItem['id'] = movie.xpath('.//div[@class="pic"]/em/text()').extract_first()

            # doubanItem['id'] = movie.xpath('.//div[@class="pic"]/em/text()').extract_first()
            detail_link = movie.xpath('.//div[@class="info"]/div[@class="hd"]/a/@href').extract_first()

            # print(doubanItem)
            # print(detail_link)

            if detail_link is not None:
                yield scrapy.Request(detail_link, callback=self.detail_parse, meta={'item': doubanItem})

        next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href').extract_first()
        if next_url is not None:
            # 如果有next link, 则拼接URL
            # 注意需使用response.urljoin 去拼接URL, 直接用'+' 会导致追加URL的情况
            yield response.follow(next_url, callback=self.parse)
            # next_url = response.urljoin(next_url)
            # yield scrapy.Request(next_url, callback=self.parse)

    def detail_parse(self, response):
        # 直接实例化一个doubanItem 对象
        doubanItem = response.meta['item']

        # doubanItem['id'] = response.xpath('//div[@id="content"]/div[@class="top250"]/span/text()').extract_first().replace('No.', '')
        doubanItem['image'] = response.xpath('//div[@id="mainpic"]//img/@src').extract_first()
        doubanItem['movie_name'] = response.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract_first()
        doubanItem['average'] = response.xpath(
            '//div[@class="article"]//div[@class="rating_self clearfix"]/strong/text()').extract_first()
        # doubanItem['id'] = response.xpath('.//div[@class="pic"]/em/text()').extract_first()

        doubanItem['director'] = response.xpath('//div[@id="info"]//span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract_first()
        # '%s'%t for t in response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract()
        doubanItem['type'] = ' / '.join(response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract())
        doubanItem['publish_date'] = response.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract_first()
        doubanItem['duration'] = response.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract_first()

        yield doubanItem

