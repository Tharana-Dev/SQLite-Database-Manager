import time

def get_tasks():
    # List of available cleaning tasks
    tasks = [
        'Create Table',
        'Insert Data',
        'Update Data',
        'Delete Data',
        'Select And Filter Data',
        'Exit'
    ]

    # Display the menu with a small delay for effect
    print("Tasks Provided:")
    for i, task in enumerate(tasks, 1):
        print(f"        {i}. {task}")
        time.sleep(0.25)

    print()
    
    # Ask how many tasks the user wants to perform
    while True:
        try:
            number = int(input("How many tasks would you like to perform through this system: "))
            if 1 <= number <= len(tasks):
                break  # valid input, exit loop
            else:
                print("Please select a number within the given range.\n")
        except ValueError:
            print("Input numbers only!\n")

    # Collect the chosen tasks
    chosen_tasks = []
    for _ in range(number):
        while True:
            choice = input("What task would you like to perform: ").title().strip()
            if choice in tasks:
                chosen_tasks.append(choice)
                break  # valid task, move to next one
            else:
                print("Please select from the available tasks.\n")

    return chosen_tasks

# Test block – runs only when this file is executed directly
if __name__ == "__main__":
    selected = get_tasks()
    print("\nYou selected the following tasks:")
    for task in selected:
        print(f"  - {task}")
