from uuid import UUID
from databases import Database

from data.wallet_balance_repository import WalletBalanceRepository
from data.wallet_repository import WalletRepository
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.wallet import Wallet
from domain.wallet_balance import WalletBalance

GET_LATEST_WALLET_STATE = "SELECT transaction_id, transaction_amount, version, balance " \
                          "FROM wallet.transactions " \
                          "WHERE wallet_id = :wallet_id " \
                          "ORDER BY version " \
                          "DESC LIMIT 1"

INSERT_TRANSACTION = "INSERT INTO wallet.transactions (wallet_id, transaction_id, transaction_amount, balance, " \
                     "version) VALUES (:wallet_id, :transaction_id, :transaction_amount, :balance, :version)"


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.db = db


class PostgresWalletRepository(BaseRepository, WalletRepository, WalletBalanceRepository):

    async def save(self, wallet: Wallet) -> None:
        wallet_id = wallet.wallet_id
        unsaved_transactions = wallet.unsaved_transactions
        new_transactions = []
        for tx in unsaved_transactions:
            new_transaction = {
                "wallet_id": wallet_id,
                "transaction_id": tx.transaction_id,
                "transaction_amount": tx.transaction_amount,
                "balance": tx.balance,
                "version": tx.version
            }
            new_transactions.append(new_transaction)
        await self.db.execute_many(query=INSERT_TRANSACTION, values=new_transactions)

    async def load(self, wallet_id: UUID) -> Wallet:
        wallet = Wallet(wallet_id)
        result = await self.db.fetch_one(query=GET_LATEST_WALLET_STATE, values={"wallet_id": wallet.wallet_id})
        # result = <databases.backends.postgres.Record object at 0x7fbf755ae3b0>
        # todo: parse postgres object and instantiate transaction object
        if not (result is None):
            wallet.load(result)
        return wallet

    async def load_wallet_balance(self, wallet_id: UUID) -> WalletBalance:
        wallet = Wallet(wallet_id)
        result = await self.db.fetch_one(query=GET_LATEST_WALLET_STATE, values={"wallet_id": wallet.wallet_id})
        # result = <databases.backends.postgres.Record object at 0x7fbf755ae3b0>
        # todo: parse postgres object and instantiate transaction object
        if not (result is None):
            return WalletBalance.from_transaction(result)
        else:
            raise WalletNotFoundException(wallet_id)
