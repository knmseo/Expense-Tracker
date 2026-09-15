import json

import Utilities


def add(data, instruction):
    try:
        amount, category, description = instruction.split(" ", 2)

        try:
            new_val = {
                "amount": int(amount),
                "category": category,
                "description": description,
            }
            data.append(new_val)
            Utilities.printlist(data)

        except ValueError:
            print("Invalid Integer!")

    except ValueError:
        print("Insufficient Arguments!")


def remove(data, instruction):
    try:
        data[int(instruction) - 1] = Utilities.DummyValue.copy()
        print(f"Removed number {instruction} from the list")

    except ValueError:
        print("Invalid Integer!")


def list_expenses(data, instruction):
    Utilities.printlist(data)

    with open("Saved/expenses.json", "w") as file:
        json.dump(data, file)


def edit(data, instruction):
    try:
        target_num, amount, category, description = instruction.split(" ", 3)

        try:
            target_num = int(target_num) - 1

            print(
                f"Edited "
                f"{data[target_num]['amount']} >> {amount}, "
                f"{data[target_num]['category']} >> {category}, "
                f"{data[target_num]['description']} >> {description}"
            )

            data[target_num] = {
                "amount": amount,
                "category": category,
                "description": description,
            }

            with open("Saved/expenses.json", "w") as file:
                json.dump(data, file)

        except ValueError:
            print("Invalid integer!")

    except ValueError:
        print("Insufficient Arguments!")


def total(data, instruction):
    Utilities.CalcTotal(data, instruction)


ACTIONS = {
    "add": add,
    "remove": remove,
    "list": list_expenses,
    "edit": edit,
    "total": total,
}


def main():
    prev_action_type = "None"
    data = Utilities.LoadFile("Saved/expenses.json")
    program_running = True

    while program_running:
        raw_user_instruction = input("Enter the next action: ")
        action_type, instruction = Utilities.SplitRawInput(raw_user_instruction)

        if action_type not in ACTIONS:
            print("This is not a valid action!")
            continue

        prev_action_type, data = Utilities.CustomWriteJSON(
            prev_action_type,
            action_type,
            data,
            Path="Saved/expenses.json",
        )

        ACTIONS[action_type](data, instruction)

        if action_type == "remove":
            prev_action_type = "remove"

        confirm = input("Do you have more to log?(y/n)")
        program_running = confirm == "y"


if __name__ == "__main__":
    main()
