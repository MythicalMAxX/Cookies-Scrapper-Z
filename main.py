from requests import get
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import csv

def get_hostname(description):
    service_providers = ["Quantcast", "Google Analytics service", "Google Website Optimizer",
                         "Google Universal Analytics",
                         "Akamai", "Kissmetrics analytics service", "Mint Analytics software", "CloudFlare", "OneTrust"]
    if description != "":
        for element in service_providers:
            if element in description:
                host = element
                break
    elif description == "":
        host = "Data Not Available"

    try:
        return host
    except:
        return "Unknown"

def get_description(cookie_urls):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    description_data = get(cookie_urls, headers=header).text
    p = BeautifulSoup(description_data, 'html.parser')
    descript = p.find_all("div", {"class": "full-width"})
    descript = str(descript)
    p1 = BeautifulSoup(descript, 'lxml')
    desc = p1.find_all("p")
    desc = re.sub('<[^<]+?>', '', str(desc))
    desc = re.sub(r",\sThe\smain\spurpose.*$", "", str(desc))
    desc = desc.replace("\n","")
    try:
        desc = desc[4:]
    except:
        desc = "No Resources Found"

    if desc == "":
        desc = "No Resources Found"
    return desc

raw_output = []

def create_entry(dict, url):
    cookie_url = "https://cookiepedia.co.uk/cookies/" + dict["Cookiename"]
    dict["Cookie URL"] = cookie_url
    dict["URL"] = url
    if dict["Purpose"]=="Targeting/AdvertisingCookie name":
        dict["Purpose"] = "Targeting/Advertising"
    about_cookies = get_description(cookie_url)
    host_name = get_hostname(about_cookies)
    if dict["Cookiename"]=="_mcid" and (dict["Is Secure"] == "No" or dict["Is HTTP Only"]=="No"):
        pass
    elif dict["Cookiename"]=="QA" and (dict["Is Secure"] == "No" and dict["Is HTTP Only"]=="No"):
        pass

    else:
        writer.writerow([url, dict["Cookiename"],host_name, dict["Purpose"], about_cookies, cookie_url,dict["Is Secure"],dict["Is HTTP Only"],dict["Path"]])

        My_dictionary = {"Url":url,"Cookie Name":dict["Cookiename"],"Host Name":host_name,"Purpose":dict["Purpose"],"Description":about_cookies,"Cookie URL": cookie_url,"Is Secure":dict["Is Secure"],"Is HTTP Only":dict["Is HTTP Only"],"Path":dict["Path"]}
        raw_output.append((My_dictionary))


def req(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    with get(url, headers=header) as response:
        pass

    parser = BeautifulSoup(response.text, 'html.parser')
    div = parser.find_all("div", {"class": "accordion-content"})
    div = re.sub('<[^<]+?>', '', str(div))
    div = div.replace(" ", "")
    div = div.replace("\r", "")
    div = div.replace("\n", "")
    div = div.replace("[", "")
    div = div.replace("]", "")
    div = div.replace("AdvertisingCookiename", "AdvertisingMoreCookiename")
    div = div.replace("UnknownCookiename", "UnknownMoreCookiename")
    div = div.replace("Advertising,Cookiename", "AdvertisingMoreCookiename")
    div = div.replace("Unknown,Cookiename", "UnknownMoreCookiename")

    list1 = div.split("More")
    data = []
    for strings in list1:
        string = re.sub(r"AboutthisCookie.*$", "", str(strings))
        string = string.replace("/Purpose:", "/ ||Purpose:")
        string = string.replace("?", ":")
        string = string.replace("Is", "||Is")
        string = string.replace("Path", "||Path")
        string = string.replace("||", ",")
        string = string.replace("IsSecure:", "Is Secure,")
        string = string.replace("IsHTTPOnly:", "Is HTTP Only,")
        string = string.replace("Path:", "Path,")
        string = string.replace("Purpose:", "Purpose,")
        string = string.replace("Cookiename:", "Cookiename,")

        data.append(string)
    data = list(OrderedDict.fromkeys(data))
    if data[len(data)-1] == "":
        data.pop()
    return data

url1 = "https://cookiepedia.co.uk/host/mailchimp.com"
url2 = "https://cookiepedia.co.uk/host/klaviyo.com"
data1 = req(url1)
data2 = req(url2)

with open("sample.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Website URL", "Cookie Names","Host", "Purpose", "Description", "Cookie URL","Is Secure","Is HTTP only?","Path"])
    writer.writerow([" ", " ", " ", " ", " "])
    for entries in data1:
        entries = list(entries.split(","))
        dict1 = {entries[i]: entries[i + 1] for i in range(0, len(entries) - 1, 2)}
        print(dict1)
        create_entry(dict1, url1)
    for entries in data2:
        entries = entries.replace(",Cookie","Cookie")
        entries = list(entries.split(","))
        dict2 = {entries[i]: entries[i + 1] for i in range(0, len(entries), 2)}
        create_entry(dict2, url2)

print(raw_output)
print(len(raw_output))
