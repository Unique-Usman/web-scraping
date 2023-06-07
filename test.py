from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import lxml
import time

def scrap(html):
#    link = input("Input the Google scholar page of the user\n")
#    link = "https://scholar.google.com/citations?user=KiDhcfkAAAAJ&hl=en"
    sub_link = "https://scholar.google.com"
#   html = requests.get(link, headers = {'User-agent': 'your bot 0.1'}).text
    publication_names = []
    publication_years = []
    publication_abstracts = []
    publications_dict = {} #for organizing the data
    content = BeautifulSoup(html, "lxml")
#    print(content.prettify())
    publications = content.find_all("a", class_="gsc_a_at", limit=None)
    years = content.find_all("span", class_="gsc_a_h gsc_a_hc gs_ibl", limit=None)
    print(len(years))
    for a_tag in publications:
        publication_name = a_tag.text
        publication_abstract = a_tag["href"]
        publication_names.append(publication_name)
        publication_abstract_link = sub_link + publication_abstract
        publication_abstract_html = requests.get(publication_abstract_link, headers = {'User-agent': 'your bot 0.1'}).text
        publication_abstract_content = BeautifulSoup(publication_abstract_html, "lxml")
        abstract = publication_abstract_content.find("div", class_="gsh_csp")
        if abstract == None:
            abstract = publication_abstract_content.find("div", class_="gsh_small")
            publication_abstracts.append(abstract.text if abstract else "None")
        else:
            publication_abstracts.append(abstract.text)
    for year in years:
        publication_year = year.text
        publication_years.append(publication_year)
    for i in range(len(publication_names)):
        publications_dict[publication_names[i]] = f"{publication_years[i]}\n{publication_abstracts[i]}"
    publications_dict = dict(sorted(publications_dict.items(), key=lambda x: int(x[1][0:4]) if (x[1][0:4]).isnumeric() else 2023, reverse=True))
    size = len(publications_dict)
    print(f"The length of the publication is {size}")
    max = int(input("Input the number of publication which you want to get\n"))
    count = 0 
    if max >= size:
        max = size
    with open(f"result.txt", "w") as file:
        for publicat in publications_dict:
            if (count < max):
                file.write(f"{count + 1}. {publicat} - {publications_dict[publicat]}\n\n")
                count += 1
            else:
                break

# Set up Selenium webdriver
driver = webdriver.Chrome()  # Replace with the appropriate webdriver for your browser
driver.get("https://scholar.google.com/citations?user=BR6HchkAAAAJ&hl=en&oi=ao")  # Replace with the URL of the page you want to download

# Scroll down the page to load additional content
SCROLL_PAUSE_TIME = 2  # Adjust as needed
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get the full HTML source code of the page
html = driver.page_source

# Close the browser
driver.quit()

scrap(html)

# Save the HTML source code to a file
#with open("page.html", "w", encoding="utf-8") as file:
 #   file.write(html)

