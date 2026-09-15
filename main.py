import json

import Utilities


def main():
    PrevActionType = "None"
    data = Utilities.LoadFile("Saved/expenses.json")
    ProgramRunning = True

    while ProgramRunning:
        RawUserInstruction = input("Enter the next action: ")
        ActionType, Instruction = Utilities.SplitRawInput(RawUserInstruction)

        if not ActionType in Utilities.ActionTypes:
            print("This is not a valid action!")
            continue

        PrevActionType, data = Utilities.CustomWriteJSON(
            PrevActionType, ActionType, data, Path="Saved/expenses.json"
        )

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
                data[int(Instruction) - 1] = Utilities.DummyValue.copy()
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
                    TargetNum = int(TargetNum)
                    TargetNum -= 1
                    print(
                        f"Edited {data[TargetNum]['amount']} >> {amount}, {data[TargetNum]['category']} >> {category}, {data[TargetNum]['description']} >> {description},"
                    )
                    data[int(TargetNum)] = {
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
            Utilities.CalcTotal(data, Instruction)

        Confirm = input("Do you have more to log?(y/n)")
        if Confirm == "y":
            ProgramRunning = True
        else:
            ProgramRunning = False


if __name__ == "__main__":
    main()
