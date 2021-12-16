from uuid import UUID

from data.wallet_balance_repository import WalletBalanceRepository
from data.wallet_repository import WalletRepository
from domain.exceptions.duplicate_transaction_exception import DuplicateTransactionException
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.transaction import Transaction
from domain.wallet import Wallet
from domain.wallet_balance import WalletBalance


class InMemoryWalletRepository(WalletRepository, WalletBalanceRepository):
    wallet_repo = dict()

    def save(self, wallet: Wallet) -> None:
        wallet_id = wallet.wallet_id
        saved_transactions = self.get_saved_transactions(wallet_id)
        unsaved_transactions = wallet.unsaved_transactions
        new_transactions = []

        if not saved_transactions:
            saved_transactions.extend(unsaved_transactions)
        else:
            for tx in unsaved_transactions:
                if tx in saved_transactions: raise DuplicateTransactionException(tx)
                new_transactions.append(tx)
            saved_transactions.extend(new_transactions)

        self.wallet_repo[wallet_id] = saved_transactions
        unsaved_transactions.clear()

    def load(self, wallet_id: UUID) -> Wallet:
        wallet = Wallet(wallet_id)
        if wallet.wallet_id in self.wallet_repo.keys():
            latest_transaction = self.get_latest_transaction(wallet_id)
            wallet.load(latest_transaction)
        return wallet

    def load_wallet_balance(self, wallet_id: UUID) -> WalletBalance:
        if wallet_id in self.wallet_repo.keys():
            latest_transaction = self.get_latest_transaction(wallet_id)
            return WalletBalance.from_transaction(latest_transaction)
        else:
            raise WalletNotFoundException(wallet_id)

    def get_saved_transactions(self, wallet_id: UUID):
        return self.wallet_repo.get(wallet_id) or []

    def get_latest_transaction(self, wallet_id: UUID) -> Transaction:
        saved_transactions = self.get_saved_transactions(wallet_id)
        return saved_transactions[-1]
