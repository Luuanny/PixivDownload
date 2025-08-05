import os
import json
from res.ask_info import ask_input


def main() -> None:
    headers = check_and_generate_json()
    if ask_input("是否重新输入？"):
        os.system('cls' if os.name == 'nt' else 'clear')
        headers = get_headers_interactive()
        write_headers(headers)
        print(f"当前 Headers:\n{json.dumps(headers, ensure_ascii=False, indent=2)}")


def get_headers_interactive() -> dict:
    """ 交互式获取请求头信息。
    :return: 包含 User-agent, Referer 和 Cookie 的字典
    """
    return {
        "User-agent": input_user_agent(),
        "Referer": input_referer(),
        "Cookie": input_cookie()
    }


def input_user_agent() -> str:
    """ 获取 User_agent 字符串。
    :return: User_agent 字符串
    """
    user_agent = input("请输入 User_agent (留空使用默认值): ").strip()
    if not user_agent:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    os.system('cls' if os.name == 'nt' else 'clear')
    return user_agent


def input_referer() -> str:
    """ 获取 Referer 字符串。
    :return: Referer 字符串
    """
    referer = input("请输入 Referer (留空使用默认值): ").strip()
    if not referer:
        referer = "https://www.pixiv.net/"
    os.system('cls' if os.name == 'nt' else 'clear')
    return referer


def input_cookie() -> str:
    """ 获取 Cookie 字符串。
    :return: Cookie 字符串
    """
    cookie = input("请输入 Cookie (可留空，留空可能导致图片下载不完全): ").strip()
    if not cookie:
        cookie = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    return cookie


def check_and_generate_json() -> dict:
    """ 检查 headers.json 是否存在，不存在则交互生成并输出内容。
    :return: Headers 字典 (dict)
    """
    if not os.path.exists("headers.json"):
        print("headers.json 文件不存在，将为你生成新的 headers.json ...")
        headers = get_headers_interactive()
        write_headers(headers)
        print(f"生成的 headers.json 内容如下：\n{json.dumps(headers, ensure_ascii=False, indent=2)}")
        return headers
    else:
        headers = read_headers()
        print(f"当前 headers:\n{json.dumps(headers, ensure_ascii=False, indent=2)}")
        return headers


def write_headers(headers: dict) -> None:
    """ 将 Headers 写入到 headers.json 文件中。
    :param headers: Headers 字典 (dict)
    """
    try:
        with open("headers.json", "w", encoding="utf-8") as f:
            json.dump(headers, f, ensure_ascii=False, indent=2)
        print("Headers 已写入到 headers.json")
    except Exception as e:
        print(f"写入headers.json失败: {e}")


def read_headers() -> dict | None:
    """ 从 headers.json 文件中读取 Headers。
    :return: Headers 字典 (dict)
    """
    if not os.path.exists("headers.json"):
        new_headers = get_headers_interactive()
        write_headers(new_headers)
    try:
        with open("headers.json", "r", encoding="utf-8") as f:
            headers = json.load(f)
        return headers
    except Exception as e:
        print(f"读取headers.json失败: {e}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()