class VersionMissmatchException(Exception):
    def __init__(self, wallet_id: str):
        self.message = f"Wallet {wallet_id} version is not ax expected"
