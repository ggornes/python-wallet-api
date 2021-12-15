from domain.transaction import Transaction


class WalletBalance:
    transaction_id: str
    balance: int
    version: int

    def __init__(self, transaction_id: str, balance: int, version: int):
        self.transaction_id = transaction_id
        self.balance = balance
        self.version = version

    @staticmethod
    def from_transaction(tx: Transaction):
        return WalletBalance(tx.transaction_id, tx.balance, tx.version)
