import json
from pyyoutube import Api

from wordcloud import WordCloud

import matplotlib.pyplot as plt

import os

f = open("tokens.json", "r")
data = json.load(f)
ytkey = data["youtube"]
f.close()

api = Api(api_key=ytkey)

try:
    print("Making output directory...")
    os.mkdir("./output/")
    print("Success!")
except FileExistsError:
    print("Directory already exists.")
    pass

id = input("Input a channel ID/Name: ")

# Get the channel's uploads playlist ID, usually the same as the channel, but best to be sure
# Use ID or username
try:
    if id.startswith("UC"):
        chan = api.get_channel_info(channel_id=id).items[0].to_dict()
    else:
        chan = api.get_channel_info(channel_name=id).items[0].to_dict()
except TypeError:
    print("Error: Could not find channel")
    exit()
name = chan["snippet"]["title"]
chanuploads = chan["contentDetails"]["relatedPlaylists"]["uploads"]
print("Uploads Playlist ID: ", chanuploads)

# Get the playlist
plist = api.get_playlist_items(playlist_id=chanuploads, count=None).items
print("Playlist: ", plist)

titles = []

for i in plist:
    titles.append(i.to_dict()["snippet"]["title"])

titles_joined = " ".join(titles)

wordcloud = WordCloud().generate(titles_joined)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

plt.savefig("./output/" + name + " - " + id + ".png")

print("\n\n\n")
print("==============================")
print("Channel ID:", id)
print("Channel Name:", name)
print("Saved wordcloud to: ./output/" + name + " - " + id + ".png")
print("==============================")

plt.show()
