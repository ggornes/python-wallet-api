from data.wallet_repository import WalletRepository
from domain.credit_command import CreditCommand
from domain.debit_command import DebitCommand
from domain.transaction import Transaction


class CommandHandler:
    wallet_repository: WalletRepository

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repository = wallet_repo

    def handle_credit(self, command: CreditCommand) -> Transaction:
        wallet_id = command.wallet_id
        wallet = self.wallet_repository.load(wallet_id)
        transaction = wallet.credit(command)
        self.wallet_repository.save(wallet)
        return transaction

    def handle_debit(self, command: DebitCommand) -> Transaction:
        wallet_id = command.wallet_id
        wallet = self.wallet_repository.load(wallet_id)
        transaction = wallet.debit(command)
        self.wallet_repository.save(wallet)
        return transaction
