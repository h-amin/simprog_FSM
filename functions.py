import math

CMB_RANGE = 2  # Combat range in meters
EVAL_RANGE = 5  # Evaluation range in meters
MAX_IDLE = 60  # Maximum idle distance in meters
LOS_RANGE = 15  # Line of Sight range in meters
THREE_SEC_INTERVAL = 3
player_list = []


# Function to define the coordinates of said player/mob.
def calc_distance(pos1, pos2):
    dx = (pos1[0] - pos2[0]) ** 2
    dy = (pos1[1] - pos2[1]) ** 2
    distance = math.sqrt(dx + dy)
    return int(distance)


# First state: IDLE, function that transitions the idle state towards player_approach or walk depending on the
# calculated distance between mob and player.
def idle_transitions(mob, player):
    mob.current_state = "IDLE"
    mob.summary(player)
    if player_in_range(mob, player.position):
        return player_approach_transitions(mob, player)
    if mob.clock.current_time - mob.start_idle_time < MAX_IDLE:
        return "IDLE"
    else:
        return walk_transitions(mob, player)


# Function that checks if the mob and player are within 15-meter distance.
def player_in_range(mob, player_pos):
    if calc_distance(mob.position, player_pos) < LOS_RANGE:
        return True
    else:
        return False


# Function state COMBAT, that will transition the current combat state to either a VICTORY or DEFEAT state.
def combat_transitions(mob, player):
    mob.current_state = "COMBAT"
    mob.summary(player)
    if mob.lvl > player.lvl:
        mob.victory_time = mob.clock.current_time
        print("player got killed")
        player.respawn(mob)
        return victory_transitions(mob, player)
    else:
        mob.hp = 0
        return defeat_transitions(mob, player)


# Function that transitions from the WALK state towards the player_approach state or staying within the WALK state.
def walk_transitions(mob, player):
    mob.current_state = "WALK"
    mob.summary(player)
    if player in player_list:
        # no time to make a nice walking route, so currently it moves 1 to the right
        mob.position = [mob.position[0] + 1, 0]
        return "WALK"
    elif calc_distance(mob.position, player.position) <= 15:
        return player_approach_transitions(mob, player)
    else:
        return "WALK"


# Respawn function that will restore the mob hit points and revert into the IDLE state and x0, y0 coordinates.
def respawn_transitions(mob, player):
    mob.current_state = "RESPAWN"
    mob.summary(player)
    mob.hp = 100
    mob.position = [0, 0]
    return idle_transitions(mob, player)


# DEFEAT state function that will transition the current state into a RESPAWN state.
def defeat_transitions(mob, player):
    mob.current_state = "DEFEAT"
    mob.summary(player)
    return respawn_transitions(mob, player)


# REGEN state function that will transition the current state into a BoT state.
def regen_transitions(mob, player):
    mob.current_state = "REGEN"
    mob.summary(player)
    return bot_transitions(mob, player)


# VICTORY state function that will transition the current state into the REGEN state if the 3 second interval condition
# has been met, if this isn't the case, repeat VICTORY state.
def victory_transitions(mob, player):
    mob.current_state = "VICTORY"
    mob.summary(player)
    if mob.clock.current_time - mob.victory_time >= THREE_SEC_INTERVAL:
        return regen_transitions(mob, player)
    else:
        return "VICTORY"


# AGGRO state function that will transition the current state into COMBAT state if the below 3 meters condition has
# been met, if this isn't the case, repeat AGGRO state.
def aggro_transitions(mob, player):
    mob.current_state = "AGGRO"
    mob.summary(player)
    if calc_distance(mob.position, player.position) <= CMB_RANGE:
        return combat_transitions(mob, player)
    else:
        move_towards_player(mob, player)
        return "AGGRO"


# EVALUATION state function, compares the mob level with the player level. If the mob level exceeds the player, enter
# COMBAT state, if not return BoT state.
def eval_transitions(mob, player):
    mob.current_state = "EVAL"
    mob.summary(player)
    if mob.lvl > player.lvl:
        return aggro_transitions(mob, player)
    else:
        player_list.append(player)
        return walk_transitions(mob, player)


# BoT (Back on Track) state function that will transition the current state into the WALK state.
def bot_transitions(mob, player):
    mob.current_state = "BOT"
    mob.summary(player)
    return walk_transitions(mob, player)


# PLAYER_APPROACH state function that calculates the distance between mob position and player position. If the delta
# distance between mob and player <= 5 meters, enter EVAL state, if the delta distance is bigger than 15 m enter BoT
# (Back on Track) state. Should the mentioned conditions not be met, return the move_towards_player function.
def player_approach_transitions(mob, player):
    mob.current_state = "PLAYER_APPROACH"
    mob.summary(player)
    distance = calc_distance(mob.position, player.position)
    if distance > LOS_RANGE:
        return bot_transitions(mob, player)
    elif distance <= EVAL_RANGE:
        return eval_transitions(mob, player)
    else:
        move_towards_player(mob, player)

    # Secondary statement that will immediately evaluate the player if the distance between mob and player is equal or
    # below 5 meters, in case of player movement that will interrupt the evaluation process.
    new_distance = calc_distance(mob.position, player.position)
    if new_distance <= EVAL_RANGE:
        return eval_transitions(mob, player)
    else:
        return "PLAYER_APPROACH"


# Function that uses the calculated distance between mob and player in order to close the distance between these two
# classes. The x and y coordinates of both mob and player will be subtracted of each other. The result is a float that
# will multiply itself by 0.9 (a value that represents the 'lower' speed compared to the 1.0 of the player.) and then
# add itself to the current X and Y coordinate values.
def move_towards_player(mob, player):
    distance = calc_distance(mob.position, player.position)
    dx, dy = (player.position[0] - mob.position[0], player.position[1] - mob.position[1])
    # unit vector of the directional vector
    udx, udy = (dx / distance, dy / distance)
    mob.position[0] = mob.position[0] + 0.9 * udx
    mob.position[1] = mob.position[1] + 0.9 * udy


# Simulation function that acts as the start function for the whole process.
def simulate(mob, player):
    state_transition = mob.states_transitions[mob.current_state]
    while True:
        player.turn(mob)
        mob.current_state = state_transition(mob, player)
        state_transition = mob.states_transitions[mob.current_state]
        if mob.clock.current_time == 100:
            print("times up!")
            break
