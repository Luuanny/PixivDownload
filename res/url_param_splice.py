def splicing(illust_ids: list) -> str:
    """ url 请求参数拼接
    :param illust_ids: 插画 id 数组 (list)
    :return: 拼接好的请求参数字符串
    """
    param = ""
    for id in illust_ids:
        param += f"ids[]={id}&"
    param += "work_category=illustManga&is_first_page=1&sensitiveFilterMode=userSetting&lang=zh"
    return param