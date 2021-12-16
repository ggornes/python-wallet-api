from pydantic import BaseModel


class WalletBalanceResponse(BaseModel):
    transaction_id: str
    version: int
    coins: int