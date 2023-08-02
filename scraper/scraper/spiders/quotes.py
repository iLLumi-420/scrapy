import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/1/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback)

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield{
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def errback(self, error):
            failed_page = int(error.request.url.split('/')[-2])
            next_page = failed_page + 1
            next_page_url = f'http://quotes.toscrape.com/{next_page}/'

            yield scrapy.Request(next_page_url, callback=self.parse, errback=self.errback)