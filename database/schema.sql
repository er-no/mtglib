PRAGMA foreign_keys = OFF;

-- drop tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS collections;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS deck_lists;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS mana_costs;
DROP TABLE IF EXISTS card_sets;

PRAGMA foreign_keys = ON;

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
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    PRIMARY KEY (deck_id)
);

CREATE TABLE deck_lists (
    deck_list_id   INTEGER NOT NULL,
    deck_reference INTEGER,
    set_code       TEXT,
    card_number    INTEGER,
    FOREIGN KEY    (deck_reference) REFERENCES decks(deck_id),
    FOREIGN KEY    (set_code, card_number) REFERENCES cards(set_code, card_number),
    PRIMARY KEY    (deck_list_id)
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

INSERT INTO mana_costs(mana_id, cost) VALUES (0, "[L]");

-- deck constraints
-- deck must never contain more than 4 of the same non-basic-land card, decided by name
DROP TRIGGER IF EXISTS playset_rule;
CREATE TRIGGER playset_rule
BEFORE INSERT ON deck_lists
BEGIN
    SELECT CASE WHEN (
        SELECT   count()
        FROM     deck_lists
        JOIN     cards
        USING    (set_code, card_number)
        WHERE    deck_reference = NEW.deck_reference
        AND      card_name = (SELECT card_name FROM cards WHERE set_code = NEW.set_code AND card_number = NEW.card_number)
        GROUP BY card_name
    ) >= 4
    THEN
        RAISE (ROLLBACK, "You can not have more than four of the same non-land cards in your deck!")
    END;
END;

-- you can not list a card in your deck if you do not own it
DROP TRIGGER IF EXISTS must_own_cards;
CREATE TRIGGER must_own_cards
BEFORE INSERT ON deck_lists
BEGIN
    SELECT CASE WHEN (
        SELECT
        ( -- find number in collection
            SELECT count()
            FROM   collections
            WHERE  owner_id = ( -- find owner of the deck that NEW refers to
                SELECT          owner_id
                FROM            decks
                LEFT OUTER JOIN deck_lists ON(deck_reference = deck_id)
                WHERE           deck_id = NEW.deck_reference
            )
            AND set_code = NEW.set_code
            AND card_number = NEW.card_number
        )
        -
        ( -- find number in deck_list
            SELECT count()
            FROM   deck_lists
            WHERE  deck_reference = NEW.deck_reference
            AND    set_code = NEW.set_code
            AND    card_number = NEW.card_number
        )
    ) <= 0
    THEN
        RAISE (ROLLBACK, "You do not have enough copies in your collection!")
    END;
END;
