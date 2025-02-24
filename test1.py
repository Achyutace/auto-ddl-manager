import re

s = """
    这里有一些数据：
    - 列表1: [{ "name": "Alice", "age": 30 }, { "name": "Bob", "age": 25 }]
    - 列表2: [{ "product": "苹果", "price": 3.5 }, { "product": "香蕉", "price": 2.0 }]
    - 列表3: []
    - 列表4: [{ "id": 1 }, { "id": 2, "active": true }]
    """

pattern_one = r'\[\{[^\]]*\}\]'
s_new = re.search(pattern_one, s).group()

pattern_two = r'\{\{[^\}]*\}\}'
matches = re.findall(pattern_two, s_new)
print(s_new)
print(matches)