from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import json


session = HTMLSession()

def get_data_details(element, headers):
    response = {}
    elements = element.find("tr", {"class": "propspt"}).find_all("td")
    for i in range(1, len(headers)):
        response[headers[i].text] = elements[i].text
    return response


def get_groupspt_data(element, headers):
    response = {}
    elements = element.find_all("td", {"class": "name"})
    for el in elements:
        response[el.text] = get_data_details(element, headers)
    return response


def process_groupspt_data(list_of_data):
    data_holder = {}
    for element in list_of_data:
        headers = element.find("tbody").find("tr", {"class": "pagehead"}).find_all("td")
        category = headers[0].text
        data_holder[category] = get_groupspt_data(element, headers)
    return data_holder


def get_head_and_feature_data(group_head_elements, text_feature_elements):
    response = {}
    for i in range(len(group_head_elements)):
        response[group_head_elements[i].text] = text_feature_elements[i].text
    return response

def process_group_feature(data, group_feature_elements):
    for group_element in group_feature_elements:
        group_head_elements = group_element.find_all("div", {"class": "grouphead"})
        text_feature_element = group_element.find_all("div", {"class": "textfeature"})
        page_head = group_element.find("div", {"class": "pagehead"}).text
        data[page_head] = get_head_and_feature_data(group_head_elements, text_feature_element)
    return data;


def get_page(page):
    # we create a session that will link us with the website we want to scrap by providing the url
    session = HTMLSession()
    # this is the page size that specifies how many elements we want to take
    page_size = 50
    # here we make the get request using the session variable and the url to get back the html file
    source = session.get("https://www.campusplastics.com/campus/list/" + str(page * page_size))
    try:
        source.raise_for_status()
    except:
        print("ERROR")
    soup = BeautifulSoup(source.text, 'html.parser')
    list_of_elements = soup.find_all("div", {"class": "row row-grade"})
    response = []
    for elements in list_of_elements:
        # here we get all the elements that have the tag a
        # from the list of 'a' tags we want to get the second one because it has the
        # url to the page we want to get the data
        link = elements.find_all('a')[1]

        # from the 'a' tag we get the 'href' attribute that has the url in it
        raw_url = link['href']

        # from all the value of 'href' we want only the part after 'datasheet/' which
        # is the url of the page
        url = raw_url.split("datasheet/")[1]
        # here we store the text of the 'a' tag which we will use do show in the html page
        title = link.text

        # here we add the extracted data from the 'a' tag and append it to the list we
        # created
        response.append({
            "href_url": url,
            "title": title
        })
        # here we return the list of data we created
    return response


def get_data_from_url(param):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    url = "https://www.campusplastics.com/campus/en/datasheet/" + param
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    projects_soup = BeautifulSoup(html, 'lxml')

    group_spt_elements = projects_soup.find_all("div", {"class": "groupspt"})
    group_feature_elements = projects_soup.find_all("div", {"class": "groupfeature"})

    data = process_groupspt_data(group_spt_elements)
    data = process_group_feature(data, group_feature_elements)
    return data


# data = get_data_from_url("Akulon®+K224-KGM35/DSM/50/5c85ec01/SI/?pos=101&campus-main=acvs1is96mqgq8pfacsrcg7gk1")
# print(data)