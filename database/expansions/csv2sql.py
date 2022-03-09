from os.path import exists
import sys

# supports standard format
codes_to_info = {
    'ZNR' : ['\"Zendikar Rising\"', 391],
    'KHM' : ['\"Kaldheim\"', 405],
    'STX' : ['\"Strixhaven: School of Mages\"', 382],
    'STA' : ['\"Strixhaven: Mystical Archive\"', 126],
    'AFR' : ['\"Dungeons & Dragons: Adventures in the Forgotten Realms\"', 402],
    'MID' : ['\"Innistrad: Midnight Hunt\"', 391],
    'VOW' : ['\"Innistrad: Crimson Vow\"', 412],
    'NEO' : ['\"Kamigawa: Neon Dynasty\"', 512]
}

# will be strings in query but numbers while stored
rarity_to_int = {
    'C' : '1',
    'U' : '2',
    'R' : '3',
    'M' : '4'
}

# queries the database and inserts the expansion
def insert_expansion(set_code, set_name, max_count, sql_file):
    # insert the expansion into the expansions table
    sql_file.write("-- create the expansion\n")
    sql_file.write("INSERT INTO expansions (expansion_id, expansion_name, max_count)\n")
    sql_file.write("VALUES (\"" + set_code + "\", " + set_name + ", " + max_count + ");\n\n")

# looks through the cards raw data and returns all unique mana costs.
def unique_mana_costs(cards):
    manas = {"[L]"}
    for card in cards:
        mana = card[3]
        if mana != "" and mana != "cost" and mana not in manas:
            manas.add(mana)
    return manas

# takes a list of mana costs and inserts them as sql syntax in sql_file
def populate_mana(manas, sql_file):
    sql_file.write("-- populate mana table\n")
    sql_file.write("INSERT OR IGNORE INTO mana_costs (cost) VALUES\n")
    width = 0
    for mana in manas:
        if width >= 50: # formatting, estetical, never get too wide
            sql_file.write(",\n")
            width = 0

        s = ", (\"" + mana + "\")"
        if width == 0: # if first like, remove the comma and space
            s = s[2:len(s)]

        sql_file.write(s)
        width += len(s)

# takes a list of cards and inserts them as sql syntax in sql_file
def populate_cards(cards, sql_file):
    sql_file.write(";\n\n-- populate with card data\n")
    sql_file.write("INSERT INTO cards (set_code, card_number, card_name, mana_id, rarity) VALUES\n")
    for card in cards:
        set_code = card[0]
        card_number = card[1]
        card_name = card[2]
        # make sure lands are represented as [L] cost
        mana_cost = card[3] if card[3] != "" else "[L]"
        card_rarity = card[4]
        # writing ("exp_code", card_nbr, "card_name", (QUERY FOR MANA), rarity)
        sql_file.write(
            "(\"" + set_code +
            "\", " + card_number +
            ", \"" + card_name +
            "\", (SELECT mana_id FROM mana_costs WHERE cost = \"" + mana_cost + "\")" +
            ", " + rarity_to_int.get(card_rarity) + ")")
        if int(card_number) == codes_to_info.get(set_code)[1]: # if it is the last card
            sql_file.write(";\n") # append a semicolon
        else: # elese -- its not the last card
            sql_file.write(",\n") # so append a comma

def main(set_code):
    if set_code not in codes_to_info:
        if set_code == "ALL":
            print("generating for all known sets!")
            for code in codes_to_info.keys():
                main(code)
                print(code + "... done!")
            exit(0)
        else:
            print("ERROR: UNKNOWN_SET [" + set_code + "]")
            exit(1)

    if not exists("../data/" + set_code + ".csv"):
        print("ERROR: UNKNOWN_FILE [../data/" + set_code + ".csv]")
        exit(1)

    set_info = codes_to_info.get(set_code)
    sql_file = open(set_code + ".sql", "w")
    csv_file = open("../data/" + set_code + ".csv", "r")
    csv_raw = csv_file.read().splitlines()
    # cards filtered where cardnumber MUST be numeric (skipping alternate arts)
    cards = [c.split(";") for c in csv_raw if c.split(";")[1].isnumeric()]

    # insert the actual set into DB
    insert_expansion(set_code, set_info[0], str(set_info[1]), sql_file)

    # find all unique mana costs
    manas = unique_mana_costs(cards)

    # now we can insert the unique mana costs (reducing number of values passed to DB)
    populate_mana(manas, sql_file)

    # finally, insert the actual cards
    populate_cards(cards, sql_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python3 csv2sql <set_code>")
    elif len(sys.argv[1]) != 3:
        print("must provide a set_code with 3 letters")
    elif exists(sys.argv[1].upper() + ".sql"):
        print("output file exists, this program will never overwrite!")
    else:
        set_code = sys.argv[1].upper()
        main(set_code)
    # assume git file tree
    # take set code as argument
    # check if csv exists
    # start parsing
