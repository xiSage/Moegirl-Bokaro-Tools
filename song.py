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
    "artists": {},
    "pvs":{}
}
## 标题
song_data["title"] = jdata["defaultName"]
## 作者
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
            song_data["artists"][category][role].append(artist["name"])
## PV
for pv in jdata["pvs"]:
    if pv["pvType"] == "Original":
        service = pv["service"]
        if "pvID" in pv:
            id = pv["pvID"]
        else:
            id = ""
        if "publishDate" in pv:
            date = pv["publishDate"]
        else:
            date = ""
        if service not in song_data["pvs"]:
            song_data["pvs"][service] = []
        song_data["pvs"][service].append({"id":id,"date":date})
print(song_data)
# 确认数据
# song_title = input(f"请输入歌曲标题[{song_title}]：") or song_title
# print(song_title)

