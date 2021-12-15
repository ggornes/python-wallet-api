from domain.credit_command import CreditCommand
from domain.debit_command import DebitCommand
from domain.exceptions.insufficient_wallet_funds_exception import InsufficientWalletFundsException
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.transaction import Transaction


class Wallet:
    wallet_id: str
    balance: int
    version: int
    unsaved_transactions = []

    def __init__(self, wallet_id: str):
        self.wallet_id = wallet_id
        self.balance = 0
        self.version = 0

    def credit(self, command: CreditCommand) -> Transaction:
        updated_balance = self.balance + command.transaction_amount
        updated_version = self.version + 1
        tx = Transaction(
            self.wallet_id,
            command.transaction_id,
            command.transaction_amount,
            updated_balance,
            updated_version
        )
        self.apply_transaction(tx)
        return tx

    def debit(self, command: DebitCommand) -> Transaction:
        if self.version == 0: raise WalletNotFoundException(command.wallet_id)
        if self.balance <= command.transaction_amount: raise InsufficientWalletFundsException(command.transaction_amount, command.wallet_id, self.balance)
        updated_balance = self.balance - command.transaction_amount
        updated_version = self.version + 1
        tx = Transaction(
            self.wallet_id,
            command.transaction_id,
            command.transaction_amount,
            updated_balance,
            updated_version
        )
        self.apply_transaction(tx)
        return tx

    def apply_transaction(self, tx: Transaction) -> None:
        self.balance = tx.balance
        self.version = tx.version
        self.unsaved_transactions.append(tx)

    def load(self, tx: Transaction) -> None:
        self.balance = tx.balance
        self.version = tx.version
