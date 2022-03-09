PRAGMA foreign_keys=OFF;

-- drop tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS card_inventories;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS deck_lists; -- renamed from DeckEntry in ER.png
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS mana_costs;
DROP TABLE IF EXISTS expansions; -- renamed from Set in /docs/ER.png

PRAGMA foreign_keys=ON;

-- create tables
CREATE TABLE users (
    user_id     INTEGER,
    nickname    TEXT, -- renamed from name in /docs/ER.png
    UNIQUE      (nickname),
    PRIMARY KEY (user_id)
);

CREATE TABLE card_inventories (
    inventory_id   INTEGER,
    owner_id       INTEGER,
    card_number    INTEGER,
    expansion_code INTEGER,
    FOREIGN KEY    (owner_id) REFERENCES users(user_id),
    FOREIGN KEY    (card_number, expansion_code) REFERENCES cards(card_number, expansion_code),
    PRIMARY KEY    (inventory_id)
);

CREATE TABLE decks (
    deck_id     INTEGER,
    owner_id    INTEGER,
    deck_name   TEXT,
    UNIQUE      (owner_id, deck_name),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE deck_lists ( -- renamed from DeckEntry in ER.png
    deck_list_id   INTEGER,
    deck_reference INTEGER,
    card_number    INTEGER,
    expansion_code TEXT,
    FOREIGN KEY    (deck_reference) REFERENCES decks(deck_id),
    FOREIGN KEY    (card_number, expansion_code) REFERENCES cards(card_number, expansion_code)
);

CREATE TABLE cards (
    expansion_code  TEXT,
    card_number     INTEGER,
    card_name       TEXT,
    rarity          INTEGER,
    mana_id         INTEGER,
    UNIQUE          (card_name, card_number, expansion_code),
    FOREIGN KEY     (expansion_code) REFERENCES expansions(expansion_id),
    FOREIGN KEY     (mana_id) REFERENCES mana_costs(mana_id),
    PRIMARY KEY     (expansion_code, card_number)
);

CREATE TABLE mana_costs (
    mana_id     INTEGER,
    cost        TEXT,
    UNIQUE      (cost),
    PRIMARY KEY (mana_id)
);

CREATE TABLE expansions ( -- renamed from Set in /docs/ER.png
    expansion_id   TEXT,
    expansion_name TEXT,
    max_count      INTEGER,
    UNIQUE         (expansion_name),
    PRIMARY KEY    (expansion_id)
);

INSERT INTO mana_costs(mana_id, cost) VALUES (1, "[L]")
