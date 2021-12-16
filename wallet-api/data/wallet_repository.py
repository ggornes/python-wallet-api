import abc
from uuid import UUID

from domain.wallet import Wallet


class WalletRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, wallet: Wallet) -> None:
        pass

    @abc.abstractmethod
    def load(self, wallet_id: UUID) -> Wallet:
        pass
