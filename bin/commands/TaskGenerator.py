from os import path, makedirs
import json
from from_root import from_root


class TaskGeneratorCommand:
    def __init__(self, input=None):
        self.input = input
        # generate tasks.json in case it doesn't exist
        if not path.exists(from_root("config/tasks.json")):
            try:
                with open(from_root("config/tasks.json"), "w") as f:
                    json.dump({"tasks": {}}, f, indent=2)
            except Exception as e:
                print(f"Error opening config/tasks.json. Error: {e}")

    def get_available_tasks(self) -> dict:
        data = {}
        try:
            f = open("config/tasks.json", "r")
            return json.load(f)
        except Exception as e:
            print("Unable to grab tasks from ")
            return data

    def reformat_text(self, word: str):
        if "-" in word:
            parts = word.split("-")
            capitalized_parts = [part.capitalize() for part in parts]
            return "".join(capitalized_parts)
        else:
            return word.capitalize()

    def make_task_class_template(self, task_name: str) -> str:
        """Generate a Python class template for a task."""
        class_name = self.reformat_text(task_name)
        template = f"""class {class_name}:\n\
    def __init__(self, bot, logger):\n\
        self.bot = bot\n\
        self.logger = logger\n\n\
    async def main(self):\n\
        self.logger.info("Task: {class_name} has started...")
"""
        return template

    def generate_task_entry(self, task_name: str) -> None:
        class_name = self.reformat_text(task_name)
        file_name = task_name.replace("-", "_").lower()

        try:
            task_structure: dict = {
                "file_name": f"{file_name}.py",
                "class_name": class_name,
                "hours": 1,
                "minutes": 0,
                "seconds": 0,
                "enabled": True,
            }

            available_tasks: dict = self.get_available_tasks()
            if available_tasks and class_name in available_tasks["tasks"]:
                print(f"Task name: {task_name} already exists within config/tasks.json")
                return

            available_tasks["tasks"][class_name] = task_structure

            with open(from_root("config/tasks.json"), "w") as f:
                json.dump(available_tasks, f, indent=2)

            print(f"Task entry added for: '{task_name}' in config/tasks.json")

            task_template = self.make_task_class_template(task_name)
            task_dir = from_root("tasks")

            if not path.exists(task_dir):
                makedirs(task_dir)

            task_file_path = path.join(task_dir, f"{file_name}.py")
            with open(task_file_path, "w") as task_file:
                task_file.write(task_template)

            print(
                f"Task template for: '{task_name}' has been created at {task_file_path}"
            )

        except Exception as e:
            print(f"Unable to generate task for {task_name}. Error: {e}")
