CREATE TABLE wallets
(
    id       serial PRIMARY KEY,
    value    integer DEFAULT 0 NOT NULL CHECK (value >= 0),
    name     text
);


CREATE TABLE users_wallets (
    user_id   serial REFERENCES users(id),
    wallet_id   serial REFERENCES wallets(id),
    PRIMARY KEY (user_id, wallet_id)
);


CREATE TABLE wallets_history
(
    id       serial PRIMARY KEY,
    wallet_id   serial REFERENCES wallets(id),
    value    integer,
    label    text
);
