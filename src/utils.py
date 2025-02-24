import os
import json
import re
import yaml
import ast

from openai import OpenAI
from datetime import datetime
from json import JSONDecoder


'''
加载配置文件
'''
main_dir = (os.path.dirname(os.path.dirname(__file__)))
with open(f"{main_dir}/config.yaml", 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_key = config['api_key']
api_base = config['api_base']
api_model = config['api_model']

formal_prompt = '返回一个列表，每一项是一个字典，分别是课程，作业和截止日期（某年某月某日几点，如果没有提到几点默认23点）。'

def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

def extract_dict_lists(s):
    """
    从给定的字符串中解析所有形如 [{},...{}] 的字典列表。

    参数:
        s (str): 输入的字符串。

    返回:
        list: 包含第一个提取出的字典列表中的所有字典的列表。
    """
    pattern_one = r'\[\{[^\]]*\}\]'
    s_new = re.search(pattern_one, s).group()
    pattern_two = r'\{[^\}]*\}'
    matches = re.findall(pattern_two, s_new)
    
    dict_lists = []
    for match in matches:
        # 如果匹配结果为空字符串，表示是 []
        if match == '':
            dict_lists.append([])
            continue

        # 处理可能的多余空格
        cleaned_match = match.replace(' ', '')
        cleaned_match = cleaned_match.replace('\'','\"' )
        print(cleaned_match)
        # 替换单个空格（如果有），然后使用 json.loads 解析为字典列表
        try:
            dict_list = json.loads(f'{cleaned_match}')
            dict_lists.append(dict_list)
        except json.JSONDecodeError as e:
            print(f"无法解析的字典列表: {match}\n错误信息: {e}")

    return dict_lists

def print_dic_info(dic, dic_name, tag=''):
    for k in dic:
        print(tag, end='')
        if type(dic[k])==type({}):
            print(f'{dic_name}[{k}]:{type(dic[k])}'+'{')
            print_dic_info(dic[k], f'{dic_name}[{k}]', tag=tag+'\t')
            print('}', end='')
        elif 'numpy' in str(type(dic[k])):
            print(f'{dic_name}[{k}]:{type(dic[k])}  (shape={dic[k].shape})', end='')
        elif type(dic[k])== type([]):
            lis = dic[k]
            s = f'({len(lis)}, {len(lis[0])})' if len(lis)>0 and type(lis[0])==type([]) else f'{len(lis)}'
            print(f'{dic_name}[{k}]:{type(dic[k])}  (len={s})', end='')
        else:
            print(f'{dic_name}[{k}]:{type(dic[k])}', end='')
        print()

def today_info():
    '''
    返回当天日期信息的字符串。
    '''
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    day_of_week = today.strftime("%A")

    weekdays = {
        'Monday': '一',
        'Tuesday': '二',
        'Wednesday': '三',
        'Thursday': '四',
        'Friday': '五',
        'Saturday': '六',
        'Sunday': '日'
    }
    day_of_week_cn = weekdays.get(day_of_week, '未知')
    today_str = f'今天是{year}年{month}月{day}日，星期{day_of_week_cn}。'
    return today_str

def handle_input(words):
    '''
    parse words: 自然语言输入
    '''
    client = OpenAI(api_key = api_key, base_url = api_base)
    response = client.chat.completions.create(
        model = api_model,
        messages = [
            {"role":"system","content":"你是一个ai-deadline-manager助手，请按照给定输入格式返回列表。"},
            {"role":"user","content":today_info()+words+formal_prompt}
        ],
        stream=False
    )
    print(response.choices[0].message.content)
    return extract_dict_lists(response.choices[0].message.content)

if __name__ == "__main__":
    # 测试用例
    words = '代组作业：“《离散数学教程》习题十五，p. 238: 9”，本次作业ddl暂定3月5日。算分作业：算分作业1，已发邮箱，ddl这周五。'
    # handle_input(words)

    sample_text = """
    这里有一些数据：
    - 列表1: [{ "name": "Alice", "age": 30 }, { "name": "Bob", "age": 25 }]
    - 列表2: [{ "product": "苹果", "price": 3.5 }, { "product": "香蕉", "price": 2.0 }]
    - 列表3: []
    - 列表4: [{ "id": 1 }, { "id": 2, "active": true }]
    """

    extracted = extract_dict_lists(sample_text)
    print(extracted)
    for idx, dl in enumerate(extracted, 1):
        print(f"字典列表 {idx}: {dl}")
        print_dic_info(dl, f'dl{idx}', tag='\t')