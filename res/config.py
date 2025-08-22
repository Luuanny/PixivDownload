import json
import os


def show_config() -> None:
    """ 显示当前 config 配置 """
    check_config()
    config = read_config()
    print(f"当前 config.json 如下：\n{json.dumps(config, ensure_ascii=False, indent=2)}")
    return None


def reconfig() -> dict:
    """ 重新配置 config """
    config: dict = {
        "Headers": get_headers(),
        "SavePath": get_save_path()
    }
    write_config(config)
    return config


def get_headers() -> dict:
    """ 交互式获取请求头信息
    :return: 包含 User-agent, Referer 和 Cookie 的字典 (dict)
    """
    return {
        "User-agent": input_user_agent(),
        "Referer": input_referer(),
        "Cookie": input_cookie()
    }


def get_save_path() -> str:
    """ 获取保存路径
    :return: 保存路径 (str)
    """
    save_path: str = input("请输入保存路径 (留空使用默认值)：").strip()
    if not save_path:
        save_path = "Download"
    return save_path


def input_user_agent() -> str:
    """ 获取 User_agent
    :return: User_agent (str)
    """
    user_agent: str = input("请输入 User_agent (留空使用默认值): ").strip()
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    return user_agent


def input_referer() -> str:
    """ 获取 Referer
    :return: Referer (str)
    """
    referer: str = input("请输入 Referer (留空使用默认值): ").strip()
    if not referer:
        referer = "https://www.pixiv.net/"
    return referer


def input_cookie() -> str:
    """ 获取 Cookie
    :return: Cookie (str)
    """
    cookie: str = input("请输入 Cookie (可留空，留空可能导致图片下载不完全): ").strip()
    if not cookie:
        cookie = ""
    return cookie


def check_config() -> None:
    """ 检查 config.json 是否存在，不存在则交互生成 """
    if not os.path.exists("config.json"):
        print("config.json 文件不存在，将为你生成新的 config.json...")
        reconfig()
    return None


def read_config() -> dict:
    """ 读取 config.json 文件配置
    :return: config (dict)
    """
    check_config()
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        print(f"读取 config 失败：{e}")
        config = reconfig()
    return config


def read_headers() -> dict:
    """ 从 config.json 文件中读取 Headers。
    :return: headers 字典 (dict)
    """
    config = read_config()
    headers = config["Headers"]
    return headers


def read_save_path() -> str:
    """ 从 config.json 文件中读取 save_path。
    :return: 保存路径 (str)
    """
    config = read_config()
    save_path = config["SavePath"]
    return save_path


def write_config(config: dict) -> None:
    """ 将 Headers 写入到 config.json 文件中。
    :param config: Headers 字典 (dict)
    """
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("配置已写入到 config.json")
    except Exception as e:
        print(f"写入 config.json 失败: {e}")
    return None
