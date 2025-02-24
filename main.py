import os
import json
import tkinter as tk
from src import *

# 初始化待办事项，从json文件中读取
main_dir = os.path.dirname(__file__)
try:
    with open(f"{main_dir}/data/data.json", encoding='utf=8') as f:
        ini_tasks = json.load(f)
except:
    ini_tasks = []
ini_task_manager = TaskManager(ini_tasks)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root, task_manager=ini_task_manager)
    root.mainloop()
    with open(f"{main_dir}/data/data.json", "w", encoding='utf-8') as f:
        json.dump(app.task_manager.view_tasks(), f)