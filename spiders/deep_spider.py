# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Article(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()


class DeepSpider(CrawlSpider):
    name = "Deep"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page)))
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_url],
            restrict_xpaths=[rule.extract_from]),
            callback='parse_item', follow=True))
        self.rules = tuple(rule_list)
        super(DeepSpider, self).__init__()

    def parse_item(self, response):
        self.log('Hi, this is an article page! %s' % response.url)

        article = Article()

        article["url"] = response.url

        title = response.xpath(self.rule.title_xpath).extract()
        article["title"] = title[0] if title else ""

        body = response.xpath(self.rule.body_xpath).extract()
        article["body"] = '\n'.join(body) if body else ""

        publish_time = response.xpath(self.rule.publish_time_xpath).extract()
        article["publish_time"] = publish_time[0] if publish_time else ""

        source_site = response.xpath(self.rule.source_site_xpath).extract()
        article["source_site"] = source_site[0] if source_site else ""

        return article
