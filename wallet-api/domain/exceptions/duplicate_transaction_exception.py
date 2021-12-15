from domain.transaction import Transaction


class DuplicateTransactionException(Exception):
    def __init__(self, tx: Transaction):
        self.transaction_id = tx.transaction_id
        self.version = tx.version
        self.balance = tx.balance
        self.message = f"Wallet already contains transaction {self.transaction_id}"
