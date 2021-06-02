import scrapy


class QuotesSpider(scrapy.Spider):
    name = "Edinburgh"

    def start_requests(self):
        urls = [
            'http://www.drps.ed.ac.uk/20-21/dpt/cxartx08053.htm',
            'http://www.drps.ed.ac.uk/20-21/dpt/cxchem08022.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'University': 'Edinburgh',
            'Department': response.css("td::text").re('College of.*')[0],
            'Course title':'',
            'Professor':'',
            'Objective':'',
            'Prerequisite':'',
            'Required Skills':'',
            'Outcome':'',
            'References':'',
            'Scores':'',
            'Description':'',
            'University Homepage': "https://www.ed.ac.uk/",
            'course Homepage':'',
            'Professor Email':''

        }
