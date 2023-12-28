-- Создать таблицу Wallet (id, value, name) [пример: (1, Yandex, 1000), (2, Sber, 1500)] + ограничение (constaint на value >= 0)

CREATE TABLE wallets
(
    id       serial PRIMARY KEY,
    value    integer DEFAULT 0 NOT NULL CHECK (value >= 0),
    name     text
);

-- Добавить таблицу UserWallet (user_id, wallet_id) [пример: (1, 1), (1, 2)]

CREATE TABLE users_wallets (
    user_id   serial REFERENCES users(id),
    wallet_id   serial REFERENCES wallets(id),
    PRIMARY KEY (user_id, wallet_id)
);

-- WalletHistory (id, wallet_id, value, label: string) -- value мб положительным и отрицательным

CREATE TABLE wallets_history
(
    id       serial PRIMARY KEY,
    wallet_id   serial REFERENCES wallets(id),
    value    integer,
    label    text
);