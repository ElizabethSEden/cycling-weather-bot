from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from settings import REGION_CODE, REGION_NAME
from datetime import date

class NoWarningsException(Exception):
    pass

def get_weather_warning():
    try:
        return WarningDetails(REGION_CODE, REGION_NAME) #get warning for London and South East
    except NoWarningsException:
        return None

class WarningDetails:
    def __init__(self, region_code, region_name):
        self.region_name = region_name
        soup = self.get_soup(region_code)
        if self.is_region_affected(soup):
            warningMatrixTable = soup.find("table", class_="warningsMatrixInner")
            if warningMatrixTable is None:
                raise NoWarningsException
            self.colour = self.get_colour(warningMatrixTable)
            self.event = self.get_event(soup.find("span", class_="wxDetails"))
            self.time_from = self.get_times(soup.find("span", class_="wxDetails"))[0]
            if (self.time_from.split('T')[0] != date.today().isoformat()):
               raise NoWarningsException
            elif (int(self.time_from.split('T')[1].split(':')[0]) > 22):
                raise NoWarningsException
            self.time_to = self.get_times(soup.find("span", class_="wxDetails"))[1]
            likelihood = 1
            for tr in warningMatrixTable.find_all("tr"):
                if tr.find_all("td", class_="selected"):
                    self.impact = self.get_impact(tr)
                    self.likelihood = self.get_likelihood(likelihood)
                    break
                likelihood += 1
        else:
            raise NoWarningsException

    def get_soup(self, region_code):
        req = Request(
            'http://www.metoffice.gov.uk/public/weather/warnings#?region={}'.format(region_code),
            headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read()
        return BeautifulSoup(data, "html.parser")

    def is_region_affected(self, soup):
        regions = soup.find_all("div", class_="localAuthoritiesTitle")
        if any([tag.contents[0] for tag in regions if tag.contents[0]==self.region_name]):
            return True
        return False

    def __str__(self):
        return "{} warning of {} - {} a {} impact.".format(self.colour.capitalize(), self.event, self.likelihood, self.impact)

    def get_colour(self, warningMatrixTable):
        selected_td = warningMatrixTable.find("td", class_="selected")
        for attribute in selected_td["class"]:
            if attribute == "yellow":
                return "yellow"
            elif attribute == "amber":
                return "amber"
            elif attribute == "red":
                return "red"

    def get_event(self, warning):
        return warning.find("span", class_="wxType").contents[0].lower()

    def get_times(self, warning):
        return [x["datetime"] for x in warning.find_all("time")]

    def get_likelihood(self, likelihood):
        dict = {
            1:"there will be",
            2:"there is likely to be",
            3:"there might be",
            4:"there's a very small chance of",
        }
        return dict[likelihood]

    def get_impact(self, tr):
        impact = 0
        dict = {
                1:"low",
                2:"medium",
                3:"high",
            }
        for td in tr.find_all("td"):
            if "selected" in td['class']:
                return dict[impact]
            impact += 1
