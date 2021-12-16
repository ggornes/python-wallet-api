import abc
from uuid import UUID

from domain.wallet_balance import WalletBalance


class WalletBalanceRepository(abc.ABC):
    @abc.abstractmethod
    def load_wallet_balance(self, wallet_id: UUID) -> WalletBalance:
        pass
