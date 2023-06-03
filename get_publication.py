from bs4 import BeautifulSoup
import requests
import lxml

def main():
    link = input("Input the Google scholar page of the user\n")
#    link = "https://scholar.google.com/citations?user=KiDhcfkAAAAJ&hl=en"
    html = requests.get(link, headers = {'User-agent': 'your bot 0.1'}).text
    publication_names = []
    publication_years = []
    publications_dict = {} #for organizing the data
    content = BeautifulSoup(html, "lxml")
    print(content.prettify())
    publications = content.find_all("a", class_="gsc_a_at")
    years = content.find_all("span", class_="gsc_a_h gsc_a_hc gs_ibl")
    for a_tag in publications:
        publication_name = a_tag.text
        publication_names.append(publication_name)
    for year in years:
        publication_year = year.text
        publication_years.append(publication_year)
    for i in range(len(publication_names)):
        publications_dict[publication_names[i]] = publication_years[i]
    publications_dict = dict(sorted(publications_dict.items(), key=lambda x: x[1], reverse=True))
    size = len(publications_dict)
    print(f"The length of the dictionay is {size}")
    max = int(input("Input the number of publication which you want to get"))
    count = 0
    if max >= size:
        max = size
    with open(f"rudra.txt", "w") as file:
        for publicat in publications_dict:
            if (count < max):
                file.write(f"{publicat} - {publications_dict[publicat]}\n")
                count += 1
            else:
                break

if __name__ == "__main__":
    main()
