
# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

# Variable keeping count of enemy stances
enemyStances = [0, 0, 0]

# Keep count of enemy stances
def updateEnemyStances():
    opp = game.get_opponent()
    if opp.location == game.get_self().location:
        stance = opp.stance
        if stance == "Rock":
            enemyStances[0] += 1
        elif stance == "Paper":
            enemyStances[1] += 1
        elif stance == "Scissors":
            enemyStances[2] += 1

# Check if monster will be arrive by the time we arrive
def shouldAttack(monster):
    if not monster.dead:
        return True
    turnsToRespawn = monster.respawn_counter
    totalTurnsToMove = get_distance(me.location, monster.location, me.speed)
    return totalTurnsToMove  >= turnsToRespawn

# Find the attack stat which is lowest
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

# Find the monster who would increase lowest attack stat
def get_monster_node_for_attack_balance():
    lowest_attack = get_lowest_attack()
    node = 0
    highest = -1000
    for monster in game.get_all_monsters():
        if (lowest_attack == "rock"):
            if (monster.death_effects.rock > highest and shouldAttack(monster)):
                highest = monster.death_effects.rock
                node = monster.location
        elif (lowest_attack == "paper" and shouldAttack(monster)):
            if (monster.death_effects.paper > highest):
                highest = monster.death_effects.paper
                node = monster.location
        else:
            if (monster.death_effects.scissors > highest and shouldAttack(monster)):
                highest = monster.death_effects.scissors
                node = monster.location
    return node

# Find the path that would increase the lowest attack stat
def get_best_path_for_attack_balance():
    highest_total = -1000
    best_path = []
    for path in game.shortest_paths(game.get_self().location, get_monster_node_for_attack_balance()):
        total = 0
        for node in path:
            lowest_attack = get_lowest_attack()
            if (not game.has_monster(node)):
                continue
            weight = 1
            if (shouldAttack(game.get_monster(node))):
                weight = 2
            if (lowest_attack == "rock"):
                total += weight*game.get_monster(node).death_effects.rock
            elif (lowest_attack == "paper"):
                total += weight*game.get_monster(node).death_effects.paper
            else:
                total += weight*game.get_monster(node).death_effects.scissors
        if total > highest_total:
            highest_total = total
            best_path = path
    return best_path

# Return stance that would win
def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

# Find number of turns to travel between 2 nodes
def get_distance(start, end, speed):
    path = game.shortest_paths(start, end)
    return len(path[0])*(7-speed)

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
    enemy = game.get_opponent()

    enemy_distance = min(get_distance(me.location, enemy.location, me.speed), get_distance(me.location, enemy.location, enemy.speed))

    # Check if we have moved this turn
    if me.location == me.destination:
        # Get the path to the monster that will best balance our attack
        paths = get_best_path_for_attack_balance()
        destination_node = paths[0]

    else:
        destination_node = me.destination

    

    # Logic for choosing stance
    if enemy.location == me.location:
        if enemyStances[0] > enemyStances[1] and enemyStances[0] > enemyStances[2]:
            chosen_stance = "Paper"
        elif enemyStances[1] > enemyStances[2] and enemyStances[1] > enemyStances[0]:
            chosen_stance = "Scissors"
        else:
            chosen_stance = "Rock"

    elif game.has_monster(me.location) and not game.get_monster(me.location).dead:
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
        game.log(str(chosen_stance))

    #elif game.has_monster(destination_node):
    #    chosen_stance = get_winning_stance(game.get_monster(destination_node).stance)

    # Keep track of enemy moves
    updateEnemyStances();

    # submit your decision for the turn 
    game.submit_decision(destination_node, chosen_stance)
