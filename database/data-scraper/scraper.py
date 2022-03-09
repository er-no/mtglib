from html.parser import HTMLParser
from io import BytesIO
from os.path import exists
import sys, pycurl, certifi

class MyHTMLParser(HTMLParser):
    """"Scraps html checklist from https://scryfall.com/sets/SET_KEY?as=checklist"""

    inside_table = False
    temporary_ignore = False
    collect_data = False
    data = ""
    cols = 0
    max_cols = 4
    return_string = ""

    def flush_data(self):
        self.return_string += self.data + "\n"
        self.data = ""

    def handle_starttag(self, tag, attr):
        if tag == "table":
            self.inside_table = True

        if tag == "thead":
            self.temporary_ignore = True

        if self.inside_table and tag == "tr":
            self.collect_data = True
            self.cols = 0

        if self.inside_table and tag == "td":
            self.cols += 1

    def handle_endtag(self, tag):
        if tag == "table":
            self.inside_table = False
            self.collect_data = False
            self.data = ""

        if tag == "thead":
            self.temporary_ignore = False

        if self.inside_table and tag == "tr":
            self.collect_data = False
            self.flush_data()

        if self.inside_table and tag == "td":
            if self.cols >= self.max_cols:
                self.collect_data = False
            else:
                self.data += ";"

    def handle_data(self, data):
        data = data.strip()
        if self.collect_data and not self.temporary_ignore:
            self.data += data.replace("{", "[").replace("}", "]")

def fetch_html(url):
    print("connecting to: " + url)
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    print("success! data fetched...")
    body = buffer.getvalue()
    return body.decode('utf-8')

def scrape(url):
    parser = MyHTMLParser()
    input = fetch_html(url)
    parser.feed(input)
    return parser.return_string
    # print(input)

def main(set_code, file):
    print("will fetch data for: ", set_code)
    url = "https://scryfall.com/sets/" + set_code.lower() + "?dir=asc&as=checklist"
    csv_header = "set;number;name;cost\n"
    csv_body = scrape(url).strip() + "\n"
    file.write(csv_header + csv_body)
    print("data compiled, written to: " + file.name)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("will connect to scryfall website to fetch set details, please provide set key (STX, NEO etc) and a file name for output")
        print("usage: py scraper.py XXX [output_file]")
    elif len(sys.argv[1]) != 3:
        print("please provide an mtg expansion code, that is 3 letters")
    elif exists(sys.argv[2]):
        print("output file exists, this program will never overwrite!")
    elif len(sys.argv[1]) == 3 and not exists(sys.argv[2]):
        main(sys.argv[1].upper(), open(sys.argv[2], "w"))
    else:
        print("something went wrong......")
