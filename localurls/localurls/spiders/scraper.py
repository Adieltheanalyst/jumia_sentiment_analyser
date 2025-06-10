from typing import Iterable, Any

import scrapy
import json

class jumiascraper(scrapy.Spider):
    name= "jumia"
    allowed_domains=["jumia.co.ke"]
    start_urls = [
        "https://www.jumia.co.ke/smartphones/?price=0-9999&rating=1-5#catalog-listing"
    ]

    def parse(self,response):
        product_links=response.xpath('//a[@class="core"]/@href').getall()
        for link in product_links:
            full_url=response.urljoin(link)
            yield {"url": full_url}

            for i in range(2,11):
                next_page=f"https://www.jumia.co.ke/smartphones/?price=0-9999&rating=1-5&page={i}#catalog-listing"
                yield scrapy.Request(url=next_page,callback=self.parse)
