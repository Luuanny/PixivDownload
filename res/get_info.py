import requests
from headers import read_headers
from res.url_param_splice import splicing


headers = read_headers()


def get_body(url: str, headers: str, get_info: str = "get body") -> any:
    """ 获取响应体内容。
    :param url: 请求的 URL (str)
    :param headers: 请求头 (str)
    :param get_info: 请求信息 (str)
    :return: 返回响应体的 JSON 内容，如果失败则返回 None
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        res = response.json()  # 解析JSON数据
    except Exception:
        return None
    body = res.get("body", {})
    if not body:
        print(f"{get_info} is none!!!")
        return None
    return body


def get_user_name(uid: str, lang: str = "zh") -> str:
    """ 获取Pixiv用户信息。
    :param uid: 用户 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: 返回用户名，如果获取失败则返回 "unknown"
    """
    url = f"https://www.pixiv.net/ajax/user/{uid}?full=1&lang={lang}"
    headers["Referer"] = f"https://www.pixiv.net/users/{uid}/artworks"
    body = get_body(url, headers, "get user info")
    user_name = body.get("name")
    return user_name


def get_illust_ids(uid: str, lang: str = "zh") -> list:
    """ 获取指定用户所有插画 ID 列表。
    :param uid: 用户 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: ids 列表
    """
    url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?sensitiveFilterMode=userSetting&lang={lang}"
    headers["Referer"] = f"https://www.pixiv.net/users/{uid}/artworks"
    body = get_body(url, headers, "get illust ids")
    illust_ids = list(body.get("illusts").keys())
    return illust_ids


def get_illust_info(uid: str, lang: str = "zh") -> dict:
    """ 获取插画信息。
    :param uid: 用户 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: 返回目标用户所有的插画信息字典
    """
    url = f"https://www.pixiv.net/ajax/user/{uid}/profile/illusts?{splicing(get_illust_ids(uid, lang))}"
    headers["Referer"] = f"https://www.pixiv.net/users/{uid}/artworks"
    body = get_body(url, headers, "get illust info")
    works = body.get("works")
    return dict(works)


def get_illust_sum(uid: str, lang: str = "zh") -> int:
    """ 获取插画总数
    :param uid: 用户 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: 插画总数
    """
    illust_sum = 0
    works = get_illust_info(uid, lang)
    illust_ids = get_illust_ids(uid, lang)
    for id in illust_ids:
        illust_sum += works[id]["pageCount"]
    return int(illust_sum)


def get_illust_url(illust_id: str, lang: str = "zh") -> list:
    """ 获取插画原图链接。
    :param uid: 插画 ID (str)
    :param lang: 语言选项，默认为中文 (str)
    :return: url 列表， url 数量
    """
    url = f"https://www.pixiv.net/ajax/illust/{illust_id}?lang={lang}"
    headers["Referer"] = f"https://www.pixiv.net/artworks/{illust_id}"
    body = get_body(url, headers, "get illust info")
    page_count = body.get("pageCount")
    originals = []
    if page_count == 1:
        try:
            originals.append(body.get("urls", {}).get("original"))
        except Exception as e:
            print(f"get original url error: {e}")
    else:
        url = f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang={lang}"
        body = get_body(url, headers, "get multi-page illust info")
        if not body:
            return []
        try:
            for page in body:
                originals.append(page.get("urls", {}).get("original"))
        except Exception as e:
            print("get original error: ", e)
    return originals, len(originals)

