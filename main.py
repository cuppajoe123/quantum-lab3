#!/usr/bin/env python3
"""
Quantum Computing Exercise Runner
Usage: python3 main.py <task_number>
Example: python3 main.py 1
"""

import sys
import os
import importlib.util


def load_task(task_number):
    """Dynamically load and execute a task module"""
    task_file = f"tasks/task{task_number}.py"

    if not os.path.exists(task_file):
        print(f"Error: Task {task_number} not found. File {task_file} does not exist.")
        print("Available tasks:")
        list_available_tasks()
        return False

    try:
        # Load the task module dynamically
        spec = importlib.util.spec_from_file_location(f"task{task_number}", task_file)
        task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_module)

        # Execute the task
        if hasattr(task_module, "run_task"):
            task_module.run_task()
        else:
            print(f"Error: Task {task_number} does not have a run_task() function.")
            return False

        return True

    except Exception as e:
        print(f"Error executing task {task_number}: {e}")
        return False


def list_available_tasks():
    """List all available tasks in the tasks directory"""
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        print("No tasks directory found.")
        return

    task_files = [
        f for f in os.listdir(tasks_dir) if f.startswith("task") and f.endswith(".py")
    ]
    task_numbers = []

    for task_file in task_files:
        try:
            # Extract task number from filename
            task_num = task_file.replace("task", "").replace(".py", "")
            if task_num.isdigit():
                task_numbers.append(int(task_num))
        except:
            continue

    task_numbers.sort()

    if task_numbers:
        for num in task_numbers:
            print(f"  Task {num}: python3 main.py {num}")
    else:
        print("  No valid tasks found.")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <task_number>")
        print("\nExample:")
        print("  python3 main.py 1")
        print("  python3 main.py 2")
        print("\nAvailable tasks:")
        list_available_tasks()
        sys.exit(1)

    try:
        task_number = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid task number.")
        print("Task number must be an integer.")
        sys.exit(1)

    print(f"=" * 50)
    print(f"Quantum Computing Exercise Runner")
    print(f"=" * 50)

    success = load_task(task_number)

    if not success:
        sys.exit(1)

    print(f"=" * 50)
    print(f"Task {task_number} completed!")
    print(f"=" * 50)


if __name__ == "__main__":
    main()
