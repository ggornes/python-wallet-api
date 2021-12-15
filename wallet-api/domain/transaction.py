class Transaction:
    wallet_id: str
    transaction_id: str
    transaction_amount: int
    balance: int
    version: int

    def __init__(self, wallet_id: str, transaction_id: str, transaction_amount: int, balance: int, version: int):
        self.wallet_id = wallet_id
        self.transaction_id = transaction_id
        self.transaction_amount = transaction_amount
        self.balance = balance
        self.version = version

    def __str__(self):
        return "Transaction: " + self.wallet_id + " | " + self.transaction_id + " | " + str(self.transaction_amount) + " | " + str(self.balance) + " | " + str(self.version)

    def __eq__(self, o: object) -> bool:
        tx = (self.wallet_id, self.transaction_id)
        other_tx = (o.wallet_id, o.transaction_id)
        return tx == other_tx


