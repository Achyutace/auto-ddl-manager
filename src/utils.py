import os
import json
import re
import yaml

from datetime import datetime



'''
加载配置文件
'''
main_dir = (os.path.dirname(os.path.dirname(__file__)))
with open(f"{main_dir}/config.yaml", 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_key = config['api_key']
api_base = config['api_base']
api_model = config['api_model']

formal_prompt = '只用返回一个列表，不需要描述性文字。每一项是一个字典，分别是课程，任务和截止日期（某年某月某日几点，如果没有提到几点默认23点）。'

def extract_dict_lists(s):
    """
    从给定的字符串中解析所有形如 [{},...{}] 的字典列表。

    参数:
        s (str): 输入的字符串。

    返回:
        list: 包含第一个提取出的字典列表中的所有字典的列表。
    """
    try:
        s = s.replace('\n', '').replace('\r', '').replace(' ', '')
        pattern_one = r'\[\{[^\]]*\}\]'
        s_new = re.search(pattern_one, s).group()
        pattern_two = r'\{[^\}]*\}'
        matches = re.findall(pattern_two, s_new)
    except AttributeError as e:
        print(f"无法解析的字符串: {s}\n错误信息: {e}")
        return
    
    dict_lists = []
    for match in matches:
        # 如果匹配结果为空字符串，表示是 []
        if match == '':
            dict_lists.append([])
            continue

        # 处理可能的多余空格
        cleaned_match = match.replace('\'','\"' )
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

