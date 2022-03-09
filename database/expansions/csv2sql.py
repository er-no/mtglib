from os.path import exists
import sys

# open csv
# read csv line by line
# for every line
# create sql insert statement

# supports standard format
codes_to_expansion_info = {
    'ZNR' : ['\"Zendikar Rising\"', 391],
    'KHM' : ['\"Kaldheim\"', 405],
    'STX' : ['\"Strixhaven: School of Mages\"', 382],
    'AFR' : ['\"Dungeons & Dragons: Adventures in the Forgotten Realms\"', 402],
    'MID' : ['\"Innistrad: Midnight Hunt\"', 391],
    'VOW' : ['\"Innistrad: Crimson Vow\"', 412],
    'NEO' : ['\"Kamigawa: Neon Dynasty\"', 512]
}

rarity_to_int = {
    'C' : '0',
    'U' : '1',
    'R' : '2',
    'M' : '3'
}

def main(set_code):
    if set_code not in codes_to_expansion_info:
        print("ERROR: UNKNOWN_SET [" + set_code + "]")
        exit(1)

    if not exists("../data/" + set_code + ".csv"):
        print("ERROR: UNKNOWN_FILE [../data/" + set_code + ".csv]")
        exit(1)

    # insert the set into the expansions table
    set_info = codes_to_expansion_info.get(set_code)
    sql_file = open(set_code + ".sql", "w")
    sql_file.write("-- create the set\n")
    sql_file.write("INSERT INTO expansions (expansion_id, expansion_name, max_count)\n")
    sql_file.write("VALUES (\"" + set_code + "\", " + set_info[0] + ", " + str(set_info[1]) + ");\n\n")

    # lets read the csv file
    csv_file = open("../data/" + set_code + ".csv", "r")
    csv_raw = csv_file.read()
    cards = csv_raw.splitlines()

    # find all unique mana costs, lands exists 100%
    manas = {"[L]"}
    for card in cards:
        mana = card.split(";")[3]
        if mana != "" and mana != "cost" and mana not in manas:
            manas.add(mana)

    # now we can insert the unique values (reducing number of values passed to DB)
    sql_file.write("-- populate mana table\n")
    sql_file.write("INSERT OR IGNORE INTO mana_costs (cost) VALUES\n")
    width = 0
    for mana in manas:
        s = ", (\"" + mana + "\")"
        if width == 0:
            s = s[2:len(s)] # if first in line, skip comma
        sql_file.write(s)
        width += len(s)
        if width >= 50:
            sql_file.write(",\n")
            width = 0

    sql_file.write(";\n\n-- populate with card data\n")
    sql_file.write("INSERT INTO cards (expansion_code, card_number, card_name, mana_id, rarity) VALUES\n")
    for card in cards:
        if card[0] != "s": # this is header row
            card = card.split(";")
            expansion_code = card[0]
            card_number = card[1]
            card_name = card[2]
            mana_cost = card[3] if card[3] != "" else "[L]"
            card_rarity = card[4]
            sql_file.write(
                "(\"" + expansion_code +
                "\", " + card_number +
                ", \"" + card_name +
                "\", (SELECT mana_id FROM mana_costs WHERE cost = \"" + mana_cost + "\")" +
                ", " + rarity_to_int.get(card_rarity) + ")")
            if int(card_number) == codes_to_expansion_info.get(set_code)[1]: # if it is the last card
                sql_file.write(";\n")
            else: # its not the last card
                sql_file.write(",\n")



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
