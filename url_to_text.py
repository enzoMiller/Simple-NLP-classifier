import urllib
from lxml import etree
import string



class Url_to_texts:
    def __init__(self, url):
        self.url = url
        self.list_title_urlPDF_summary_category = self.parse_api(url)

    def parse_api(self, url):
        output_list = []
        data_api = urllib.urlopen(url).read()
        tree = etree.fromstring(data_api)
        for entry in tree.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = entry.find(".//{http://www.w3.org/2005/Atom}title").text
            id_of_entry = entry.find(".//{http://www.w3.org/2005/Atom}id").text
            url_pdf = string.replace(id_of_entry, "abs", "pdf") + ".pdf"
            summary = entry.find(".//{http://www.w3.org/2005/Atom}summary").text
            category = entry.find(".//{http://www.w3.org/2005/Atom}category").get("term")

            #for category in entry.findall(".//{http://www.w3.org/2005/Atom}category term"):
             #   print(1)
            #print(summary+title)

            output_list.insert(0, {'title': title,
                                   'url_pdf': url_pdf,
                                   'summary': summary,
                                   'category': category })
        return output_list
