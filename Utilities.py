import json

DummyValue = {
    "amount": 0,
    "category": "REMOVED",
    "description": "None",
}

ActionTypes = {"add", "remove", "list", "edit", "total"}


def printlist(data):
    index = 1
    for i in range(len(data)):
        category = data[i]["category"]

        if category != "REMOVED":
            print(
                f"{index}: {data[i]['amount']} / {data[i]['category']} / {data[i]['description']}"
            )
            index += 1


def LoadFile(Path):
    try:
        with open(Path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("The JSON file is corrupted or doesn't exist?")
        data = []

    return data


def SplitRawInput(RawInput):
    TempList = RawInput.split(" ", 1)
    if len(TempList) == 1:
        ActionType = TempList[0]
        Instruction = "None"
    elif len(TempList) == 2:
        ActionType, Instruction = TempList

    return ActionType, Instruction


def CustomWriteJSON(PrevActionType, ActionType, data, Path):
    SaveCandidate = []
    if PrevActionType == "remove" and ActionType != "remove":
        PrevActionType = "None"
        for i in range(len(data)):
            if data[i]["category"] != "REMOVED":
                SaveCandidate.append(data[i])

        data = SaveCandidate.copy()
        with open(Path, "w") as file:
            json.dump(data, file)

    return PrevActionType, data


def CalcTotal(data, Instruction):
    if Instruction == "None":
        Sum = 0
        for log in data:
            Sum += log["amount"]
        print(f"The total is {Sum}!")

    elif Instruction != "None":
        Sum = 0
        for i in range(len(data)):
            amount, category = (data[i]["amount"], data[i]["category"])
            if category == Instruction:
                Sum += amount
        if Sum == 0:
            print("Invalid Category!")
        print(f"The total for {Instruction} is {Sum}!")
