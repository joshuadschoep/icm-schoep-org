from enum import Enum
from typing import List, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, PositiveInt, conlist, model_validator, ValidationError

class Player(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=63, frozen=True)]] = None
    stack: PositiveInt

class Request(BaseModel):
    payouts: conlist(PositiveInt, min_length=1, max_length=12)
    players: conlist(Player, min_length=1, max_length=12)

    @model_validator(mode='after')
    def more_players_than_payouts(self):
        if len(self.payouts) > len(self.players):
            raise ValidationError("There must be more players than remaining payouts")
        return self

class Version(str, Enum):
    V1 = "1.0"
    V2 = "2.0"