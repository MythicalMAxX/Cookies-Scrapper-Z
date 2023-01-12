from requests import get
from bs4 import BeautifulSoup
import re
import csv

def assignment_task(cookie_urls):
    description = []
    result = []
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    for i in range(len(cookie_urls)):

        description_data = get(cookie_urls[i],headers=header).text
        p = BeautifulSoup(description_data, 'lxml')
        descript = p.find_all("div", {"class": "full-width"})
        descript = str(descript)
        p1 = BeautifulSoup(descript, 'lxml')
        desc = p1.find_all("p")
        description.append(desc)
    for ele in description:
        ele = str(ele)
        try:
            ele = ele[14:]
        except:
            ele = "No Data Found"

        if ele != "No Data Found":
            ele = re.sub(r"\B</p>.*$", "", ele)
        result.append(ele)
    return result

def req(url):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    with get(url,headers=header) as response:
        pass

    parser = BeautifulSoup(response.text, 'lxml')
    div = parser.find_all("div", {"class": "accordion-content"})
    div = str(div)
    list1 = div.split("Cookie")

    list2 = []
    for element in list1:
        parser1 = BeautifulSoup(element, 'lxml')
        x = parser1.find_all("a")

        list2.append(x)

    list3 = []
    for element in list2:
        element = str(element)
        element = element.replace("[", "")
        element = element.replace("]", "")

        string = re.search("^<a.*More</a>$", element)
        if string != None:
            list3.append(element)

    cookie_names = []
    urls = []
    for element in list3:
        names = element[18:-10]
        url = element[9:-10]
        cookie_names.append(names)
        urls.append("https://cookiepedia.co.uk"+url)
    return urls, cookie_names

url1 = "https://cookiepedia.co.uk/host/mailchimp.com"
url2 = "https://cookiepedia.co.uk/host/klaviyo.com"
urls1,cookie_names1 = req(url1)
urls2,cookie_names2 = req(url2)
purpose1 = "Targeting/Advertising"
purpose2 = "Unknown"
de1 = assignment_task(urls1)
de2 = assignment_task(urls2)

with open("sample.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Website URL", "Cookie Names", "Purpose", "Description", "Cookie URL"])
    writer.writerow([" ", " ", " ", " ", " "])
    for i in range(len(cookie_names1)):
        writer.writerow([url1,cookie_names1[i],purpose1,de1[i],urls1[i]])

    for i in range(len(cookie_names2)):
        writer.writerow([url2,cookie_names2[i],purpose2,de2[i],urls2[i]])
