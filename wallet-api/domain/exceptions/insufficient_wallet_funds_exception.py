class InsufficientWalletFundsException(Exception):
    def __init__(self, tx_amount: int, wallet_id: str, balance: int):
        self.tx_amount = tx_amount
        self.wallet_id = wallet_id
        self.balance = balance
        self.message = f"Could not debit {str(tx_amount)} from wallet {wallet_id} with balance {str(balance)}"