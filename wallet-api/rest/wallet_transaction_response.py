from pydantic import BaseModel


class WalletTransactionResponse(BaseModel):
    transaction_id: str
    coins: int
