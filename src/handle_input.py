from .utils import *
from json import JSONDecoder
from openai import OpenAI

def handle_input(words):
    '''
    parse words: 自然语言输入
    '''
    client = OpenAI(api_key = api_key, base_url = api_base)
    response = client.chat.completions.create(
        model = api_model,
        messages = [
            {"role":"system","content":"你是一个ai-deadline-manager助手，请按照给定输入格式返回列表。default填未知。"},
            {"role":"user","content":today_info()+words+formal_prompt}
        ],
        stream=False
    )
    reply = response.choices[0].message.content
    print("reply:\n",reply)
    tem = extract_dict_lists(reply)
    # print(tem)
    return tem

if __name__ == "__main__":
    # 测试用例
    words = '代组任务：“《离散数学教程》习题十五，p. 238: 9”，本次任务ddl暂定3月5日。算分任务：算分任务1，已发邮箱，ddl这周五。'
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