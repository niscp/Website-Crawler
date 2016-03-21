__author__ = 'nishank'

from bs4 import BeautifulSoup
import urllib2

website = "http://www.justdial.com/"
class Restaurant:

    def __init__(self,location= None,area = None,page=None):
        self.location = location
        self.area = area
        self.page = page



    def getAll(self):
        restaurant_list = []
        try:
            ####### Checking which URL to hit
            if self.area is not None:
                url = website + str(self.location) + "/restaurants-<near>-"+self.area+"/ct-304085/page-"+ str(self.page)
            else:
                url = website + str(self.location) + "/Restaurants/page-" + str(self.page)
            content = urllib2.urlopen(url).read()
            ## soup object to serve us
            soup = BeautifulSoup(content, "lxml")

            ## capturing the DOM elements

            item = soup.find_all('div', class_="store-details")
            address = soup.find_all('span', class_="desk-add")
            contact = soup.find_all('p', class_="contact-info")
            for j,k,l in zip(address,item,contact):
                address = (j.get_text())
                name = k.h4.span.a.get_text()
                rating = k.ul.li.span.get_text()
                contact = l.span.a.get_text()

            ## decode the names before passing to HTML pages


                address = address.encode('utf-8',errors='ignore')
                name = name.encode('utf-8',errors='ignore')
                rating = rating.encode('utf-8',errors='ignore')
                contact = contact.encode('utf-8',errors='ignore')
                address = address.translate(None,'\t\n')
                restaurant_list.append({'name':name,
                                          'rating':rating,
                                            'address':address,
                                            'contact':contact
                                        })

        except Exception as exception:
                return 'Error caught',exception
        return restaurant_list


