import os, json
import datetime

def create_file():

    tasks = []
    print("\n----- CREATE A NEW FILE -----")
    json_file_name_input = input("Create a file name: ")
    json_file_name = f"{json_file_name_input}.json"

    try:
        with open(json_file_name, "w") as file:
            json.dump(tasks, file, indent=4)
            print(f"\nJSON File named {json_file_name} was created")

    except FileExistsError:
        print(f"\nJSON File named {json_file_name} already exists.")

    print("Thank you for using Task Tracker.")
    print("The program requires to be restarted.")
    print("Reopen the program to access your file.")
    exit("\n----- FILE CREATED -----")

def open_file():

    print("\n----- OPEN EXISTING FILE -----")
    json_file_name_input = input("Name of existing file: ")
    json_file_name = f"{json_file_name_input}.json"
    tasks = []

    try:
        with open(json_file_name, "r") as file:
            rows = json.load(file)
            for row in rows:
                tasks.append(row)
        print(f"\nJSON File named {json_file_name} was created.")
        return tasks, json_file_name

    except FileNotFoundError:
        print(f"\nJSON File named {json_file_name} was not found.")
        return None, None

    except PermissionError:
        print(f"\nNo Access to file {json_file_name}.")
        return None, None

def delete_file():

    print("\n----- DELETE FILE -----")
    json_file_name_input = input("Name of file to delete: ")
    json_file_name = f"{json_file_name_input}.json"

    if os.path.exists(json_file_name):
        os.remove(json_file_name)
        print(f"\nJSON File named {json_file_name} was deleted.")
    else:
        print(f"\nJSON File named {json_file_name} does not exist.")

def read_file(json_file_name):

    tasks = []

    if os.path.exists(json_file_name):
        with open(json_file_name, "r") as file:
            rows = json.load(file)
            for row in rows:
                tasks.append(row)

    return tasks

def add_tasks(json_file_name):
    print("\n----- ADD TASK -----")
    task_name = input("Task Name: ")
    task_status = input("Task Status: ")

    tasks = read_file(json_file_name)

    date = datetime.datetime.today().strftime("%m/%d/%y")

    if tasks and str(tasks[-1]["ID"]).isdigit():
        id = int(tasks[-1]["ID"])

    else:
        id = 0

    current = id + 1

    with open(json_file_name, "r") as file:
        tasks = json.load(file)

    new_task = {"ID": current, "Date": date, "Name": task_name, "Status": task_status}
    tasks.append(new_task)

    with open(json_file_name, "w") as file:
        json.dump(tasks, file, indent=4)

    print("\nTask Added Successfully.")

def update_tasks(json_file_name):
    tasks = read_file(json_file_name)

    if not tasks:
        print("\nNo tasks to update.")

    view_tasks(json_file_name)

    print("\n----- UPDATE TASKS -----")

    try:
        id = int(input("Input ID to Update: "))

    except ValueError:
        print("\nInvalid ID. Please try again.")
        return

    found_id = False

    for task in tasks:
        if task["ID"] == id:
            found_id = True

            print("\n----- UPDATE TASKS -----")
            print("1. Update Name")
            print("2. Update Status")
            print("3. Update Both")
            print("4. Back to Action Menu")

            choice = input("Input an action (1-4): ")
            if choice == "1":
                old_name = task["Name"]
                print(f"\nCurrent Name: {old_name}")
                new_name = input("New Name: ")
                task["Name"] = new_name
                task["Date"] = datetime.datetime.today().strftime("%m/%d/%y")

                view_tasks(json_file_name)
                print("\nName Updated.")

            elif choice == "2":
                old_status = task["Status"]
                print(f"\nCurrent Status: {old_status}")
                new_status = input("New Status: ")
                task["Status"] = new_status
                task["Date"] = datetime.datetime.today().strftime("%m/%d/%y")

                view_tasks(json_file_name)
                print("\nStatus Updated.")

            elif choice == "3":
                old_name = task["Name"]
                print(f"\nCurrent Name: {old_name}")
                new_name = input("New Name: ")
                task["Name"] = new_name

                old_status = task["Status"]
                print(f"\nCurrent Status: {old_status}")
                new_status = input("New Status: ")
                task["Status"] = new_status
                task["Date"] = datetime.datetime.today().strftime("%m/%d/%y")

                view_tasks(json_file_name)
                print("\nName and Status Updated.")


            elif choice == "4":
                get_action(json_file_name)

            else:
                print("\nInvalid Action. Please try again.")
                return

            break

    if not found_id:
        print("\nNo ID was found. Please try again.")
        return

    with open(json_file_name, "w") as file:
        json.dump(tasks, file, indent=4)

    print("\nTask Updated Successfully.")

def delete_tasks(json_file_name):
    tasks = read_file(json_file_name)

    view_tasks(json_file_name)

    with open(json_file_name, "r") as file:
        tasks = json.load(file)

    print("\n----- DELETE TASKS -----")

    try:
        id = int(input("Input ID to Delete: "))

    except ValueError:
        print("\nInvalid ID. Try again.")
        return

    updated_tasks = [task for task in tasks if int(task["ID"]) != id]

    updated_id = 1

    for task in updated_tasks:
        task["ID"] = updated_id
        updated_id += 1

    with open(json_file_name, "w") as file:
        json.dump(updated_tasks, file, indent=4)

    print("\nTask Deleted Successfully.")

def view_tasks(json_file_name):
    tasks = read_file(json_file_name)

    if not tasks:
        print("\nNo tasks to show.")
        return

    print("\n---------- TASK TRACKER ----------")

    for task in tasks:
        print(f"ID: {task['ID']} | Date: {task['Date']} | Name: {task['Name']} | Status: {task['Status']}")

def view_tasks_status(json_file_name):
    tasks = read_file(json_file_name)

    if not tasks:
        print("\nNo tasks to show.")

    print("\n----- VIEW TASKS BY STATUS -----")

    try:
        status = input("Input Progress (No Progress, In Progress, Done): ").title()

    except ValueError:
        print("\nInvalid Indicator. Please try again.")
        return

    indicator = [task for task in tasks if task["Status"] == status]

    if not indicator:
        print("\nNo tasks to show.")

    updated_id = 1

    for task in indicator:
        task["ID"] = updated_id
        updated_id += 1
        print(f"ID: {task['ID']} | Date: {task['Date']} | Name: {task['Name']} | Status: {task['Status']}")

def get_action(json_file_name):
    while True:
        print("\n----- TASK TRACKER ACTIONS -----")
        print("1. Add Tasks")
        print("2. Update Tasks")
        print("3. Delete Tasks")
        print("4. View Tasks")
        print("5. Back to Main Menu")
        print("6. Exit")

        choice = input("Input an action (1-6): ")
        if choice == "1":
            add_tasks(json_file_name)

        elif choice == "2":
            update_tasks(json_file_name)

        elif choice == "3":
            delete_tasks(json_file_name)

        elif choice == "4":
            print("\n----- VIEW TASKS -----")
            print("1. View All Tasks")
            print("2. View By Status")

            choice_task = input("Input an action (1-2): ")
            if choice_task == "1":
                view_tasks(json_file_name)

            elif choice_task == "2":
                view_tasks_status(json_file_name)

        elif choice == "5":
            main()

        elif choice == "6":
            exit("\n----- THANK YOU FOR USING TASK TRACKER -----")

        else:
            print("\nInvalid Action. Please try again.")

def main():

    print("----- WELCOME TO TASK TRACKER -----")
    print("Progress: No Progress, In Progress, Done")
    print("This program only uses those three indicators.")
    print("If you want to change the indicators, feel free")
    print("to change it in the code!")

    while True:
        print("\n----- TASK TRACKER MENU -----")
        print("1. Create a New Task Tracker")
        print("2. Open Existing Task Tracker")
        print("3. Delete Existing Task Tracker")
        print("4. Exit")

        choice = input("Input an action (1-4): ")
        if choice == "1":
            create_file()

        elif choice == "2":
            tasks, json_file_name = open_file()
            if json_file_name:
                get_action(json_file_name)

        elif choice == "3":
            delete_file()

        elif choice == "4":
            exit("\n----- THANK YOU FOR USING TASK TRACKER -----")

        else:
            print("\nInvalid Action. Please try again.")

if __name__ == "__main__":
    main()