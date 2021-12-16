import unittest
import uuid

from domain.debit_command import DebitCommand
from domain.exceptions.insufficient_wallet_funds_exception import InsufficientWalletFundsException
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.credit_command import CreditCommand
from domain.transaction import Transaction
from domain.wallet import Wallet


class WalletTest(unittest.TestCase):
    WALLET_ID = uuid.uuid1()
    TX_ID_1 = "tx1"
    TX_ID_2 = "tx2"
    AMOUNT_50 = 50
    AMOUNT_100 = 100

    def test_givenEmptyWallet_whenCrediting_thenWalletIsUpdated(self):
        # given
        wallet = Wallet(self.WALLET_ID)

        # when
        tx = Transaction(self.WALLET_ID, self.TX_ID_1, self.AMOUNT_100, self.AMOUNT_100, 1)
        command = CreditCommand(tx.wallet_id, tx.transaction_id, tx.transaction_amount)

        # then
        actual_tx = wallet.credit(command)
        self.assertEqual(tx, actual_tx)

    def test_givenLoadedWallet_whenDebitingLessThanBalance_thenWalletIsUpdated(self):
        # given
        wallet = Wallet(self.WALLET_ID)
        tx1 = Transaction(self.WALLET_ID, self.TX_ID_1, self.AMOUNT_100, self.AMOUNT_100, 1)
        wallet.load(tx1)

        # when
        tx2 = Transaction(self.WALLET_ID, self.TX_ID_2, self.AMOUNT_50, self.AMOUNT_50, 2)
        command = DebitCommand(tx2.wallet_id, tx2.transaction_id, tx2.transaction_amount)

        # then
        actual_tx = wallet.debit(command)
        self.assertEqual(tx2, actual_tx)

    def test_givenEmptyWallet_whenDebiting_thenWalletNotFoundExceptionIsThrown(self):
        # given
        wallet = Wallet(self.WALLET_ID)

        # when
        command = DebitCommand(self.WALLET_ID, self.TX_ID_1, self.AMOUNT_100)
        with self.assertRaises(WalletNotFoundException) as context:
            wallet.debit(command)

        # then
        self.assertTrue(f"Wallet {wallet.wallet_id} not found" in context.exception.message)

    def test_givenLoadedWallet_whenDebitingMoreThanBalance_thenInsufficientWalletFundsExceptionIsThrown(self):
        # given
        wallet = Wallet(self.WALLET_ID)
        tx1 = Transaction(self.WALLET_ID, self.TX_ID_1, self.AMOUNT_50, self.AMOUNT_50, 1)
        wallet.load(tx1)

        # when
        command = DebitCommand(self.WALLET_ID, self.TX_ID_1, self.AMOUNT_100)
        with self.assertRaises(InsufficientWalletFundsException) as context:
            wallet.debit(command)

        # then
        self.assertTrue(f"Could not debit {str(self.AMOUNT_100)} from wallet {self.WALLET_ID} with balance {self.AMOUNT_50}" in context.exception.message)


if __name__ == '__main__':
    unittest.main()
