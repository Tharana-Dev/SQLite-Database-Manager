import sqlite3
from pathlib import Path
from operations import *

TASKS = [
    'Create Table',
    'Insert Data',
    'Update Data',
    'Delete Data',
    'Select And Filter Data',
    'Exit'
]

def get_single_task():
    """Display menu and return one task based on user input.
       Accepts partial matches (case‑insensitive)."""
    print("\nAvailable tasks:")
    for i, task in enumerate(TASKS, 1):
        print(f"  {i}. {task}")

    while True:
        choice = input("Enter task (or part of it): ").strip().lower()
        if not choice:
            continue

        # Look for a task that contains the input string
        matched_task = None
        for task in TASKS:
            if choice in task.lower():
                matched_task = task
                break

        if matched_task:
            print(f"✅ Selected: {matched_task}")
            return matched_task
        else:
            print("❌ No matching task found. Try again.")

def main():
    # --- Database path handling ---
    dir_input = input("Enter database directory (press Enter for current folder): ").strip()
    if dir_input:
        db_dir = Path(dir_input)
        if not db_dir.exists():
            print(f"❌ Directory '{db_dir}' does not exist. Exiting.")
            return
        if not db_dir.is_dir():
            print(f"❌ '{db_dir}' is not a directory. Exiting.")
            return
    else:
        db_dir = Path.cwd()

    db_name = input("Enter database name (without extension): ").strip()
    if not db_name:
        print("❌ Database name cannot be empty. Exiting.")
        return

    db_filename = db_name + '.db'
    db_path = db_dir / db_filename

    try:
        conn = sqlite3.connect(db_path)
        print(f"\n✅ Connected to database: {db_path.name}")
        print(f"📍 Location: {db_path.resolve().parent}")
        print(f"📁 Full path: {db_path.resolve()}\n")
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return

    # --- Interactive task loop ---
    while True:
        task = get_single_task()
        if task == 'Exit':
            print("Exiting program.")
            break

        print(f"\n--- Executing: {task} ---")
        if task == 'Create Table':
            create_table(conn)
        elif task == 'Insert Data':
            insert_data(conn)
        elif task == 'Update Data':
            update_data(conn)
        elif task == 'Delete Data':
            delete_data(conn)
        elif task == 'Select And Filter Data':
            select_data(conn)
        else:
            print(f"Unknown task: {task}")

        again = input("\nDo you want to perform another task? (y/n): ").strip().lower()
        if again != 'y':
            break

    conn.close()
    print("\n🔒 Connection closed. Goodbye!")

if __name__ == "__main__":
    main()
