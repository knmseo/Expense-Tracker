import json
from dataclasses import dataclass

import Utilities


class ExpenseTrackerError(Exception):
    "Base Error for ExpenseTracker Application"


class InvalidUserInputError(ExpenseTrackerError):
    "Base Error when User Input is Invalid"


class InvalidActionError(InvalidUserInputError):
    "Attempted Action is not a possible action"


class InvalidTypeError(InvalidUserInputError):
    "The attempted user input has a invalid data type"


class InvalidInputFormatError(InvalidUserInputError):
    "The attempted user input was formatted incorrectly or had too little arguments"


@dataclass(kw_only=True)
class UserAction:

    @classmethod
    def FormatAction(cls, Instruction: str):
        pass

    def RunAction(self, Data):
        pass


@dataclass(kw_only=True)
class ActionAdd(UserAction):
    Amount: int
    Category: str
    Description: str

    @classmethod
    def FormatAction(cls, Instruction: str):
        try:
            amount, category, description = Instruction.split(" ", 2)
            try:
                return cls(
                    Amount=int(amount), Category=category, Description=description
                )
            except ValueError:
                raise InvalidTypeError("Invalid 'Amount' Value!")

        except ValueError:
            raise InvalidInputFormatError("Insufficient Arguments!")

    def RunAction(self, Data):
        Data.append(
            {
                "amount": self.Amount,
                "category": self.Category,
                "description": self.Description,
            }
        )
        Utilities.PrintList(Data)


@dataclass(kw_only=True)
class ActionRemove(UserAction):
    TargetIndex: int

    @classmethod
    def FormatAction(cls, Instruction: str):
        try:
            return cls(TargetIndex=int(Instruction))
        except ValueError:
            raise InvalidTypeError("Target index wasn't a valid integer!")

    def RunAction(self, Data):
        Data[self.TargetIndex - 1] = Utilities.DummyValue.copy()
        print(f"Removed number {self.TargetIndex} from the list")


@dataclass(kw_only=True)
class ActionList(UserAction):
    TargetCategory: str

    @classmethod
    def FormatAction(cls, Instruction: str):
        return cls(TargetCategory=Instruction)

    def RunAction(self, Data):
        if self.TargetCategory == "None":
            Utilities.PrintList(Data)
            with open("Saved/expenses.json", "w") as file:
                json.dump(Data, file)
        else:
            templist = []
            for entry in Data:
                if entry["category"] == self.TargetCategory:
                    templist.append(entry)
            if len(templist) == 0:
                print(f"There are no entries under category: {self.TargetCategory}")
            Utilities.PrintList(templist)
            with open("Saved/expenses.json", "w") as file:
                json.dump(Data, file)


@dataclass(kw_only=True)
class ActionEdit(UserAction):
    TargetIndex: int
    Amount: int
    Category: str
    Description: str

    @classmethod
    def FormatAction(cls, Instruction: str):
        try:
            targetindex, amount, category, description = Instruction.split(" ", 3)

            try:
                return cls(
                    TargetIndex=int(targetindex) - 1,
                    Amount=int(amount),
                    Category=category,
                    Description=description,
                )

            except ValueError as exc:
                raise InvalidTypeError(
                    f"There is an invalid integer in the input!: {exc}"
                ) from exc

        except ValueError:
            raise InvalidInputFormatError("Insufficient arguments!")

    def RunAction(self, Data):
        print(
            f"Edited "
            f"{Data[self.TargetIndex]['amount']} >> {self.Amount}, "
            f"{Data[self.TargetIndex]['category']} >> {self.Category}, "
            f"{Data[self.TargetIndex]['description']} >> {self.Description}"
        )

        Data[self.TargetIndex] = {
            "amount": self.Amount,
            "category": self.Category,
            "description": self.Description,
        }.copy()

        with open("Saved/expenses.json", "w") as file:
            json.dump(Data, file)


@dataclass(kw_only=True)
class ActionSum(UserAction):
    TargetCategory: str

    @classmethod
    def FormatAction(cls, Instruction: str):
        return cls(TargetCategory=Instruction)

    def RunAction(self, Data):
        if self.TargetCategory == "None":
            local_sum = 0
            for entry in Data:
                sum += entry["amount"]
            print(f"The total is {local_sum}!")

        elif self.TargetCategory != "None":
            local_sum = 0
            for entry in Data:
                amount, category = entry["amount"], entry["category"]
                if category == self.TargetCategory:
                    local_sum += amount
            if local_sum == 0:
                print("Invalid Category!")
            print(f"The total for {self.TargetCategory} is {local_sum}!")


def BuildAction(RawUserInput: str) -> tuple[str, UserAction]:
    ActionType, Instruction = Utilities.SplitRawInput(RawUserInput)
    if ActionType not in ACTIONS:
        raise InvalidActionError
    else:
        useraction = ACTIONS[ActionType].FormatAction(Instruction)

    return ActionType, useraction


ACTIONS = {
    "add": ActionAdd,
    "remove": ActionRemove,
    "list": ActionList,
    "edit": ActionEdit,
    "sum": ActionSum,
}


def run(Data: list) -> None:
    PrevActionType = "None"
    while True:
        try:
            ActionType, UserAction = BuildAction(
                input("Enter the next action: ").strip()
            )
            PrevActionType, Data = Utilities.CustomWriteJSON(
                PrevActionType,
                ActionType,
                Data,
                Path="Saved/expenses.json",
            )

            UserAction.RunAction(Data)

            if ActionType == "remove":
                PrevActionType = "remove"
        except InvalidInputFormatError as exc:
            print(f"Your input format was Invalid: {exc}")
        except InvalidTypeError as exc:
            print(f"There was a type error in your input: {exc}")
        except InvalidActionError as exc:
            print(f"There was no valid action related to your input: {exc}")
        except InvalidUserInputError as exc:
            print(f"There was a unrecognizable error in your input: {exc}")

        confirm = input("Do you have more to log?(y/n)").strip().lower()
        if confirm != "y":
            break


def main():
    Data = Utilities.LoadFile("Saved/expenses.json")
    run(Data)


if __name__ == "__main__":
    main()
