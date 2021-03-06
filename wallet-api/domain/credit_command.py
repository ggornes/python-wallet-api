from uuid import UUID


class CreditCommand:
    wallet_id: UUID
    transaction_id: str
    transaction_amount: int

    def __init__(self, wallet_id: UUID, transaction_id: str, transaction_amount: int):
        self.wallet_id = wallet_id
        self.transaction_id = transaction_id
        self.transaction_amount = transaction_amount
