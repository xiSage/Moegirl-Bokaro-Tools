import urllib.request
import ssl
import json
import langid
from dateutil.parser import isoparse


def lang_detect(text):
    """格式化文本，若为日语则返回{{lj|text}}，否则返回text

    Args:
        text (string): 需要格式化的文本

    Returns:
        string: 格式化后的文本
    """
    print(langid.classify(text))
    if langid.classify(text)[0] == "ja":
        return f"{{{{lj|{text}}}}}"
    return text


def load_vocadb(id):
    """从vocaDB歌曲API获取json数据

    Args:
        id (int): 要查询的vocaDB歌曲页面ID

    Returns:
        dict: 从vocaDB获取的数据
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(
        f"https://vocadb.net/api/songs/{id}?fields=Artists,PVs&lang=Default"
    )
    with urllib.request.urlopen(req) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


def format_data(raw_data):
    """整理从vocaDB获取的歌曲数据格式

    Args:
        raw_data (dict): 从vocaDB获取的数据

    Returns:
        dict: 整理后的数据
    """
    formatted_data = {
        "artists": {},
        "pvs": {}
    }
    # 标题
    formatted_data["title"] = raw_data["defaultName"]
    # 作者
    for artist in raw_data["artists"]:
        categories = artist["categories"].split(", ")
        roles = artist["effectiveRoles"].split(", ")
        name = artist["name"]
        for category in categories:
            if category not in formatted_data["artists"]:
                formatted_data["artists"][category] = dict()
            for role in roles:
                if role not in formatted_data["artists"][category]:
                    formatted_data["artists"][category][role] = []
                formatted_data["artists"][category][role].append(
                    artist["name"])
    # PV
    for pv in raw_data["pvs"]:
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
            if service not in formatted_data["pvs"]:
                formatted_data["pvs"][service] = []
            formatted_data["pvs"][service].append({"id": id, "date": date})

    return formatted_data

def to_wikitext(id):
    jdata = load_vocadb(id)
    song_data = format_data(jdata)
    print(song_data)

def start():
    vocadb_id = input("请输入vocadbID：")
    to_wikitext(vocadb_id)

start()