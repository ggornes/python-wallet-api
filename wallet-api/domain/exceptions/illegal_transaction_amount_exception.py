class IllegalTransactionAmountException(Exception):
    def __init__(self, tx_id: str, tx_amount: int):
        self.message = f"Incorrect transaction amount {str(tx_amount)} for transactionId {tx_id}. Amount must be greater than zero"