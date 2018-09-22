# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

def get_lowest_attack():
    lowest_attack = "rock"
    lowest_damage = game.get_self().rock;
    if (game.get_self().paper < lowest_damage):
        lowest_damage = game.get_self().paper
        lowest_attack = "paper"
    if (game.get_self().scissors < lowest_damage):
        lowest_damage = game.get_self().scissors
        lowest_attack = "scissors"
    return lowest_attack

def get_monster_node_for_attack_balance():
    lowest_attack = get_lowest_attack()
    node = 0
    highest = -1000
    for monster in game.get_all_monsters():
        if (lowest_attack == "rock"):
            if (monster.death_effects.rock > highest):
                highest = monster.death_effects.rock
                node = monster.location
        elif (lowest_attack == "paper"):
            if (monster.death_effects.paper > highest):
                highest = monster.death_effects.paper
                node = monster.location
        else:
            if (monster.death_effects.scissors > highest):
                highest = monster.death_effects.scissors
                node = monster.location
    return node

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()

    if me.location == me.destination: # check if we have moved this turn
        # get all living monsters closest to me
        monsters = game.nearest_monsters(me.location, 1)

        # choose a monster to move to at random
        monster_to_move_to = monsters[random.randint(0, len(monsters)-1)]

        # get the set of shortest paths to that monster
        paths = game.shortest_paths(me.location, monster_to_move_to.location)
        destination_node = paths[random.randint(0, len(paths)-1)][0]

    else:
        destination_node = me.destination

    if game.has_monster(me.location):
        # if there's a monster at my location, choose the stance that damages that monster
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    else:
        # otherwise, pick a random stance
        chosen_stance = stances[random.randint(0, 2)]

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)
