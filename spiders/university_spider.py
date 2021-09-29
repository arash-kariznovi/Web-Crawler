from urllib.parse import urljoin
import re
import scrapy


class UniversitySpider(scrapy.Spider):
    name = "Edinburgh"

    def start_requests(self):
        urls = [
            'http://www.drps.ed.ac.uk/20-21/dpt/cx_schindex.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        colleges = response.css("li a").xpath("@href").extract()
        for c in colleges:
            url = urljoin(response.url, c)
            yield scrapy.Request(url, callback=self.parse_college)

    def parse_college(self, response):
        schools = response.css("li a").xpath("@href").extract()
        for s in schools:
            url = urljoin(response.url, s)
            yield scrapy.Request(url, callback=self.parse_course)

    def parse_course(self, response):
        courses = response.css("table.content td table tr td a").xpath("@href").extract()
        for c in courses:
            url = urljoin(response.url, c)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        rows = response.css("table.sitstablegrid tr")
        University = 'Edinburgh'
        Abbreviation = 'Edin'
        Outcome = response.css("ol li::text").extract()
        University_Homepage = "https://www.ed.ac.uk/"
        for row in rows:
            School = row.xpath("//td[contains(text(), 'School')]/following-sibling::td[1]/text()").extract()
            College = row.xpath("//td[contains(text(), 'College')]/following-sibling::td[1]/text()").extract()
            Course_title = response.css('h1.sitspagetitle::text').extract()
            Degree, Course_title = str(Course_title).split(': ')
            Degree = re.sub('\[\'', '', str(Degree))
            Course_title = re.sub('\']', '', str(Course_title))
            Professor = row.xpath("//td[contains(text(), 'Course organiser')]"
                                  "/following-sibling::td[1]/text()").extract()
            info = str(Professor).splitlines()[0]
            info = re.sub('\\n', '', info)
            info = info.split(',')
            ProfessorName, ProfessorPhoneNumber, ProfessorEmail = re.sub('\[\'', '', info[0]), re.sub('\'', '', info[2]), re.sub('\']', '', info[4])
            ProfessorName = re.sub('\'', '', str(ProfessorName))
            ProfessorPhoneNumber = re.sub('\'', '', str(ProfessorPhoneNumber))
            ProfessorEmail = re.sub('\'', '', str(ProfessorEmail))
            Objective = row.xpath("//td[contains(text(), 'Summary')]/following-sibling::td[1]/text()").extract()
            Pre_requisites = row.xpath("//td[contains(text(), 'Pre-requisites')]"
                                       "/following-sibling::td[1]/text()").extract()
            Pre_requisites = re.sub('\'', '', str(Pre_requisites))
            Co_requisites = row.xpath("//td[contains(text(), 'Co-requisites')]"
                                      "/following-sibling::td[1]/text()").extract()
            Co_requisites = re.sub('\'', '', str(Co_requisites))
            Other_requirements = row.xpath("//td[contains(text(), 'Other requirements')]"
                                           "/following-sibling::td[1]/text()").extract()
            References = ''
            tables = response.css("table.sitstablegrid")
            for tab in tables:
                if tab.css("caption::text")[0].extract() == 'Reading List':
                    References = tab.css("tr td::text").extract()
            Scores = row.xpath("//td[contains(text(), 'Assessment')]"
                               "/following-sibling::td[1]/text()").extract()
            Scores = re.sub('\s+', ' ', str(Scores))
            Scores = re.sub('\\n', ' ', str(Scores))
            Scores = str(Scores).strip('\n')
            Course_description = row.xpath("//td[contains(text(), 'Course description')]"
                                           "/following-sibling::td[1]/text()").extract()
            Course_description = re.sub('\s+', ' ', str(Course_description))
            Course_description = re.sub('\\n', ' ', str(Course_description))
            Course_description = str(Course_description).strip('\n')
            Projects = row.xpath("//td[contains(text(), 'Additional Information (Assessment)')]"
                                 "/following-sibling::td[1]/text()").extract()
            Projects = re.sub('\\n', ' ', str(Projects))
            Projects = re.sub('\'', ' ', str(Projects))
            Projects = str(Projects).strip('\n')
            Course_Homepage = response.url
        yield {
            "University": University,
            "Abbreviation": Abbreviation,
            "School": School,
            "College": College,
            "Degree": Degree,
            "Course_title": Course_title,
            "Professor_Name": ProfessorName,
            "Professor_PhoneNumber": ProfessorPhoneNumber,
            "Professor_Email": ProfessorEmail,
            "Objective": Objective,
            "Pre_requisites": Pre_requisites,
            "Co_requisites": Co_requisites,
            "Required Skills": Other_requirements,
            "Outcome": Outcome,
            "References": References,
            "Scores": Scores,
            "Description": Course_description,
            "Projects": Projects,
            "University_Homepage": University_Homepage,
            "Course_Homepage": Course_Homepage,
        }
