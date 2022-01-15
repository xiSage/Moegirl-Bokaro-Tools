import urllib.request
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context
# 获取vocadb数据并存入jdata
vocadb_id = input("请输入vocadbID：")
req = urllib.request.Request(
    f"https://vocadb.net/api/songs/{vocadb_id}?fields=Artists,PVs&lang=Default"
)
with urllib.request.urlopen(req) as response:
    data = response.read().decode("utf-8")
# 数据转存
jdata = json.loads(data)
song_data = {
    "artists": {}
}
song_data["title"] = jdata["defaultName"]
for artist in jdata["artists"]:
    categories =  artist["categories"].split(", ")
    roles = artist["effectiveRoles"].split(", ")
    name = artist["name"]
    for category in categories:
        if  category not in song_data["artists"]:
            song_data["artists"][category] = dict()
        for role in roles:
            if role not in song_data["artists"][category]:
                song_data["artists"][category][role] = []
            song_data["artists"][category][role] = artist["name"]
print(song_data)
# 确认数据
# song_title = input(f"请输入歌曲标题[{song_title}]：") or song_title
# print(song_title)

