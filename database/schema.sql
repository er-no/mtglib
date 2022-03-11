PRAGMA foreign_keys=OFF;

-- drop tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS collections;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS deck_lists;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS mana_costs;
DROP TABLE IF EXISTS card_sets;

PRAGMA foreign_keys=ON;

-- create tables
CREATE TABLE users (
    user_id     INTEGER,
    nickname    TEXT,
    UNIQUE      (nickname),
    PRIMARY KEY (user_id)
);

CREATE TABLE collections (
    collection_id INTEGER,
    owner_id      INTEGER,
    set_code      TEXT,
    card_number   INTEGER,
    FOREIGN KEY   (owner_id) REFERENCES users(user_id),
    FOREIGN KEY   (set_code, card_number) REFERENCES cards(set_code, card_number),
    PRIMARY KEY   (collection_id)
);

CREATE TABLE decks (
    deck_id     INTEGER,
    owner_id    INTEGER,
    deck_name   TEXT,
    UNIQUE      (owner_id, deck_name),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE deck_lists (
    deck_list_id   INTEGER,
    deck_reference INTEGER,
    set_code       TEXT,
    card_number    INTEGER,
    FOREIGN KEY    (deck_reference) REFERENCES decks(deck_id),
    FOREIGN KEY    (set_code, card_number) REFERENCES cards(set_code, card_number)
);

CREATE TABLE cards (
    set_code    TEXT,
    card_number INTEGER,
    card_name   TEXT,
    rarity      INTEGER,
    mana_id     INTEGER,
    UNIQUE      (card_name, card_number, set_code),
    FOREIGN KEY (set_code) REFERENCES card_sets(set_code),
    FOREIGN KEY (mana_id) REFERENCES mana_costs(mana_id),
    PRIMARY KEY (set_code, card_number)
);

CREATE TABLE mana_costs (
    mana_id     INTEGER,
    cost        TEXT,
    UNIQUE      (cost),
    PRIMARY KEY (mana_id)
);

CREATE TABLE card_sets (
    set_code       TEXT,
    set_name       TEXT,
    max_count      INTEGER,
    UNIQUE         (set_name),
    PRIMARY KEY    (set_code)
);

INSERT INTO mana_costs(mana_id, cost) VALUES (0, "[L]")
