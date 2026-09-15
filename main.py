import json

import Utilities

DummyValue = {
    "amount": 0,
    "category": "REMOVED",
    "description": "None",
}


def main():
    PrevActionType = "None"
    data = []
    try:
        with open("Saved/expenses.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("The JSON file is corrupted or doesn't exist?")
        data = []

    ProgramRunning = True

    while ProgramRunning:
        RawUserInstruction = input("Enter the next action: ")
        TempList = RawUserInstruction.split(" ", 1)
        if len(TempList) == 1:
            ActionType = TempList[0]
            Instruction = "None"
        elif len(TempList) == 2:
            ActionType, Instruction = TempList

        if not ActionType in {"add", "remove", "list", "edit", "total"}:
            print("This is not a valid action!")
            continue

        SaveCandidate = []
        if PrevActionType == "remove" and ActionType != "remove":
            PrevActionType = "None"
            for i in range(len(data)):
                if data[i]["category"] != "REMOVED":
                    SaveCandidate.append(data[i])

            data = SaveCandidate.copy()
            with open("Saved/expenses.json", "w") as file:
                json.dump(data, file)

        if ActionType == "add":
            try:
                amount, category, description = Instruction.split(" ", 2)
                try:
                    NewVal = {
                        "amount": int(amount),
                        "category": category,
                        "description": description,
                    }
                    data.append(NewVal)
                    Utilities.printlist(data)
                except ValueError:
                    print("Invalid Integer!")
            except ValueError:
                print("Insufficient Arguments!")
        elif ActionType == "remove":
            try:
                data[int(Instruction) - 1] = DummyValue.copy()
                PrevActionType = "remove"
                print(f"Removed number {Instruction} from the list")
            except ValueError:
                print("Invalid Integer!")

        elif ActionType == "list":
            Utilities.printlist(data)
            with open("Saved/expenses.json", "w") as file:
                json.dump(data, file)

        elif ActionType == "edit":
            try:
                TargetNum, amount, category, description = Instruction.split(" ", 3)
                try:
                    print(
                        f"Edited {data[int(TargetNum)-1]['amount']} >> {amount}, {data[int(TargetNum)-1]['category']} >> {category}, {data[int(TargetNum)-1]['description']} >> {description},"
                    )
                    data[int(TargetNum) - 1] = {
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
        elif ActionType == "total":
            if Instruction == "None":
                print("count total ")
                Sum = 0
                for log in data:
                    Sum += log["amount"]
                print(f"The total is {Sum}!")

            elif Instruction != "None":
                print(f"count total for {Instruction}")
                Sum = 0
                for i in range(len(data)):
                    amount, category, description = (
                        data[i]["amount"],
                        data[i]["category"],
                        data[i]["description"],
                    )
                    if category == Instruction:
                        Sum += amount
                print(f"The total for {Instruction} is {Sum}!")
        Confirm = input("Do you have more to log?(y/n)")

        if Confirm == "y":
            ProgramRunning = True
        else:
            ProgramRunning = False


if __name__ == "__main__":
    main()
