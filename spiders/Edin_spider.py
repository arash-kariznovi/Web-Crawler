import scrapy


class QuotesSpider(scrapy.Spider):
    name = "Edinburgh"

    def start_requests(self):

        urls = [
            'http://www.drps.ed.ac.uk/20-21/dpt/cxartx08053.htm',
            'http://www.drps.ed.ac.uk/20-21/dpt/cxchem08022.htm',
            'http://www.drps.ed.ac.uk/17-18/dpt/cxcast08004.htm',
            'http://www.drps.ed.ac.uk/17-18/dpt/cxlaws10211.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def recognize(self,response,column):
        webpage = response.xpath('.//tr/td/text()').extract()
        if column in webpage:
            return webpage[webpage.index(column)+1]
    def parse(self, response):

        yield {
            'University': 'Edinburgh',
            'Department': self.recognize(response,'School'),
            # 'Course title': self.recognize(response,'Pre-requisites'),
            'Professor': self.recognize(response,'Course organiser'),
            # 'Objective':'',
            'Prerequisite':self.recognize(response,'Pre-requisites'),
            # 'Required Skills':'',
            # 'Outcome':'',
            # 'References':'',
            # 'Scores':response.xpath('//td/text()')[87].get(),
            'Description':self.recognize(response,'Course description'),
            'University Homepage': "https://www.ed.ac.uk/",
            # 'course Homepage':'',
            'Professor Email':''
        }
