from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Launch url
url = "https://otakustream.tv/"

# Create a new Firefox session
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

driver = webdriver.Firefox(firefox_profile=profile)
driver.get(url)

# xpath to our desired content : Popular Anime
xpath = "/html/body/div[2]/div[1]/header/div/div/ul[2]/li[2]/a"

# find the button and redirect to Popular Anime page
popular_anime_list_button = driver.find_element_by_xpath(xpath)
popular_anime_list_button.click()

# now we use BS to find our contents
soup = bs(driver.page_source, "lxml")

anime_list = []
anime_article = soup.find_all("article", {"class": "article-block"})

for article in anime_article:
    article_details_div = article.find("div", {"class": "inner"})
    title = article_details_div.find("a").get_text()
    summary = article_details_div.find("span", {"class": "summary"}).get_text()
    tds = article_details_div.find_all("td")
    status = tds[3].get_text()
    genre = [e.get_text() for e in tds[7].find_all("a")]
    anime = {
        "title": title,
        "summary": summary,
        "status": status,
        "genre": genre
    }

    anime_list.append(anime)

# Open and write our results in file.txt
result_file = open("webscrape_result.txt", "w")
result_file.write("Top 20 animes based on views count on otakustream.tv \n")

for item in anime_list:
    result_file.write("\n")
    result_file.write(item["title"] + "\n")
    result_file.write("Summary : " + item["summary"] + "\n")
    result_file.write("Status : " + item["status"] + "\n")
    result_file.write("Genre : " + ",".join(item["genre"]).strip("[]") + "\n")