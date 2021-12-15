class WalletNotFoundException(Exception):
    def __init__(self, wallet_id: str):
        self.wallet_id = wallet_id
        self.message = f"Wallet {wallet_id} not found"
