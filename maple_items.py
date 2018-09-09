# Example of connecting to API to pull images from an online game

import requests
import json
import pandas as pd
from collections import OrderedDict

# Load json from api
link = "https://labs.maplestory.io/api/gms/latest/item"
f = requests.get(link)
all_items = f.text
parsed_json = json.loads(all_items)

aDict = {}

for item in parsed_json:
	aDict[item["Name"]] = item["Id"]

# Read item list
df = pd.read_csv('maple_items.csv', header=None)
wanted_list = list(df[0])

bDict = OrderedDict()

# Pull image per item in list
for item in wanted_list:
	try:
		item_id = aDict[item.strip()]
		full_url = "https://labs.maplestory.io/api/gms/latest/item/" + str(item_id) + "/icon"
		bDict[item] = '=IMAGE(\"' + full_url + '\", 3)'
	except:
		bDict[item] = "None"

final_df = pd.DataFrame(bDict.items(), columns=['Item Name', 'URL'])

# Output list of image links
final_df.to_csv("item_pics.csv", index=False)

