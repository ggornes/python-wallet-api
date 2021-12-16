CREATE TABLE IF NOT EXISTS wallet.transactions (
    wallet_id           UUID NOT NULL,
    transaction_id      TEXT NOT NULL,
    transaction_amount  INT NOT NULL,
    balance             INT NOT NULL,
    version             INT NOT NULL,
    PRIMARY KEY (wallet_id, transaction_id),
    UNIQUE (wallet_id, version)
);
