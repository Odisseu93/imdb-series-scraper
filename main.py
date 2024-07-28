import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import json


def make_a_soup(url):
    headers = {
        # "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    website = requests.get(url, headers=headers)
    if website.status_code != 200:
        print(f"Failed to get response from {url}: {website.status_code}")
        return False

    soup = BeautifulSoup(website.content, "html.parser")

    return soup


def get_episode_data(soup):
    episodes = []
    has_episodes = soup

    if not has_episodes:
        print(f"No episodes found")
        return False

    episode_containers = soup.find_all("div", class_="ipc-list-card")

    if not episode_containers:
        return False

    for container in episode_containers:
        episode_data = {}

        thumbnail = container.img["src"]
        title = container.find("h4").text
        description = getattr(
            container.find(class_="ipc-html-content-inner-div"), "text", ""
        )

        episode_data["title"] = title
        episode_data["thumbnail"] = thumbnail
        episode_data["description"] = description

        episodes.append(episode_data)
    return episodes


def get_series_name(title_id):
    base_url = "https://www.imdb.com/title/"
    has_name = make_a_soup(base_url + str(title_id))

    if not has_name:
        print("Invalid title_id or not found  series name")
        return False

    name = "_".join(str(make_a_soup(base_url + str(title_id)).h1.text).lower().split())
    return name


def get_imdb_series_data(title_id):
    seasons = []
    season_number = 1
    base_url = "https://www.imdb.com/title/"

    def get_url(season_number):
        url = base_url + title_id + "/episodes/?season=" + str(season_number)
        return url

    def has_content():
        return make_a_soup(get_url(season_number))

    # get episodes for all seasons in the series until no episodes are found in the current season page
    while get_episode_data(has_content()):
        print("Season " + str(season_number) + " scraping finished.")
        current_season = {}
        current_season["season_number"] = season_number
        current_season["episodes"] = get_episode_data(
            # base_url
            # + title_id
            # + "/epsodes/?season="
            # + str(season_number)
            make_a_soup(get_url(season_number))
            #
        )

        seasons.append(current_season)
        season_number += 1

    print("Process completed!")
    return seasons


def find_series():
    query = input("Search IMDb: ")

    base_url = "https://www.imdb.com/find?q="
    soup = make_a_soup(base_url + query)
    search_list = soup.find("ul", class_="ipc-metadata-list")
    series_list_id = []

    if not search_list:
        print("No series found")
        return False
    series_list = search_list.find_all("a", href=True)

    for series in series_list:
        title = series.text.strip()
        id = series["href"].split("/")[2]
        if title and id:
            print(f"{title} - {id}")
        if id:
            series_list_id.append(id)
    return series_list_id


def main():
    output_dir = "data"
    path = Path(output_dir)

    if not os.path.exists(path):
        os.makedirs(path)

    def search_series():
        find_series()

    def menu():
        print("")
        print("Choose an option:")
        print("1. Find series")
        print("2. Get series data")
        print("3. Exit")
        print("")

        choice = input("Enter your choice (1-3): ")
        if not choice.isdigit():
            return 0
        return int(choice)

    while True:
        choice = menu()
        if choice == 1:
            search_series()
        elif choice == 2:
            series_id = input("Enter the series ID an press enter (i.g tt0386676): ")
            name = get_series_name(title_id=series_id)
            if name:
                data = get_imdb_series_data(title_id=series_id)
                has_data = len(data) > 0
                if not has_data:
                    print("No has data")
                    exit()
                file_directory_path = os.path.join(output_dir, name + ".json")
                with open(
                    file_directory_path,
                    "w",
                    encoding="utf8",
                ) as f:
                    title = {"title": name}
                    data.insert(0, title)
                    f.write(json.dumps(data, ensure_ascii=False))
                f.close()
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


main()

