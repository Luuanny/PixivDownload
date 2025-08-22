from typing import Any

import requests

from res.config import read_headers

local_headers: dict | None = read_headers()


def get_body(url: str, headers: dict, get_info: str = "get body") -> Any | None:
    """ 获取响应体内容。
    :param url: 请求的 URL (str)
    :param headers: 请求头 (str)
    :param get_info: 请求信息 (str)
    :return: 返回响应体的 JSON 内容，如果失败则返回 None
    """
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # 检查请求是否成功
    res = response.json()  # 解析JSON数据
    body = res.get("body", {})
    if not body:
        print(f"{get_info} is none!!!")
        return None
    return body


def get_illust_ids1(uid: str, lang: str = "zh") -> list:
    """ 获取指定用户所有插画 ID 列表。
    :param uid: 用户 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: ids 列表 (list)
    """
    url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?sensitiveFilterMode=userSetting&lang={lang}"
    local_headers["Referer"] = f"https://www.pixiv.net/users/{uid}/artworks"
    body = get_body(url, local_headers, "get illust ids")
    illust_ids = list(body.get("illusts").keys())
    return illust_ids


def get_illust_ids2() -> list:
    origin_ids: list = []
    while True:
        illust_id: str = input("请输入图片 id (留空退出):").strip().lower()
        match illust_id:
            case "":
                ids: list[str] = list(dict.fromkeys(origin_ids))
                return ids
            case _:
                origin_ids.append(illust_id)


def get_illust_url(illust_id: str, lang: str = "zh") -> tuple[list[str], int, str]:
    """ 获取插画原图链接。
    :param illust_id: 插画 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: url 列表， url 数量
    """
    originals = []
    url = f"https://www.pixiv.net/ajax/illust/{illust_id}?lang={lang}"
    local_headers["Referer"] = f"https://www.pixiv.net/artworks/{illust_id}"
    body = get_body(url, local_headers, "get illust info")
    user_name = body.get("userName")
    page_count = body.get("pageCount")
    if page_count == 1:
        try:
            originals.append(body.get("urls", {}).get("original"))
        except Exception as e:
            print(f"get original url error: {e}")
    else:
        url = f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang={lang}"
        body = get_body(url, local_headers, "get multi-page illust info")
        if not body:
            return [], 0, user_name
        try:
            for page in body:
                originals.append(page.get("urls", {}).get("original"))
        except Exception as e:
            print("get original error: ", e)
    return originals, len(originals), user_name
