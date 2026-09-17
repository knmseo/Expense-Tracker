from dataclasses import dataclass


@dataclass(kw_only=True)
class AttemptedAction:
    ActionType: str


@dataclass(kw_only=True)
class ActionAdd(AttemptedAction):
    amount: int
    category: str
    description: str
    ActionType: str = "add"


a = ActionAdd(amount=60, category="groceries", description="lunch")
print(a.ActionType)
