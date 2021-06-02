import scrapy


class QuotesSpider(scrapy.Spider):
    name = "Edinburgh"

    def start_requests(self):

        # response.xpath('.//td/text()')[98].extract()
        urls = [
            'http://www.drps.ed.ac.uk/20-21/dpt/cxartx08053.htm',
            'http://www.drps.ed.ac.uk/20-21/dpt/cxchem08022.htm',
            'http://www.drps.ed.ac.uk/17-18/dpt/cxcast08004.htm',
            'http://www.drps.ed.ac.uk/17-18/dpt/cxlaws10211.htm',
            'http://www.drps.ed.ac.uk/17-18/dpt/cxelee10006.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def recognize(self,response,column):

        webpage = response.xpath('.//tr/td/text()').extract()
        if column in webpage and  not column == "Email:":
            return webpage[webpage.index(column)+1]

        else:
            webpage = response.xpath('.//text()').extract()
            if column in webpage:
                if column=="Reading List":
                    return webpage[webpage.index(column) + 2]
                elif column == "Email:":
                    return webpage[webpage.index(column) + 1]
                elif column == "Learning Outcomes":
                    temp = webpage[webpage.index(column) + 3]
                    return temp


    def parse(self, response):

        yield {
            'University': 'Edinburgh',
            'Department': self.recognize(response,'School'),
            'Course title': response.xpath('.//h1/text()')[1].getall(),
            'Professor': self.recognize(response,'Course organiser'),
            'Objective':self.recognize(response,'Graduate Attributes and Skills'),
            'Prerequisite':self.recognize(response,'Pre-requisites'),
            # 'Required Skills':'',
            #some bugs below
            'Outcome':self.recognize(response,'Learning Outcomes'),

            'References':self.recognize(response,'Reading List'),
            'Scores': self.recognize(response,'Assessment '),
            'Description':self.recognize(response,'Course description'),
            'University Homepage': "https://www.ed.ac.uk/",
            'Professor Email':self.recognize(response,'Email:')
        }
