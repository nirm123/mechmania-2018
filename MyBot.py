# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

enemyStance = ""
counter = 0

# Check if monster will be arrive by the time we arrive
def shouldAttack(monster, shift):
    if not monster.dead:
        return True
    turnsToRespawn = monster.respawn_counter - shift
    totalTurnsToMove = get_distance(me.location, monster.location, me.speed)
    return totalTurnsToMove  >= turnsToRespawn

# Find the attack stat which is lowest
def get_lowest_attack():
    me = game.get_self()
    lowest_attack = "rock"
    lowest_damage = me.rock;
    if (me.paper < lowest_damage):
        lowest_damage = me.paper
        lowest_attack = "paper"
    if (me.scissors < lowest_damage):
        lowest_damage = me.scissors
        lowest_attack = "scissors"
    if (me.speed < 2):
        lowest_attack = "speed"
    return lowest_attack

# Find the monster who would increase lowest attack stat
def get_monster_node_for_attack_balance():
    lowest_attack = get_lowest_attack()
    node = 0
    highest = -1000
    max_distance = 0
    if me.health < 60:
        max_distance = 1;
    elif me.health < 100:
        max_distance = 2
    else:
        max_distance = 3
    for monster in game.get_all_monsters():
        paths = game.shortest_paths(me.location, monster.location)
        if (len(paths[0]) <= max_distance):
            if (lowest_attack == "rock"):
                if (monster.death_effects.rock > highest and shouldAttack(monster, 0)):
                    highest = monster.death_effects.rock
                    node = monster.location
            elif (lowest_attack == "paper" and shouldAttack(monster, 0)):
                if (monster.death_effects.paper > highest):
                    highest = monster.death_effects.paper
                    node = monster.location
            elif (lowest_attack == "scissors" and shouldAttack(monster, 0)):
                if (monster.death_effects.scissors > highest and shouldAttack(monster, 0)):
                    highest = monster.death_effects.scissors
                    node = monster.location
            else:
                node = 3
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
            weight = 0
            if (shouldAttack(game.get_monster(node), 0)):
                weight = 1
            if (lowest_attack == "rock" and game.get_monster(node).attack < 4):
                total += weight*game.get_monster(node).death_effects.rock-(game.get_monster(node).attack)**4
            elif (lowest_attack == "paper" and game.get_monster(node).attack < 4):
                total += weight*game.get_monster(node).death_effects.paper-(game.get_monster(node).attack)**4
            else:
                if (game.get_monster(node).attack < 4):
                    total += weight*game.get_monster(node).death_effects.scissors-(game.get_monster(node).attack)**4
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
    game.log(str(me.location))
    enemy_distance = min(get_distance(me.location, enemy.location, me.speed), get_distance(me.location, enemy.location, enemy.speed))
  
    current_stance = me.stance
    current_stance = current_stance.lower()
    attack_current = 0
    if (current_stance == "rock"):
        attack_current = me.rock
    elif current_stance == "paper":
        attack_current = me.paper
    else:
        attack_current = me.scissors

    # If health is less than 20
    if me.health<=20:
        # If my location is node 0
        if me.location == 0: 
            # If monster alive and health/attack < move time 
            if (not game.get_monster(0).dead and (game.get_monster(me.location).health/attack_current) < 7-me.speed):
                paths = get_best_path_for_attack_balance()
                destination_node = paths[0]
            # If monster dead
            else:
                destination_node = me.location
        # If I need to go to 0
        else:
            path = game.shortest_paths(me.location, 0)
            destination_node = path[0][0]

    # If health monster is alive go to 0
    if shouldAttack(game.get_monster(0), 10):
        path = game.shortest_paths(me.location, 0)
        destination_node = path[0][0]

    # Check if we have moved this turn
    elif me.location == me.destination:
        if game.has_monster(me.location):
            if game.get_monster(me.location).dead:
        # Get the path to the monster that will best balance our attack
                paths = get_best_path_for_attack_balance()
                destination_node = paths[0]
            else:
                if ((game.get_monster(me.location).health/attack_current) < 7-me.speed):
                    paths = get_best_path_for_attack_balance()
                    destination_node = paths[0]
                else:
                    destination_node = me.location
        else:
            paths = get_best_path_for_attack_balance()
            destination_node = paths[0]

    else:
        destination_node = me.destination

    if (destination_node == 11):
        destination_node = 0
    
    monster_not_on_location = True
    # Logic for choosing stance
    
    # If in the same location as enemy, randomly choose stance
    if enemy.location == me.location:
        chosen_stance = stances[random.randint(0,2)]
        if enemyStance == enemy.stance:
            counter += 1
            if counter >= 8:
                if enemyStance == "Rock":
                    chosen_stance = "Paper"
                elif enemyStance == "Paper":
                    chosen_stance = "Scissors"
                elif enemyStance == "Scissors":
                    chosen_stance = "Paper"

        else:
            enemyStance = enemy.stance
            counter = 0

    # If in the same location of a monster who is not dead
    elif game.has_monster(me.location) and not game.get_monster(me.location).dead:
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
        monster_not_on_location= False

    # If no monster or person then set next node
    if game.has_monster(destination_node) and monster_not_on_location and (enemy.location != me.location):
        chosen_stance = get_winning_stance(game.get_monster(destination_node).stance)

    # submit your decision for the turn 
    game.submit_decision(destination_node, chosen_stance)
