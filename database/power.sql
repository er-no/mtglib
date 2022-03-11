-- creates a user "power" that owns a playset of every card

PRAGMA foreign_keys = ON;

-- create the power user
INSERT INTO users(nickname) VALUES ("power");

-- insert all cards and do it four times
INSERT INTO collections(owner_id, set_code, card_number)
SELECT  (SELECT user_id FROM users WHERE nickname LIKE "power"),
        set_code,
        card_number
FROM    cards;

INSERT INTO collections(owner_id, set_code, card_number)
SELECT  (SELECT user_id FROM users WHERE nickname LIKE "power"),
        set_code,
        card_number
FROM    cards;

INSERT INTO collections(owner_id, set_code, card_number)
SELECT  (SELECT user_id FROM users WHERE nickname LIKE "power"),
        set_code,
        card_number
FROM    cards;

INSERT INTO collections(owner_id, set_code, card_number)
SELECT  (SELECT user_id FROM users WHERE nickname LIKE "power"),
        set_code,
        card_number
FROM    cards;
