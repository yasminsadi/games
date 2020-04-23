tileSize = 16
jump_height = 160
time_to_jump_apex = 0.5
gravity = -(2.0 * jump_height) / (time_to_jump_apex * time_to_jump_apex)
jump_velocity = abs(gravity) * time_to_jump_apex
warp_func = None
state = 0
lives = 3
energy = 2
full_energy = 2
invincibility = False
stateInfo = [
    'mario',
    'supermario'
]

class flags:
    player = 1
    platform = 2
    foe = 4
    player_attack = 8
    foe_attack = 16
    platform_passthrough = 32

class tags:
    player = 1
    player_attack = 2
    foe = 3
    foe_attack = 4