from uuid import UUID

from fastapi import APIRouter, status, Request, FastAPI
from starlette.responses import JSONResponse
from data.in_memory_wallet_repository import InMemoryWalletRepository
from domain.command_handler import CommandHandler
from domain.exceptions.duplicate_transaction_exception import DuplicateTransactionException
from domain.exceptions.illegal_transaction_amount_exception import IllegalTransactionAmountException
from domain.exceptions.insufficient_wallet_funds_exception import InsufficientWalletFundsException
from domain.exceptions.version_mismatch_exception import VersionMissmatchException
from domain.exceptions.wallet_not_found import WalletNotFoundException
from domain.query_handler import QueryHandler
from rest.wallet_balance_response import WalletBalanceResponse
from rest.wallet_transaction_request import WalletTransactionRequest
from rest.wallet_transaction_response import WalletTransactionResponse


def get_application():
    app = FastAPI(title="Wallet API")
    return app


app = get_application()

router = APIRouter()

wallet_repository = InMemoryWalletRepository()
commandHandler = CommandHandler(wallet_repository)
queryHandler = QueryHandler(wallet_repository)


@router.get("/wallets/{wallet_id}",
            status_code=status.HTTP_200_OK, response_model=WalletBalanceResponse)
def handle_wallet_balance_request(wallet_id: UUID):
    wallet_balance = queryHandler.handle(wallet_id)
    return WalletBalanceResponse(transaction_id=wallet_balance.transaction_id,
                                 version=wallet_balance.version,
                                 coins=wallet_balance.balance)


@router.post("/wallets/{wallet_id}/credit",
             status_code=status.HTTP_201_CREATED, response_model=WalletTransactionResponse)
def handle_credit_request(wallet_id: UUID, req: WalletTransactionRequest):
    credit_command = req.to_credit_command(wallet_id)
    transaction = commandHandler.handle_credit(credit_command)
    return WalletTransactionResponse(transaction_id=transaction.transaction_id,
                                     coins=transaction.transaction_amount)


@router.post("/wallets/{wallet_id}/debit",
             status_code=status.HTTP_201_CREATED, response_model=WalletTransactionResponse)
def handle_debit_request(wallet_id: UUID, req: WalletTransactionRequest):
    debit_command = req.to_debit_command(wallet_id)
    transaction = commandHandler.handle_debit(debit_command)
    return WalletTransactionResponse(transaction_id=transaction.transaction_id,
                                     coins=transaction.transaction_amount)


@app.exception_handler(WalletNotFoundException)
def handle_wallet_not_found_exception(req: Request, ex: WalletNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": ex.message},
    )


@app.exception_handler(DuplicateTransactionException)
def handle_duplicate_transaction_exception(req: Request, ex: DuplicateTransactionException):
    return JSONResponse(
        status_code=202,
        content={"message": ex.message},
    )


@app.exception_handler(InsufficientWalletFundsException)
def handle_insufficient_wallet_funds_exception(req: Request, ex: InsufficientWalletFundsException):
    return JSONResponse(
        status_code=400,
        content={"message": ex.message}
    )


@app.exception_handler(IllegalTransactionAmountException)
def handle_illegal_transaction_amount_exception(req: Request, ex: IllegalTransactionAmountException):
    return JSONResponse(
        status_code=400,
        content={"message": ex.message}
    )


@app.exception_handler(VersionMissmatchException)
def handle_version_missmatch_exception(req: Request, ex: VersionMissmatchException):
    return JSONResponse(
        status_code=400,
        content={"message": ex.message}
    )


@app.exception_handler(RuntimeError)
def handle_run_time_error_exception(req: Request, ex: RuntimeError):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


app.include_router(router)
