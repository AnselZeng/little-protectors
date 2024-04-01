ROUNDS = [
    [{ # ROUND 1 
        "rg": 2,
        "bg": 0,
        "yg": 0,
        "pg": 0,
        "tg": 0
    },{
        "rg": 1,
        "bg": 0,
        "yg": 0,
        "pg": 0,
        "tg": 0
    }],
    [{ # ROUND 2
        "rg": 2,
        "bg": 1,
        "yg": 0,
        "pg": 0,
        "tg": 0
    },{
        "rg": 1,
        "bg": 2,
        "yg": 0,
        "pg": 0,
        "tg": 0
    }],
    [{ # ROUND 3
        "rg": 2,
        "bg": 0,
        "yg": 2,
        "pg": 0,
        "tg": 0
    },{
        "rg": 0,
        "bg": 1,
        "yg": 1,
        "pg": 0,
        "tg": 0
    }],
    [{ # ROUND 4
        "rg": 0,
        "bg": 0,
        "yg": 0,
        "pg": 0,
        "tg": 3
    },{
        "rg": 0,
        "bg": 2,
        "yg": 0,
        "pg": 0,
        "tg": 0
    }],
]

ENEMY_DATA = {
    "rg": {
        "hp": 5,
        "speed": 1,
        "gold": 10
    },
    "bg": {
        "hp": 8,
        "speed": 1,
        "gold": 20
    },
    "yg": {
        "hp": 8,
        "speed": 1.25,
        "gold": 30
    },
    "pg": {
        "hp": 10,
        "speed": 1,
        "gold": 25
    },
    "tg": {
        "hp": 5,
        "speed": 2,
        "gold": 30
    }
}

TOWER_DATA = {
    "archer": {
        "damage": 2,
        "range": 4,
        "cooldown": 500,
        "cost": 10,
        "animation_steps": 8,
    },
    "knight": {
        "damage": 1.5,
        "range": 2,
        "cooldown": 200,
        "cost": 20,
        "animation_steps": 6,
    },
    "fighter": {
        "damage": 3,
        "range": 3,
        "cooldown": 300,
        "cost": 30,
        "animation_steps": 6
    }
}