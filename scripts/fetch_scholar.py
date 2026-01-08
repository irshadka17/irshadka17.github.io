import requests
from bs4 import BeautifulSoup
import json
import re

USER_ID = "3aPgewgAAAAJ"   # Your Google Scholar ID
URL = f"https://scholar.google.com/citations?user={USER_ID}&hl=en&view_op=list_works&sortby=pubdate"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

print("Fetching Google Scholar page...")
html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "lxml")

# ---------------------------
# Extract metrics
# ---------------------------
metrics_table = soup.find("table", id="gsc_rsb_st")
cells = metrics_table.find_all("td", class_="gsc_rsb_std")

total_citations = int(cells[0].text.strip())
h_index = int(cells[2].text.strip())
i10_index = int(cells[4].text.strip())

# ---------------------------
# Extract citations per year
# ---------------------------
citations_per_year = {}
script_tags = soup.find_all("script")

for script in script_tags:
    if "google.visualization.arrayToDataTable" in script.text:
        rows = re.findall(r"\['(\d{4})',\s*(\d+)\]", script.text)
        for year, cites in rows:
            citations_per_year[year] = int(cites)

# ---------------------------
# Extract publications
# ---------------------------
publications = []
rows = soup.find_all("tr", class_="gsc_a_tr")

for row in rows:
    title_tag = row.find("a", class_="gsc_a_at")
    if not title_tag:
        continue

    title = title_tag.text.strip()

    cit_tag = row.find("a", class_="gsc_a_ac")
    cited_by = int(cit_tag.text.strip()) if cit_tag and cit_tag.text.strip().isdigit() else 0

    publications.append({
        "title": title,
        "cited_by": cited_by
    })

# ---------------------------
# Save JSON
# ---------------------------
data = {
    "metrics": {
        "total_citations": total_citations,
        "h_index": h_index,
        "i10_index": i10_index,
        "citations_per_year": citations_per_year
    },
    "publications": publications
}

with open("_data/scholar.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved to _data/scholar.json")
