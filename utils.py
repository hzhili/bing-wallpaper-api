import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def append_json(region_type, data):
    """
    追加Python字典到JSON文件（顶层为列表，自动初始化空文件）
    :param region_type: 地区编码
    :param data: 待追加的字典数据
    """
    try:
        # 1. 读取已存在的文件，解析为Python列表
        with open(f'data/{region_type}.json', "r", encoding="utf-8") as f:
            data_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 异常处理：文件不存在 / 文件为空/格式非法 → 初始化空列表
        data_list = []

    # 2. 将新字典追加到列表中
    data_list.extend(data)

    # 3. 重新将列表写入文件（覆盖写入，保证格式合法）
    with open(f'data/{region_type}.json', "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False)

def get_all_data(region_type):
    """
    从JSON文件中读取所有数据（顶层为列表）
    :param region_type: 地区编码
    :return: 包含所有数据的Python列表
    """
    try:
        # 1. 读取已存在的文件，解析为Python列表
        with open(f'data/{region_type}.json', "r", encoding="utf-8") as f:
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
    with open(f'data/{region_type}-today.json', "w", encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False)
