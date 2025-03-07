import re
import json
from ast import literal_eval

def extract_dict_lists(s):
    """
    从给定的字符串中提取所有形如 [{},{}] 的字典列表。

    参数:
        s (str): 输入的字符串。

    返回:
        list: 包含所有提取出的字典列表的列表。
    """
    s = s.replace('\n', '').replace('\r', '').replace(' ', '')
    
    print("s:",s)
    pattern_one = r'\[\{[^\]]*\}\]'
    s_new = re.search(pattern_one, s).group()
    print("s_new",s_new)
    pattern_two = r'\{[^\}]*\}'
    matches = re.findall(pattern_two, s_new)
    print("matches:",matches)
    dict_lists = []
    for match in matches:
        # 如果匹配结果为空字符串，表示是 []
        if match == '':
            dict_lists.append([])
            continue
        # 替换单个空格（如果有），然后使用 json.loads 解析为字典列表
        try:
            # 处理可能的多余空格
            cleaned_match = match.replace(' ', '')
            dict_list = json.loads(f'[{cleaned_match}]')
            dict_lists.append(dict_list)
        except json.JSONDecodeError as e:
            print(f"无法解析的字典列表: {match}\n错误信息: {e}")

    return dict_lists

def main():
    # 示例文本
    sample_text = """
    [
    {"课程": "买衣服", "截止日期": "2025年2月28日 23时"},
    {"课程": "买裤子", "截止日期": "2025年2月28日 23时"}
]
    """
    simple_text = "[a]"
    # 提取字典列表
    dict_lists = extract_dict_lists(sample_text)

    # 输出结果
    for i, lst in enumerate(dict_lists, start=1):
        print(f"列表{i}: {lst}")

if __name__ == "__main__":
    main()