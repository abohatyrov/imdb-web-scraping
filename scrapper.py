import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
headers = {
    "Accept": "*/*",
    "Accept-Language": "en,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "User-Agent": "YOUR USER-AGENT"
}

df = pd.DataFrame(
    columns=[
        "title", 
        "year", 
        "genres",
        "description",
        "director",
        "stars",
        "certificate", 
        "duration",
        "imdb_rating",
        "metascore_rating",
        "votes",
        "gross",
        "poster"
    ]
)
    
pages = 0
films = 1
    
run = True
while run:
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    data = soup.find_all("div", class_="lister-item mode-advanced")

    for item in data:
        try:
            img = item.find("img", class_="loadlate")["src"]
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No image to film {films}\n")
            
        try:
            header = item.find("h3", class_="lister-item-header").contents[3].text
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No title to film {films}\n")
            
        try:
            year = int(item.find("h3", class_="lister-item-header").contents[5].text[-5: -1])
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No year to film {films}\n")
            
        try:
            certificate = item.find("span", class_="certificate").text
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No certificate to film {films}\n")
            
        try:
            duration = int(item.find("span", class_="runtime").text.split()[0]) * 60
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No duration to film {films}\n")
            
        try:
            genres = item.find("span", class_="genre").text.strip()
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No genres to film {films}\n")
            
        try:
            imdb_rating = float(item.find("div", class_="ratings-imdb-rating")["data-value"])
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No imdb_rating to film {films}\n")
            
        try:
            metascore_rating = int(item.find("span", class_="metascore").text)
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No metascore_rating to film {films}\n")
            
        try:
            description = item.find_all("p", class_="text-muted")[1].text.strip()
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No description to film {films}\n")
            
        try:
            director = item.find("p", class_="").contents[1].text
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No director to film {films}\n")
            
        try:
            stars = ", ".join([i.text for i in item.find("p", class_="").contents[5:] if "\n" not in i])
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No stars to film {films}\n")
            
        try:
            votes = int(item.find("p", class_="sort-num_votes-visible").contents[3]["data-value"])
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No votes to film {films}\n")
            
        try:
            gross = int("".join(item.find("p", class_="sort-num_votes-visible").contents[9]["data-value"].split(",")))
        except:
            with open("exception.txt", "a", encoding="utf-8") as f: f.write(f"No gross to film {films}\n")


        lst = [ header, year, genres, description, director, stars, certificate, duration, imdb_rating, metascore_rating, votes, gross, img ]
        df.loc[len(df.index)] = lst
        films += 1

    pages += 1
    print(pages, end=", ")
    
    try:
        url = "https://www.imdb.com/" + soup.find("a", class_="lister-page-next next-page")["href"]
    except:
        run = False

print("Success!")

df.to_csv("data.csv", index=False)
