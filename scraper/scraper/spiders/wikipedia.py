import scrapy

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)']

    def parse(self, response):

        data = {}

        paragraphs = response.css('div.mw-parser-output > p')

        for i, paragraph in enumerate(paragraphs, start=1):
             if isinstance(paragraph, scrapy.selector.unified.Selector):
                text = ' '.join(paragraph.css('::text').getall()).strip()
                data[f'paragraph_{i}'] = text

        yield data
