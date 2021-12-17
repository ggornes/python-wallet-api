from uuid import UUID

from psycopg2 import DatabaseError

from data.wallet_balance_repository import WalletBalanceRepository
from data.wallet_repository import WalletRepository
from domain.exceptions.duplicate_transaction_exception import DuplicateTransactionException
from domain.exceptions.version_mismatch_exception import VersionMissmatchException
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.transaction import Transaction
from domain.wallet import Wallet
from domain.wallet_balance import WalletBalance

GET_LATEST_WALLET_STATE = "SELECT transaction_id, transaction_amount, balance, version " \
                          "FROM wallet.transactions " \
                          "WHERE wallet_id = %s " \
                          "ORDER BY version " \
                          "DESC LIMIT 1"

INSERT_TRANSACTION = "INSERT INTO wallet.transactions (wallet_id, transaction_id, transaction_amount, balance, " \
                      "version) VALUES (%s, %s, %s, %s, %s)"

UNIQUE_VIOLATION_STATUS_CODE = "23505"
DUPLICATE_TX_ID_ERROR = "duplicate key value violates unique constraint \"transactions_pkey\""
VERSION_MISSMATCH_ERROR = "duplicate key value violates unique constraint \"transactions_wallet_id_version_key\""


class BaseRepository:

    def __init__(self, connection) -> None:
        self.connection = connection


class PostgresWalletRepository(BaseRepository, WalletRepository, WalletBalanceRepository):

    def save(self, wallet: Wallet) -> None:
        wallet_id = wallet.wallet_id
        unsaved_transactions = wallet.unsaved_transactions
        new_transactions = []

        for tx in unsaved_transactions:
            new_transaction = (
                wallet_id,
                tx.transaction_id,
                tx.transaction_amount,
                tx.balance,
                tx.version
            )
            new_transactions.append(new_transaction)

        cursor = self.connection.cursor()
        try:
            cursor.executemany(INSERT_TRANSACTION, new_transactions)
            self.connection.commit()
        except DatabaseError as error:
            self.connection.rollback()
            cursor.close()
            if error.pgcode == UNIQUE_VIOLATION_STATUS_CODE:
                if DUPLICATE_TX_ID_ERROR in error.pgerror:
                    latest_wallet_balance = self.load_wallet_balance(wallet_id)
                    raise DuplicateTransactionException(latest_wallet_balance)
                if VERSION_MISSMATCH_ERROR in error.pgerror:
                    raise VersionMissmatchException(wallet_id)
            raise RuntimeError
        cursor.close()
        unsaved_transactions.clear()

    def load(self, wallet_id: UUID) -> Wallet:
        wallet = Wallet(wallet_id)
        cursor = self.connection.cursor()
        try:
            cursor.execute(GET_LATEST_WALLET_STATE, (wallet.wallet_id,))
            loaded_tx = cursor.fetchone()
        except DatabaseError:
            cursor.close()
            raise RuntimeError
        cursor.close()

        if loaded_tx is not None:
            tx_id = loaded_tx[0]
            tx_amount = loaded_tx[1]
            tx_balance = loaded_tx[2]
            tx_version = loaded_tx[3]
            transaction = Transaction(wallet_id, tx_id, tx_amount, tx_balance, tx_version)
            wallet.load(transaction)

        return wallet

    def load_wallet_balance(self, wallet_id: UUID) -> WalletBalance:
        wallet = Wallet(wallet_id)
        cursor = self.connection.cursor()
        try:
            cursor.execute(GET_LATEST_WALLET_STATE, (wallet.wallet_id,))
            loaded_tx = cursor.fetchone()
        except DatabaseError:
            cursor.close()
            raise RuntimeError
        cursor.close()

        if loaded_tx is not None:
            tx_id = loaded_tx[0]
            tx_amount = loaded_tx[1]
            tx_balance = loaded_tx[2]
            tx_version = loaded_tx[3]
            transaction = Transaction(wallet_id, tx_id, tx_amount, tx_balance, tx_version)
            return WalletBalance.from_transaction(transaction)
        else:
            raise WalletNotFoundException(wallet_id)
