import tkinter as tk
from tkinter import messagebox
from .task_manager import TaskManager
from .handle_input import handle_input

class TodoApp:
    '''
    UI of the tool.
    '''
    def __init__(self, root, task_manager = TaskManager()):
        self.root = root
        self.root.title("待办事项管理工具")
        self.task_manager = task_manager

        # 创建UI组件
        self.create_widgets()

    def create_widgets(self):
        """
        创建UI组件。
        """
        # 输入框和按钮
        self.input_label = tk.Label(self.root, text="输入任务，可输入自然语言：")
        self.input_label.pack()

        self.input_text = tk.Text(self.root, height=5, width=40)
        self.input_text.pack()

        self.add_button = tk.Button(self.root, text="添加任务", command=self.add_task)
        self.add_button.pack()

        # 任务列表显示
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.view_button = tk.Button(self.root, text="查看任务", command=self.view_tasks)
        self.view_button.pack()

        self.delete_button = tk.Button(self.root, text="删除任务", command=self.delete_task)
        self.delete_button.pack()

        # 提醒按钮
        self.reminder_button = tk.Button(self.root, text="检查提醒", command=self.check_reminders)
        self.reminder_button.pack()

        self.view_tasks()

    def add_task(self):
        """
        添加任务到任务列表。
        """
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入任务内容！")
            return

        # 这里返回的是一个列表
        tasks = handle_input(input_text)
        self.task_manager.add_tasks(tasks)
        
        messagebox.showinfo("成功", "任务添加成功！")
        self.input_text.delete("1.0", tk.END)  # 清空输入框
        self.view_tasks()  # 刷新任务列表

    def view_tasks(self):
        """
        查看所有任务。
        """
        self.task_listbox.delete(0, tk.END)  # 清空列表框
        tasks = self.task_manager.view_tasks()
        for i, task in enumerate(tasks):
            print(task)
            self.task_listbox.insert(tk.END, f"{i + 1}. {task['任务']} - {task['截止日期']}")

    def delete_task(self):
        """
        删除选中的任务。
        """
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("警告", "请选择要删除的任务！")
            return

        index = selected_index[0]
        deleted_task = self.task_manager.delete_task(index)
        if deleted_task:
            messagebox.showinfo("成功", f"任务已删除：{deleted_task['任务']}")
            self.view_tasks()  # 刷新任务列表

    def check_reminders(self):
        """
        检查提醒。
        """
        reminders = self.task_manager.check_reminders()
        if not reminders:
            messagebox.showinfo("提醒", "今天没有需要完成的任务。")
        else:
            reminder_text = "\n".join([f"{task['time']} - {task['content']}" for task in reminders])
            messagebox.showinfo("提醒", f"今天需要完成的任务：\n{reminder_text}")