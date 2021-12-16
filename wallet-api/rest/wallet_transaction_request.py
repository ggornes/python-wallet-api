import uuid

from pydantic import BaseModel

from domain.credit_command import CreditCommand
from domain.debit_command import DebitCommand
from domain.exceptions.illegal_transaction_amount_exception import IllegalTransactionAmountException


class WalletTransactionRequest(BaseModel):
    transaction_id: str
    coins: int

    def to_credit_command(self, wallet_id: uuid) -> CreditCommand:
        if self.coins <= 0: raise IllegalTransactionAmountException(self.transaction_id, self.coins)
        return CreditCommand(wallet_id, self.transaction_id, self.coins)

    def to_debit_command(self, wallet_id: uuid) -> DebitCommand:
        if self.coins <= 0: raise IllegalTransactionAmountException(self.transaction_id, self.coins)
        return DebitCommand(wallet_id, self.transaction_id, self.coins)
