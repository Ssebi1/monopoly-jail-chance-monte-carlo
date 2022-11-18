import random

#    tabla monopoly
#    0 0 1 0 0 0 0 0 0 0 3
#    0                   0
#    0                   0
#    2                   2
#    0                   0
#    0                   0
#    0                   1
#    0                   0
#    0                   0
#    0                   0
#    0 0 0 1 0 0 0 0 2 0 0
#
#    where,
#    0 = neutral space
#    1 = chance
#    2 = community chest
#    3 = go to jail

table = [0, 2, 0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
         0, 1, 0, 0, 0, 0, 0, 0, 0, 3,
         0, 0, 2, 0, 0, 1, 0, 0, 0, 0]


def game_settings(file_name):
    f = open(file_name, "r")
    game_end = "jail"
    board_travels = 0
    dice_rolls = 0
    games_number = 10
    for line in f:
        if "game_end" in line:
            game_end = line.strip().split("=")[-1]
            if game_end not in ["jail", "no-jail"]:
                game_end = "jail"
        elif "board_travels" in line:
            try:
                board_travels = int(line.strip().split("=")[-1])
            except:
                board_travels = 0
            if board_travels < 0:
                board_travels = 0
        elif "dice_rolls" in line:
            try:
                dice_rolls = int(line.strip().split("=")[-1])
            except:
                dice_rolls = 0
            if dice_rolls < 0:
                dice_rolls = 0
        elif "games_number" in line:
            try:
                games_number = int(line.strip().split("=")[-1])
            except:
                games_number = 10
            if games_number <= 0:
                games_number = 10
    return game_end, board_travels, dice_rolls, games_number


def init_cards():
    community_cards = [('neutral', 0) for _ in range(14)]
    community_cards += [('tp.advance-to-go', 39), ('tp.go-to-jail', 29)]
    random.shuffle(community_cards)

    chance_cards = [('neutral', 0) for _ in range(7)]
    chance_cards += [('tp.advance-to-boardwalk', 38), ('tp.advance-to-go', 39), ('tp.advance-to-illinois', 23),
                     ('tp.advance-to-st-charles', 10),
                     ('move.go-back-3-spaces', 3), ('tp.go-to-jail', 29)]
    random.shuffle(chance_cards)

    return community_cards, chance_cards


def roll_dices():
    return random.randrange(1, 7, 1), random.randrange(1, 7, 1)


def game(community_cards, chance_cards, game_end, board_travels, dice_rolls):
    position = 39
    jail_number = 0
    board_travels_count = 0
    dice_rolls_count = 0
    consecutive_doubles_count = 0
    max_dice_rolls_count = 200
    chance_card_index = 0
    community_card_index = 0
    string_log = ""

    while True:
        dice1, dice2 = roll_dices()
        old_position = position
        if dice1 == dice2:
            consecutive_doubles_count += 1
            if consecutive_doubles_count == 3:
                consecutive_doubles_count = 0
                position = 29
        else:
            dice = dice1 + dice2
            dice_rolls_count += 1
            position = (position + dice) % 40

        if table[position] == 1:
            chance_card = chance_cards[chance_card_index]
            chance_card_index += 1
            if chance_card_index == len(chance_cards):
                random.shuffle(chance_cards)
                chance_card_index = 0

            if "tp" in chance_card[0]:
                position = chance_card[1]
            elif "move" in chance_card[0]:
                position = position - chance_card[1]
        elif table[position] == 2:
            community_card = community_cards[community_card_index]
            community_card_index += 1
            if community_card_index == len(community_cards):
                random.shuffle(community_cards)
                community_card_index = 0

            if "tp" in community_card[0]:
                position = community_card[1]

        if table[position] == 3:
            position = 9
            jail_number += 1

            string_log += " | " + "dice: " + "(" + str(dice1) + "," + str(dice2) + ") position: jail"
            if game_end == "jail":
                return jail_number, string_log

        if old_position > position and 0 <= position < 8 and old_position > 30:
            board_travels_count += 1
            if board_travels != 0 and board_travels_count > board_travels:
                string_log += " | " + "dice: " + "(" + str(dice1) + "," + str(dice2) + ") position: " + str(position)
                return jail_number, string_log

        if dice_rolls != 0 and dice_rolls_count >= dice_rolls:
            string_log += " | " + "dice: " + "(" + str(dice1) + "," + str(dice2) + ") position: " + str(position)
            return jail_number, string_log
        if dice_rolls >= max_dice_rolls_count:
            string_log += " | " + "dice: " + "(" + str(dice1) + "," + str(dice2) + ") position: " + str(position)
            return jail_number, string_log
        string_log += " | " + "dice: " + "(" + str(dice1) + "," + str(dice2) + ") position: " + str(position)


def monte_carlo(games_number, community_cards, chance_cards, game_end, board_travels, dice_rolls):
    S = 0
    string_log_monte_carlo = ""
    for i in range(games_number):
        jail_count, string_log = game(community_cards, chance_cards, game_end, board_travels, dice_rolls)
        S += jail_count
        string_log_monte_carlo += string_log + '\n'
    f = open("monopoly.log", "w")
    f.write(string_log_monte_carlo)
    f.close()
    return float(S / games_number)


if __name__ == '__main__':
    community_cards, chance_cards = init_cards()
    game_end, board_travels, dice_rolls, games_number = game_settings("monopoly.conf")
    print(monte_carlo(games_number, community_cards, chance_cards, game_end, board_travels, dice_rolls))
