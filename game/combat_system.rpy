# ============================================================
# COMBAT SYSTEM - Treasure of the Hideous One
# D&D-informed tactical combat for visual novel
# ============================================================

init python:
    import random
    
    # --- ENEMY DEFINITIONS ---
    # Based on D&D Expert Set stats, adapted for VN combat
    
    ENEMIES = {
        "hydra": {
            "name": "Hydra",
            "display_name": "the hydra",
            "rounds": 3,
            "hits_to_defeat": 3,
            "ac": 5,
            "hd": 10,
            "stance": "aggressive",
            "weaknesses": ["fire"],
            "immunities": [],
            "special": {
                "multi_head": True,
                "drag_threshold": 6,
                "water_hazard": True
            },
            "defeat_text": "The hydra's heads tear into you...",
            "victory_text": "The beast thrashes and sinks beneath the dark water."
        },
        "bandit_chieftain": {
            "name": "Elven Bandit Chieftain",
            "display_name": "the bandit chieftain",
            "rounds": 2,
            "hits_to_defeat": 2,
            "ac": 1,
            "hd": 7,
            "stance": "commander",
            "weaknesses": [],
            "immunities": ["fire"],
            "special": {
                "minions": 35,
                "spells": True,
                "fire_hazard": True
            },
            "defeat_text": "The chieftain's flaming sword descends...",
            "victory_text": "The bandits scatter into the grass."
        },
        "ghouls": {
            "name": "Ghoul Horde",
            "display_name": "the ghoul horde",
            "rounds": 3,
            "hits_to_defeat": 2,
            "ac": 6,
            "hd": 2,
            "stance": "swarm",
            "weaknesses": ["fire", "light"],
            "immunities": [],
            "special": {
                "paralysis": True,
                "overwhelm": 15,
                "water_climb": True
            },
            "defeat_text": "Paralyzed and dragged underwater...",
            "victory_text": "The ghouls scatter back into the dark water."
        },
        "rosentos": {
            "name": "Rosentos the Vampire",
            "display_name": "Rosentos",
            "rounds": 5,
            "hits_to_defeat": 4,
            "ac": 2,
            "hd": 8,
            "stance": "predator",
            "weaknesses": ["holy", "stake", "sunlight", "grave_earth"],
            "immunities": ["normal_wounds"],
            "special": {
                "charm_gaze": True,
                "regeneration": True,
                "transform": True,
                "level_drain": True
            },
            "defeat_text": "His gaze catches yours. You cannot look away...",
            "victory_text": "Rosentos crumbles to ash."
        },
        "caymen": {
            "name": "Cay-Men Village",
            "display_name": "the cay-men",
            "rounds": 2,
            "hits_to_defeat": 2,
            "ac": 7,
            "hd": 2,
            "stance": "defensive",
            "weaknesses": [],
            "immunities": [],
            "special": {
                "swarm": True,
                "ranged": True,
                "negotiate": True
            },
            "defeat_text": "The cay-men overwhelm you...",
            "victory_text": "The cay-men scatter from the walls."
        }
    }
    
    # --- STANCE MODIFIERS ---
    STANCE_EFFECTS = {
        "holding": {"modifier": 0, "text": "You hold your ground."},
        "reeling": {"modifier": -1, "text": "You are pressed back, bleeding."},
        "desperate": {"modifier": -2, "text": "This is your last stand."}
    }
    
    # --- COMPANION BONUSES ---
    COMPANION_BONUSES = {
        "carmelita": {
            "vs_human": {"attack": 1, "desc": "Carmelita knows how soldiers fight."},
            "vs_rosentos_defend": {"defend": 1, "desc": "Carmelita warns you about his gaze."},
            "opening": {"bonus": 2, "desc": "Carmelita creates a distraction, giving you a clear strike.", "once": True}
        },
        "thut": {
            "vs_swamp": {"attack": 1, "desc": "Thut knows these creatures."},
            "vs_rosentos_attack": {"attack": 1, "desc": "Thut identifies the weak points."},
            "insight": {"effect": "reveal_weakness", "desc": "Thut studies the enemy. 'The central neck—it doesn't weave.'", "once": True}
        }
    }
    
    # --- PASSIVE ITEM EFFECTS ---
    PASSIVE_ITEMS = {
        "Flaming Sword +1": {
            "attack": 1,
            "vs_hydra": 2,
            "desc": "Fire erupts along your blade."
        },
        "Sword +3: Armory of Morphos": {
            "attack": 3,
            "desc": "The sword pulses with power."
        },
        "Ring of Regeneration": {
            "stance_recover": True,
            "desc": "The ring glows warmly. Your wounds begin to close."
        },
        "Ring of Fire Resistance": {
            "fire_immune": True,
            "desc": "The ring protects you from flame."
        }
    }
    
    # --- UTILITY FUNCTIONS ---
    
    def get_combat_stance(current_stance):
        """Return stance effects dict"""
        return STANCE_EFFECTS.get(current_stance, STANCE_EFFECTS["holding"])
    
    def get_enemy(enemy_key):
        """Return enemy data dict"""
        return ENEMIES.get(enemy_key)
    
    def has_weakness(enemy_key, weakness_type):
        """Check if enemy has a specific weakness"""
        enemy = ENEMIES.get(enemy_key, {})
        return weakness_type in enemy.get("weaknesses", [])
    
    def has_immunity(enemy_key, immunity_type):
        """Check if enemy has a specific immunity"""
        enemy = ENEMIES.get(enemy_key, {})
        return immunity_type in enemy.get("immunities", [])
    
    def get_item_combat_bonus(item_name, enemy_key=None):
        """Get combat bonus from an item"""
        if item_name not in PASSIVE_ITEMS:
            return 0
        
        item = PASSIVE_ITEMS[item_name]
        bonus = item.get("attack", 0)
        
        # Check enemy-specific bonuses
        if enemy_key and enemy_key == "hydra":
            bonus += item.get("vs_hydra", 0)
        
        return bonus
    
    def get_companion_bonus(companion_name, enemy_key, action_type):
        """Get passive companion bonus"""
        if companion_name not in COMPANION_BONUSES:
            return 0
        
        companion = COMPANION_BONUSES[companion_name]
        
        # Check for specific enemy bonuses
        if enemy_key == "rosentos" and action_type == "defend":
            key = "vs_rosentos_defend"
            if key in companion:
                return companion[key].get("defend", 0)
        
        if enemy_key == "rosentos" and action_type == "attack":
            key = "vs_rosentos_attack"
            if key in companion:
                return companion[key].get("attack", 0)
        
        if enemy_key in ["hydra", "ghouls"] and action_type == "attack":
            key = "vs_swamp"
            if key in companion:
                return companion[key].get("attack", 0)
        
        if enemy_key == "bandit_chieftain" and action_type == "attack":
            key = "vs_human"
            if key in companion:
                return companion[key].get("attack", 0)
        
        return 0
    
    def can_use_companion_special(companion_name, used_list):
        """Check if companion special can be used"""
        if companion_name not in COMPANION_BONUSES:
            return False
        
        companion = COMPANION_BONUSES[companion_name]
        for key in ["opening", "insight"]:
            if key in companion:
                return key not in used_list
        return False
    
    def get_companion_special(companion_name):
        """Get companion special ability info"""
        if companion_name not in COMPANION_BONUSES:
            return None
        
        companion = COMPANION_BONUSES[companion_name]
        for key in ["opening", "insight"]:
            if key in companion:
                return {"name": key, **companion[key]}
        return None

# --- ROLL D20 FUNCTION ---
init python:
    def roll_d20(bonus=0):
        """Roll a d20 and return (raw, total, outcome)"""
        raw = random.randint(1, 20)
        total = max(1, min(20, raw + bonus))
        
        if raw == 20:
            outcome = "critical_success"
        elif raw == 1:
            outcome = "critical_blunder"
        elif total >= 13:
            outcome = "success"
        elif total >= 6:
            outcome = "partial"
        else:
            outcome = "failure"
        
        return (raw, total, outcome)

# --- STATE TRACKING ---
default combat_bonus_final = 0
default combat_round = 1
default combat_hits = 0
default combat_stance = "holding"
default combat_specials_used = []
default combat_stance_recover_used = False

# --- ENEMY-SPECIFIC STATE ---
default hydra_heads = 10
default hydra_round = 1
default hydra_hits = 0
default hydra_stance = "holding"
default hydra_specials_used = []
default hydra_stance_recover_used = False
default hydra_hungry = False
default hydra_weakness = False
default hydra_thut_insight = False
default hydra_defensive = False
default hydra_closecall = False

default bandit_round = 1
default bandit_hits = 0
default bandit_stance = "holding"
default bandit_specials_used = []
default bandit_fire_rounds = 0
default bandit_surrounded = False
default bandit_bonus = 0
default bandit_thut_insight = False
default bandit_defensive = False
default bandit_chief_killed = False
default bandit_closecall = False

default ghoul_round = 1
default ghoul_hits = 0
default ghoul_stance = "holding"
default ghoul_paralyzed = False
default ghoul_specials_used = []
default ghoul_thut_insight = False
default ghoul_fire = False
default ghoul_closecall = False

default rosentos_round = 1
default rosentos_hits = 0
default rosentos_stance = "holding"
default rosentos_specials_used = []
default rosentos_grave_earth_scattered = False
default rosentos_charm_saved = False
default rosentos_dawn_timer = 0
default rosentos_bonus = 0
default rosentos_charm_bonus = False
default rosentos_thut_insight = False
default rosentos_defensive = False
default rosentos_charmed = False
default rosentos_closecall = False

# --- GAME STATE FLAGS (from main game) ---
default grisbaldos_oath_taken = False
default grisbaldos_cursed = False
default grisbaldos_contradiction_known = False
default slave_farm_witnessed = False
default slough_debuffed = False
default slough_vision_seen = False
default rosentos_betrayed_known = False