# ============================================================
# GAME OVER SCREENS - Treasure of the Hideous One
# Defeat scenarios and restart options
# ============================================================

# --- HYDRA DEFEAT ---
label game_over_hydra:
    hide char_hydra with dissolve
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The hydra's heads tear into you. Blood fills the water."
    narrator "Your companions cannot reach you in time."
    narrator "The last thing you see is the riverbank slipping away as darkness closes in."
    
    jump game_over_screen

label game_over_hydra_drown:
    hide char_hydra with dissolve
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "Six heads coil around your limbs. You are dragged beneath the surface."
    narrator "The water is cold and dark. You struggle, but the grip is iron."
    narrator "Your lungs burn. Then... nothing."
    
    jump game_over_screen

# --- BANDIT DEFEAT ---
label game_over_bandits:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The chieftain's flaming sword descends in a terrible arc."
    narrator "Your vision goes dark."
    narrator "You wake stripped of your equipment, robbed, left for dead on the plain."
    narrator "Luln will never know what happened to their expedition."
    
    jump game_over_screen

label game_over_bandits_robbed:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The bandits surround you. The chieftain laughs."
    narrator "They take everything—your weapons, your coin, your maps."
    narrator "Left bleeding in the grass, you watch them ride away."
    narrator "The expedition is over."
    
    jump game_over_screen

# --- GHOUL DEFEAT ---
label game_over_ghouls:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "Paralysis spreads through your limbs like ice water."
    narrator "You cannot move. You cannot scream."
    narrator "The ghouls drag you beneath the black water. The last thing you see is the moonlight fading above."
    narrator "When you wake—if you can call it waking—you will not remember this."
    narrator "You will serve."
    
    jump game_over_screen

label game_over_ghouls_paralyzed:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The ghoul's claws rake your arm. Cold numbness spreads from the wound."
    narrator "You cannot move. Your companions try to carry you, but there are too many."
    narrator "They are forced to flee. You are left behind."
    narrator "The ghouls descend."
    
    jump game_over_screen

# --- ROSENTOS DEFEAT ---
label game_over_rosentos:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "His gaze catches yours. The world softens."
    narrator "You cannot look away. You do not want to."
    narrator "He speaks, and his voice is the only thing that matters."
    narrator "\"You will stay,\" he says. \"You will be happy here. Forever.\""
    narrator "He does not kill you. That would be wasteful."
    narrator "When he is finished, you will lead others to him. You will smile."
    narrator "You will be happy."
    narrator "Forever."
    
    jump game_over_screen

label game_over_rosentos_charmed:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "His eyes hold yours. The red glow is warm, welcoming."
    narrator "A voice in your head tells you to fight, but it grows distant."
    narrator "Why would you fight? He only wants to help."
    narrator "He only wants you to stay."
    narrator "Your companions call your name, but they sound so far away."
    narrator "They do not understand. You understand."
    narrator "You will stay."
    
    jump game_over_screen

label game_over_rosentos_slave:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The last thing you remember is his smile."
    narrator "Then there is only service. Only hunger."
    narrator "You lead others to him. You smile as you do it."
    narrator "Sometimes, in the brief moments between, you remember a tavern."
    narrator "A soldier telling a story. Friends around a fire."
    narrator "But the memory fades. It always fades."
    
    jump game_over_screen

# --- CAY-MEN DEFEAT ---
label game_over_caymen:
    $ renpy.hide_screen('inventory_screen')
    stop music fadeout 1.0
    
    narrator "The tiny javelins find every gap in your armor."
    narrator "Twenty, then thirty, then more cay-men swarm from their mounds."
    narrator "You fall beneath a wave of scales and feathers."
    narrator "The last thing you see is the shaman watching from the wall, unmoved."
    
    jump game_over_screen

# --- GENERAL GAME OVER SCREEN ---
label game_over_screen:
    scene black with fade
    
    narrator "THE END"
    
    menu:
        "Try Again (Restart from beginning)":
            $ renpy.full_restart()
        "Main Menu":
            $ renpy.full_restart()
        "Quit":
            $ renpy.quit()

# --- ALTERNATIVE: CONTINUE WITH CONSEQUENCES ---
# For defeats that don't end the game but have costs

label combat_defeat_robbed:
    narrator "The bandits leave you alive, but take everything."
    narrator "You stumble back toward Luln, empty-handed."
    narrator "The expedition is over."
    $ renpy.full_restart()

label combat_defeat_wounded:
    narrator "You survive, barely. The wound will slow you."
    $ combat_stance = "reeling"
    # Continue with penalty
    return

label combat_defeat_retreat:
    narrator "You flee. There is no shame in living to fight another day."
    narrator "But the enemy holds the path forward."
    # Offer alternate route or retreat
    return