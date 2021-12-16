from uuid import UUID

from data.wallet_balance_repository import WalletBalanceRepository
from domain.wallet_balance import WalletBalance


class QueryHandler:
    wallet_balance_repository = WalletBalanceRepository

    def __init__(self, wallet_balance_repo: WalletBalanceRepository):
        self.wallet_balance_repository = wallet_balance_repo

    async def handle(self, query: UUID) -> WalletBalance:
        wallet_balance = await self.wallet_balance_repository.load_wallet_balance(query)
        return wallet_balance
