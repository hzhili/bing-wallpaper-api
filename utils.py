import os
import sys
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR,"data")

def del_duplicate(old:list,new:list):
    """
    从JSON文件中删除重复数据（顶层为列表）
    :param region_type: 地区编码
    """
    merged_list = old + new
    unique_dict = {}
    for d in merged_list:
        unique_dict[d["url"]] = d  # 直接覆盖，保留最后一个
    result = list(unique_dict.values())
    return result
    

def get_location_file(location: str, today: bool = False) -> str:
    """获取指定地区的JSON文件路径"""
    if today:
        return f"{DATA_DIR}/{location}-today.json"
    else:
        return f"{DATA_DIR}/{location}.json"

def get_today_wallpaper(location: str) -> dict:
    """获取指定地区的今日壁纸"""
    file_path = get_location_file(location, today=True)
    
    if not os.path.exists(file_path):
        wallpapers = get_wallpapers(location)
        if wallpapers:
            return wallpapers[0]
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return None

def get_all_locations() -> list:
    """获取所有可用的地区编码"""
    locations = []
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".json") and not filename.endswith("-today.json"):
                location = os.path.splitext(filename)[0]
                locations.append(location)
    return locations

def get_wallpapers(location: str) -> list:
    """获取指定地区的所有壁纸"""
    file_path = get_location_file(location, today=False)
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                if isinstance(first_item, list):
                    return first_item
                return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return []

def append_json(region_type, data):
    """
    追加Python字典到JSON文件（顶层为列表，自动初始化空文件）
    :param region_type: 地区编码
    :param data: 待追加的字典数据
    """
    try:
        # 1. 读取已存在的文件，解析为Python列表
        with open(get_location_file(location=region_type), "r", encoding="utf-8") as f:
            data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 异常处理：文件不存在 / 文件为空/格式非法 → 初始化空列表
        data_list = []

    # 2. 将新字典追加到列表中
    data_list = del_duplicate(data_list,data)

    # 3. 重新将列表写入文件（覆盖写入，保证格式合法）
    with open(get_location_file(location=region_type), "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False)

def get_all_data(region_type):
    """
    从JSON文件中读取所有数据（顶层为列表）
    :param region_type: 地区编码
    :return: 包含所有数据的Python列表
    """
    try:
        # 1. 读取已存在的文件，解析为Python列表
        with open(get_location_file(location=region_type), "r", encoding="utf-8") as f:
            data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 异常处理：文件不存在 / 文件为空/格式非法 → 初始化空列表
        data_list = []
    return data_list

def writer_today(region_type, data):
    """
    将Python列表写入JSON文件（顶层为列表，自动初始化空文件）
    :param region_type: 地区编码
    :param data: 待写入的字典数据列表
    """
    with open(get_location_file(location=region_type,today=True), "w", encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False)
