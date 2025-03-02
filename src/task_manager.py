from datetime import datetime
from .utils import check_task_format

class TaskManager:
    def __init__(self, ini_tasks=None):
        self.tasks = ini_tasks  # 存储任务的列表

    def add_tasks(self, tasks):
        """
        添加多个任务到任务列表。
        """
        if tasks is not None:
            print("正在添加任务...")
            for i, task in enumerate(tasks):
                if not check_task_format(task):
                    print(f"任务 {i} 格式错误，跳过。")
                    continue
                print(i, '.:', task["任务"])
                self.tasks.append(task)

    def view_tasks(self):
        """
        查看所有任务。
        """
        return self.tasks

    def delete_task(self, index):
        """
        删除指定索引的任务。
        """
        if 0 <= index < len(self.tasks):
            deleted_task = self.tasks.pop(index)
            return deleted_task
        return None

    def check_reminders(self):
        """
        检查是否有任务需要提醒。
        """
        today = datetime.now().strftime("%Y-%m-%d")
        reminders = []
        for task in self.tasks:
            if task["time"] == today:
                reminders.append(task)
        return reminders