import requests
import json
from bs4 import BeautifulSoup as Soup


def transform_district_div(div):
    title = div.parent.select_one(".content .title").text.strip()
    if "No trees posted for removal at this time" in title:
        return None
    img_src = None
    try:
        img_src = div.parent.select_one("img")["src"]
    except:
        pass
    fields = {
        "title": title,
        "district": div.text.strip(),
        "img_src": img_src,
    }
    for strong in div.parent.select("li > strong"):
        label = strong.text.rstrip(":").strip()
        value = strong.parent.text.split("\xa0", 2)[1]
        fields[label] = value
    return fields


if __name__ == "__main__":
    soup = Soup(
        requests.get(
            "https://sfpublicworks.org/tree-removal-notifications",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
            },
        ).text,
        "html5lib",
    )
    # Write out the HTML
    open("tree-list.html", "w").write(soup.select_one("div.tree-list").prettify())
    # Now try to parse it and write out the JSON too
    try:
        divs = soup.select(".district")
        transformed = [transform_district_div(div) for div in divs]
        removals = [r for r in transformed if r]
        open("tree-list.json", "w").write(json.dumps(removals, indent=4))
    except Exception as e:
        print(e)
        pass
