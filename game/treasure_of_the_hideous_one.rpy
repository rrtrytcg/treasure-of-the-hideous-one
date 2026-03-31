# ============================================================
# THE TREASURE OF THE HIDEOUS ONE
# Based on AC2 by David Cook — D&D Expert Mini-Adventure
# For Character Levels 4–7
# ============================================================

# --- CHARACTER DEFINES ---
define narrator          = Character(None, what_color="#d4cfc8")
define fondalus          = Character("Fondalus the Soldier",      color="#c8a84b")
define grisbaldos_ghost  = Character("Ghost of Grisbaldos",       color="#a0e8a0", what_italic=True)
define possessed         = Character("??? (Possessed Companion)",  color="#a0e8a0", what_italic=True)
define bandit_chief      = Character("Elven Bandit Chieftain",    color="#8b0000")
define korat             = Character("Chief Korat",                color="#cd853f")
define carmelita         = Character("Carmelita",                  color="#dda0dd")
define thut              = Character("Thut",                       color="#8fbc8f")
define rosentos          = Character("Rosentos",                   color="#b0c4de")
define rosentos_vamp     = Character("Rosentos the Vampire",       color="#dc143c", what_italic=True)
define caymen_shaman     = Character("Cay-Men Shaman",             color="#32cd32")

# --- INVENTORY SYSTEM ---
default inventory = []

screen inventory_screen():
    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 20
        background Frame("#1a1a2ecc", 10, 10)
        vbox:
            spacing 4
            text "INVENTORY" size 18 color "#c8a84b" bold True
            if inventory:
                for item in inventory:
                    text "• [item]" size 16 color "#d4cfc8"
            else:
                text "— empty —" size 16 color "#6b6880" italic True

init python:
    def add_item(item):
        if item not in inventory:
            inventory.append(item)

    def remove_item(item):
        if item in inventory:
            inventory.remove(item)

    def has_item(item):
        return item in inventory

# --- MUSIC HELPER ---
init python:
    import random

    def play_scene_music(track, fadein=0.0):
        try:
            current = renpy.music.get_playing(channel="music")
        except TypeError:
            current = renpy.music.get_playing()

        if current == track or (current and current.rsplit("/", 1)[-1] == track.rsplit("/", 1)[-1]):
            return False

        renpy.music.play(track, channel="music", fadein=fadein)
        return True

# --- PARTY SYSTEM ---
default party_carmelita = False
default party_thut      = False

init python:
    def in_party(companion):
        return globals().get('party_' + companion, False)

# --- GAME FLAGS ---
# (Combat defaults are in combat_system.rpy)
default combat_bonus             = 0
default bone_map_found           = False
default rosentos_slain           = False
default korat_suspicious         = False
default slave_farm_betrayed      = False
default slave_farm_mercy_killed  = False

# ============================================================
# SCENES
# ============================================================

label veterans_tale:
    # Music: warm tavern ambience, the weight of an old story
    $ play_scene_music("audio/mus_luln_tavern.ogg", fadein=1.5)

    # ASSET: Dim frontier tavern interior, low smoke-blackened beams, tallow candles on rough communal tables, a barely-alive fire in a stone hearth. An old soldier sits centre-frame with a clay cup. Warm amber light, deep surrounding shadow.
    scene bg_luln_tavern with fade

    # ASSET: Fondalus the Soldier — aged man in his 60s, deeply weathered face, grey stubble, heavy dark brown wool travelling cloak. Seated at a table, forearms resting on it, clay cup in both hands. Expression grave and world-weary.
    show char_fondalus neutral with dissolve

    narrator "You sit in the smoky warmth of the tavern in Luln, listening to an old soldier nurse his drink."

    fondalus "I tell you only what I saw. Take it or leave it to the crows."
    fondalus "Tharakimeios the Scribe heard every word from my lips, so I'll not have it said I lied."

    narrator "He takes a long drink and begins."

    fondalus "One hundred years ago, Colonel Rosentos led two hundred of us west — ordered by Duke Stefan to claim new lands."
    fondalus "We marched seven days from Luln. That night at the river, a score of men vanished. A hydra. We never found the bodies."
    fondalus "Grisbaldos spoke against marching on. Rosentos had him buried alive under rocks beneath a great oak. His captains said it was necessary."
    fondalus "We built rafts. Three days through the swamp. Fevers took five men. Hedric the Lame disappeared in the night."
    fondalus "We found a village on stilts. A feast was set. But our seer Kerid Bey said to leave. So Rosentos had us sleep with our sandals laced."
    fondalus "We slipped away in the fog. Turim Fellbeard's raft was lost."
    fondalus "The second village — warriors in canoes. A day-long battle. In the end their chief made peace and gave us gold."
    fondalus "Rosentos learned the source from the chief: a great stone house on an island beyond the swamp. He took forty men inland to find it."
    fondalus "I was left to guard the rafts. Swamp beasts took most of us. When only five remained, I brought my men home."
    fondalus "Rosentos never came back. The treasure — if it exists — is still there."

    # ASSET: Fondalus — same figure, now leaning back slightly, one hand smoothing a rough parchment map across the table. Expression weary, relieved to have told it, distant.
    show char_fondalus weary with dissolve

    fondalus "Follow the river west. Seven days. The river grows impassable — build rafts, pole through the swamp. The island appears just before sundown."

    narrator "He slides a rough map across the table."

    menu:
        "Ask about Grisbaldos' grave":
            fondalus "Under a great oak near the slow bend of the river. I would leave it alone if I were you."
            jump luln_departure
        "Ask about Rosentos himself":
            fondalus "He was a good colonel. Brave. Fair. Whatever he became out there — that wasn't the man I followed."
            jump luln_departure
        "Set out immediately":
            jump luln_departure

label luln_departure:
    # Music: open road travel, slightly apprehensive
    $ play_scene_music("audio/mus_explore_river.ogg", fadein=2.0)

    # ASSET: Flat frontier road heading west from Luln, dry grass either side, the road a dirt track curving toward a distant river glinting in hazy morning light. Party silhouettes from behind. Wide, slightly overcast sky.
    scene bg_luln_road with fade

    narrator "You leave Luln as the morning mist burns off. The road heads west, straight and dusty."

    $ renpy.show_screen('inventory_screen')

    narrator "Seven days of marching lie ahead. The river is your guide."

    menu:
        "Follow the riverbank closely — look for the oak grove Fondalus mentioned":
            jump river_camp
        "Make straight time — reach the swamp as fast as possible":
            jump bandits_plain
        "Investigate the slow river bend — that is where the expedition lost men to the hydra":
            jump river_camp

label river_camp:
    # Music: travel ambience, storm building
    $ play_scene_music("audio/mus_explore_river.ogg", fadein=1.5)

    # ASSET: Evening camp on a dry hummock above the river. Storm clouds rolling from the west, distant lightning, the river smell changing. A small fire, bedrolls laid out. The light is amber and dying.
    scene bg_luln_road with fade

    narrator "Day four. Evening camp on a dry hummock above the river. The heat has been building for days."
    narrator "Now a storm rolls in from the west — black clouds, distant thunder, the river smell changing from mud to metal."

    if in_party("carmelita"):
        narrator "Carmelita sharpens a blade by the fire. Without looking up, she speaks."
        carmelita "My grandmother was one of Rosentos' original soldiers. A woman who passed as a man — it was that kind of army."
        carmelita "She told me what he was like before. Before the island. Before whatever happened to him."
        carmelita "She said he used to sing. Can you imagine? A man like that, singing."
        narrator "She tests the edge with her thumb."
        carmelita "After the island, she came back different. She never said what happened. She just... stopped talking about it."
        carmelita "She died when I was twelve. The last thing she said was 'Don't go west.' I've been going west ever since."
        narrator "She says nothing more."

    if in_party("thut"):
        narrator "Thut crouches at the water's edge, reading the mud."
        thut "Large tracks. Reptile. Recent. Heading downstream toward the bend."
        narrator "He points without looking up. The tracks are deep and wide — something heavy, something with many feet."
        narrator "He stays at the water's edge long after the others have settled. Watching the current."
        thut "I watched the island for three years. From the reeds. Never went closer than a hundred yards."
        thut "Korat asked me to go. Many times. I always said no."
        narrator "He does not explain why. But there is something in his voice that sounds like shame."

    narrator "Lightning flashes in the west. The storm will break before midnight."

    menu:
        "Push on through the night — reach the grove before the storm breaks":
            narrator "You march by lightning-flash. The river is silver and black. The rain finds you an hour in, cold as thrown stones."
            narrator "You reach the oak grove at midnight, soaked, exhausted. The cairn stones are visible in the flashes."
            narrator "You sleep poorly, dreaming of hanging. Of dirt filling your mouth."
            jump grisbaldos_grove_night_arrival
        "Camp here — better to face the hydra rested than to fight the river in darkness":
            narrator "You pitch what shelter you can. The storm breaks at midnight — rain like spears, wind that threatens to lift the tents."
            narrator "In the morning, the river is swollen, brown, carrying debris from upstream."
            narrator "You reach the slow bend by midday. The water is churned and angry. Whatever lives here has been flushed from its usual haunts — or driven upstream to calmer water."
            $ hydra_hungry = True
            jump hydra_riverbank

label grisbaldos_grove_night_arrival:
    # Music: eerie quiet, storm aftermath
    $ play_scene_music("audio/mus_explore_haunted.ogg", fadein=2.0)

    # ASSET: The oak grove at night in storm aftermath — wet, dripping, moonlight through thinning clouds. The cairn stones gleam. An oppressive stillness.
    scene bg_grisbaldos_grove_night with fade

    narrator "The storm has passed but the grove holds its breath. Water drips from every leaf. The cairn stones gleam in the returning moonlight."
    narrator "You do not choose to camp here. You collapse here. Exhaustion makes the choice for you."
    narrator "The dreams come quickly — a soldier's face, dirt in his mouth, the sound of rocks being piled."

    jump grisbaldos_ghost_encounter

label hydra_riverbank:
    # Music continues — quiet then sudden tension
    # ASSET: Muddy river bank, tall yellowing reeds, grey-green river water. Ten dark shapes float near the shore that could be crocodile heads — but the silhouette is wrong. Late flat afternoon light. Danger implicit in the stillness.
    scene bg_riverbank_hydra with fade

    narrator "Near the slow bend where Fondalus said men were lost, ten dark shapes drift in the shallows."
    narrator "Crocodiles. Or something like them. They drift toward the bank with uncanny patience."
    narrator "Then one bobs close enough. Not ten crocodiles. One creature. Ten heads on a single enormous body."

    narrator "The creature regards you with ten pairs of cold eyes. Then it moves — faster than anything that size should move."
    narrator "The heads fan out across the water. There is nowhere to run that is not downstream of something that hunts in rivers."

    jump combat_hydra

label combat_hydra:
    stop music fadeout 0.5
    play music "audio/mus_combat_mid.ogg" fadein 0.8
    
    $ hydra_heads = 7
    $ hydra_round = 1
    $ hydra_hits = 0
    $ hydra_stance = "holding"
    $ hydra_specials_used = []
    $ hydra_stance_recover_used = False
    $ hydra_closecall = False
    
    show char_hydra with dissolve
    
    if hydra_hungry:
        narrator "The hydra is agitated — flushed from its usual haunt by the storm, hungry and frenzied."
    
    jump combat_hydra_round

label combat_hydra_round:
    if hydra_round == 1:
        narrator "The hydra surges from the shallows, seven heads snapping at once!"
    
    $ renpy.show_screen('inventory_screen')
    
    # --- SITUATION REPORT ---
    if hydra_stance == "holding":
        narrator "You stand your ground on the muddy bank."
    elif hydra_stance == "reeling":
        narrator "You are pressed back toward the water's edge. Blood runs from wounds."
    else:
        narrator "The water is at your heels. This is your last stand."
    
    # --- HYDRA STATE ---
    if hydra_heads >= 6:
        narrator "The hydra's heads weave and snap, a wall of teeth and fury."
    elif hydra_heads >= 4:
        narrator "[hydra_heads] heads remain active. The beast is bleeding but still dangerous."
    elif hydra_heads >= 2:
        narrator "Only [hydra_heads] heads still fight. The beast is weakening."
    else:
        narrator "The last head thrashes blindly. Victory is close."
    
    # --- PLAYER CHOICE ---
    menu:
        "Strike at the heads with your blade":
            $ bonus = 0
            if has_item("Flaming Sword +1"):
                $ bonus += 1
                narrator "Fire erupts along your blade."
            if has_item("Sword +3: Armory of Morphos"):
                $ bonus += 3
                narrator "The sword pulses with power in your grip."
            jump combat_hydra_attack
        
        "Use fire — cauterize the wounds":
            if has_item("Flaming Sword +1"):
                $ bonus = 2
                $ hydra_weakness = True
                narrator "You slash with the flaming blade. Fire sears the stumps — heads cannot regrow."
                jump combat_hydra_attack
            else:
                narrator "You have no fire to hand. The hydra hisses."
                $ bonus = -1
                jump combat_hydra_attack
        
        "Spread out — divide its attention":
            $ bonus = 1
            narrator "You scatter along the bank, forcing the heads to track multiple targets."
            jump combat_hydra_attack
        
        "Fall back to high ground":
            $ bonus = 0
            $ hydra_defensive = True
            narrator "You retreat up the bank, trading ground for safety."
            jump combat_hydra_attack
        
        "Have Thut identify the weak point" if in_party("thut") and "insight" not in hydra_specials_used:
            $ hydra_specials_used.append("insight")
            narrator "Thut's eyes track the weaving heads. His voice cuts through the chaos."
            thut "The central neck — the one that doesn't weave. It's the original. Sever it, and the others die."
            $ hydra_thut_insight = True
            jump combat_hydra_round
        
        "Have Carmelita create an opening" if in_party("carmelita") and "opening" not in hydra_specials_used:
            $ hydra_specials_used.append("opening")
            $ bonus = 2
            narrator "Carmelita feints left, drawing three heads. You strike from the right."
            jump combat_hydra_attack
        
        "Flee into the river":
            jump combat_hydra_flee

label combat_hydra_attack:
    # --- APPLY MODIFIERS ---
    $ total_bonus = bonus
    
    if hydra_thut_insight:
        $ total_bonus += 2
        $ hydra_thut_insight = False
    
    if in_party("carmelita"):
        $ total_bonus += get_companion_bonus("carmelita", "hydra", "attack")
        if total_bonus > bonus:
            narrator "Carmelita knows how to fight beside you."
    
    if in_party("thut") and "insight" not in hydra_specials_used:
        $ total_bonus += get_companion_bonus("thut", "hydra", "attack")
    
    if hydra_weakness:
        $ total_bonus += 2
    
    # Stance penalty
    if hydra_stance == "reeling":
        $ total_bonus -= 1
    elif hydra_stance == "desperate":
        $ total_bonus -= 2
    
    # --- ROLL ---
    $ raw, total, outcome = roll_d20(total_bonus)
    narrator "You roll... [raw]!"
    
    # --- RESOLVE ---
    if outcome == "critical_success":
        $ hydra_hits += 2
        narrator "CRITICAL! Your blade finds the mark with perfect precision."
        if has_item("Flaming Sword +1"):
            narrator "Fire sears the wound — heads cannot grow back."
        $ hydra_heads -= 2
        if hydra_heads < 1:
            $ hydra_heads = 0
        narrator "[hydra_heads] heads remain."
        
    elif outcome == "success":
        $ hydra_hits += 1
        narrator "A solid hit! One head drops limp."
        if has_item("Flaming Sword +1"):
            narrator "The fire cauterizes the wound."
        $ hydra_heads -= 1
        if hydra_heads < 1:
            $ hydra_heads = 0
        
    elif outcome == "partial":
        narrator "You trade blows. The hydra's teeth scrape your armor."
        $ hydra_hits += 1
        $ hydra_heads -= 1
        if hydra_heads < 1:
            $ hydra_heads = 0
        narrator "[hydra_heads] heads remain."
        if hydra_stance == "holding":
            $ hydra_stance = "reeling"
        
    elif outcome == "failure":
        narrator "The hydra's jaws catch flesh. Blood runs."
        if hydra_stance == "holding":
            $ hydra_stance = "reeling"
        elif hydra_stance == "reeling":
            $ hydra_stance = "desperate"
        # No more instant drag death - companions always help or player survives
        
    else:  # critical_blunder
        narrator "CRITICAL BLUNDER! You slip on the mud. Three heads strike at once."
        $ hydra_stance = "desperate"
        # Companions always cut you free or you grab something
    
    # --- RESET CLOSECALL ON SUCCESS ---
    if outcome in ["critical_success", "success"]:
        $ hydra_closecall = False
    
    # --- CHECK VICTORY/DEFEAT ---
    if hydra_heads <= 0:
        jump combat_hydra_victory
    
    if hydra_hits >= 5:
        jump combat_hydra_victory
    
    if hydra_stance == "desperate" and outcome in ["failure", "critical_blunder"]:
        if hydra_closecall:
            jump game_over_hydra
        else:
            $ hydra_closecall = True
            narrator "You barely survive. The water is at your back. One more mistake and it's over."
    
    # --- ENEMY RESPONSE ---
    $ hydra_round += 1
    
    if hydra_round > 3:
        narrator "The hydra is tiring. So are you."
    
    jump combat_hydra_round

label combat_hydra_victory:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    hide char_hydra with dissolve
    
    if hydra_heads <= 0:
        narrator "The last head falls limp. The hydra sinks beneath the dark water, finally still."
    else:
        narrator "Wounded beyond fighting, the hydra slides into the current and does not return."
    
    jump hydra_loot

label hydra_loot:
    narrator "You find the hydra's lair — a hollow in the riverbank, half-filled with water."
    narrator "A mud nest holds seven hydra eggs, leathery and warm. Scattered about: thousands of copper and silver coins."
    $ add_item("Hydra Eggs (7)")
    $ add_item("Lapis Lazuli Bracelet")
    narrator "And a solid lapis lazuli bracelet, worth a fortune to the right buyer."
    
    if in_party("carmelita"):
        carmelita "My grandmother's expedition lost five men to this thing. Now it's done."
    
    narrator "You leave the lair and continue along the riverbank. The sun is lower now."
    narrator "Ahead, the land rises. Oaks stand on the hilltop, their canopy dark against the sky."
    
    jump grisbaldos_grove

label combat_hydra_flee:
    narrator "You dive into the river. The water is cold and fast."
    
    $ raw, total, outcome = roll_d20(2)  # Bonus for choosing to flee smartly
    
    if outcome in ["critical_success", "success", "partial"]:
        narrator "The hydra does not follow into deep water. You escape upstream, battered but alive."
        jump grisbaldos_grove
    else:
        # Failure - you escape but take a wound
        narrator "The current pulls you under. You surface downstream, bleeding but alive."
        narrator "The hydra does not pursue. You've escaped... but you won't be reaching the grove this way."
        # Player must choose another path - skip hydra loot
        jump swamp_entrance_path

label grisbaldos_grove:
    # Music: eerie quiet, oak grove, distant wind
    $ play_scene_music("audio/mus_explore_haunted.ogg", fadein=2.0)

    # ASSET: A rise near the riverbank, ancient oaks forming a canopy, late afternoon light filtering through leaves. Mossy ground, a rotting stump at centre, a scattered ring of old mossy stones — remnants of a cairn. Still and ominous.
    scene bg_grisbaldos_grove with fade

    narrator "A rise near the slow river bend. A grove of oaks stands on top — old, thick-rooted, their canopy blotting the sky."
    narrator "Screened from outside view: a rotting stump. Stones lie scattered in the earth. The remains of a cairn."

    menu:
        "Camp here for the night":
            jump grisbaldos_ghost_encounter
        "Examine the grave before deciding":
            narrator "The cairn has collapsed over decades. The earth beneath it is undisturbed. You feel an uneasy weight in this place."
            menu:
                "Camp here anyway — it is the safest spot nearby":
                    jump grisbaldos_ghost_encounter
                "Move on — camp downstream":
                    jump bandits_plain
        "Leave it alone — press on":
            jump bandits_plain

label grisbaldos_ghost_encounter:
    # Music: dramatic stinger then haunted ambient
    play music "audio/mus_stinger_ghost.ogg"
    pause 2.0
    $ play_scene_music("audio/mus_explore_haunted.ogg", fadein=1.0)

    # ASSET: The oak grove at night, moonlight barely penetrating the canopy. Pale green light drifts between the trees in darting balls. A shaft of cold light rises from the earth of the cairn. The ghost is beginning to form — transparent figure in tattered military uniform, head lolling to one side.
    scene bg_grisbaldos_grove_night with fade

    narrator "In the dark hours, pale green light begins to move through the trees — darting, flitting."
    narrator "Then a shaft of cold light rises from the earth of the cairn."
    narrator "It takes shape. A man. Transparent. A century-old soldier's uniform, tattered and decayed. His head lolls sideways."
    narrator "Around his neck — thick dark rope burns."

    # ASSET: Ghost of Grisbaldos — transparent full-body figure in century-old military uniform, rope burns at neck, arms outstretched, head lolling, pale green glow throughout. Expression vacant and yearning.
    show char_grisbaldos_ghost neutral with dissolve

    narrator "The ghost drifts toward you, arms outstretched."

    menu:
        "Stand your ground — let it approach":
            narrator "The ghost's fingers brush a companion. It evaporates in a cloud of cold light."
            jump grisbaldos_possessed
        "Try to turn the ghost using faith":
            narrator "You invoke your faith. The ghost shatters — then a freezing wind thunders through the grove, hurling leaves and small items through the air."
            narrator "A maniacal disembodied laugh. Then the ghost reforms, approaching again."
            jump grisbaldos_possessed
        "Back away from the grove":
            narrator "You retreat. The ghost stops at the edge of the cairn stones. It watches you go. Then it raises one hand — pointing upstream."
            narrator "You feel certain it will find you again."
            jump grove_departure

label grisbaldos_possessed:
    # ASSET: Close-up of a party member — eyes blank and glazed, pale green light visible in the pupils. They are speaking but their voice is not entirely their own. The dark grove is behind them.
    scene bg_grisbaldos_grove_night with fade

    narrator "A companion goes rigid. Their eyes fill with pale green light. When they speak, the voice is not entirely their own."

    possessed "Where is Rosentos? WHERE IS ROSENTOS?"

    narrator "For a full hour, they ask this — insistently, of everyone present."
    narrator "But while the ghost possesses them, they can answer questions about the expedition, up to the moment Grisbaldos was killed."

    menu:
        "Ask: How did men die at the riverbank on the first night?":
            possessed "The hydra came in the night. We never saw it until it had us. Rosentos drove it off but a score were taken beneath the water."
            menu:
                "Ask: Which direction did the troop march?":
                    possessed "Upstream. Always upstream. Following the chief's directions to the island."
                    jump grisbaldos_oath
                "Ask: Did Rosentos truly betray his men?":
                    possessed "He was weak. He listened to his captains. I warned him the spirits were against us. He did not listen."
                    menu:
                        "Press further — ask what really happened":
                            possessed "The captains said I was the traitor. That I spoke against the mission to save myself. They lied."
                            narrator "A long silence. The green light in your companion's eyes flickers — dimmer, then brighter."
                            possessed "But I did speak against the mission. I did try to turn the men back. The captains were right about that much."
                            possessed "Rosentos buried me for the wrong reason. But I would have stopped him if I could. I would have saved us all."
                            narrator "Another pause. When the voice returns, it is quieter. Older."
                            possessed "Or... I would have saved myself. Even I cannot remember which anymore."
                            $ grisbaldos_contradiction_known = True
                            jump grisbaldos_oath
                        "That is enough — let the hour pass":
                            jump grisbaldos_oath
        "Ask: Which direction did the expedition march along the river?":
            possessed "Upstream. Always upstream. To the island. That is where he went. That is where he is."
            jump grisbaldos_oath
        "Ask nothing — wait for the hour to pass":
            narrator "You wait in cold silence. After an hour, the green light fades from your companion's eyes. They sag, exhausted."
            jump grisbaldos_oath

label grisbaldos_oath:
    narrator "The light leaves your companion's eyes. They are themselves again, pale and drained."

    # ASSET: Ghost of Grisbaldos reformed — same figure, but now pointing directly at the viewer. Expression no longer vacant — cold, demanding, implacable. The grove visible behind him, the cairn earth disturbed.
    show char_grisbaldos_ghost demanding with dissolve

    narrator "The ghost reforms before you. Its posture has changed. It no longer reaches. It points."

    grisbaldos_ghost "Find Rosentos. Slay him. Swear it."

    if grisbaldos_contradiction_known:
        narrator "But you remember: he admitted he might have been saving himself. You remember: the captains called him traitor."
        narrator "Rosentos buried a man who spoke against the mission. But did he bury an innocent? Or did he bury a man who would have abandoned them all?"

    menu:
        "Swear the oath — you will find and destroy Rosentos":
            $ grisbaldos_oath_taken = True
            if grisbaldos_contradiction_known:
                narrator "You swear. Whatever Grisbaldos was in life — coward or martyr — Rosentos is a monster now. That is enough."
            else:
                narrator "You swear. The ghost regards you a long moment — then dissolves into the earth without a sound."
            narrator "The grove goes still. Somewhere upstream, a reckoning waits."
            jump grove_departure
        "Refuse the oath":
            $ grisbaldos_cursed = True
            if grisbaldos_contradiction_known:
                narrator "The ghost's expression cracks — not at refusal, but at being seen through."
                grisbaldos_ghost "You think you understand. You think you see clearly."
                grisbaldos_ghost "I thought the same. Before the dirt filled my mouth."
            else:
                narrator "The ghost's expression goes cold as iron."
                grisbaldos_ghost "Then I will follow."
            narrator "The ghost vanishes — but you feel certain it has not gone far."
            jump grove_departure

label grove_departure:
    scene bg_grisbaldos_grove with dissolve
    
    narrator "Dawn finds you in the grove. The cairn stones are wet with dew."
    
    if grisbaldos_oath_taken:
        narrator "The oath sits in your chest like a weight. Not heavy. But present."
        narrator "Somewhere upstream, a vampire waits. You have work to do."
    elif grisbaldos_cursed:
        narrator "You feel watched. You always will, now."
    
    narrator "You break camp and head downstream. The grass rises on either side of the river."
    
    jump bandits_plain

label bandits_plain:
    # Music: open plain, deceptive calm before the ambush
    $ play_scene_music("audio/mus_explore_river.ogg", fadein=1.5)

    # ASSET: Five-foot-tall yellowing grass rising above a steep riverbank, dustclouds in the air. A light breeze bends the grass. Something massive and armoured is rising from the grass — a figure in black polished armour with metal studs, holding a glittering black blade. A pale-eyed black horse stands beside it.
    scene bg_bandits_plain with fade

    narrator "The grass rises five feet on either side of the river path, yellowing under the heat. Dustclouds clog the air."
    narrator "Then, across the breeze, you hear it: the creak of leather. A whinny."
    narrator "A demonic-looking humanoid rises from the long grass. Black polished armour, metal studs, a menacing leer held tight on its face. A glittering black blade."
    narrator "Beside it stands a lean black horse. Pale fire glows in the horse's eyes. Smoke rises from the long grass around its feet."

    bandit_chief "Lay down your weapons. You have disturbed me!"

    narrator "He speaks in Common, but his accent is elven. And his eyes are scanning the grass around you."

    menu:
        "Lay down weapons as instructed":
            narrator "You comply — and in the two minutes that follow, thirty-five bandits rise from the grass and circle you completely."
            bandit_chief "Wise. Now — your coin pouches."
            bandit_chief "You head to the swamp, yes? The stilt-villages? The island?"
            bandit_chief "I know the paths. I know what lives there. I have lost... enough... to know."
            bandit_chief "The gold you carry now is safer than what waits there. Turn back."
            narrator "He says this while his men circle. He does not mean it as kindness. He means it as prediction."
            narrator "The chieftain raises his black blade. It erupts into flame."
            narrator "Thirty-five voices. Then silence. The grass rustles."
            jump combat_bandit_chieftain
        "Refuse and hold your ground":
            narrator "He stalls, speaking at length about your offense. The grass rustles on all sides."
            bandit_chief "You head to the swamp, yes? The stilt-villages? The island?"
            bandit_chief "I know what lives there. I have lost... enough... to know."
            narrator "Thirty-five bandits rise from the grass and close the circle."
            narrator "The chieftain raises his black blade. It erupts into flame."
            narrator "For a heartbeat, nobody moves. Then everything moves at once."
            jump combat_bandit_chieftain
        "Attack immediately — before he can stall further":
            narrator "You act before the circle can close. The chieftain's eyes go wide, then narrow."
            narrator "His blade ignites. Thirty-five bandits surge from the grass."
            $ combat_bonus_final = 1
            jump combat_bandit_chieftain

label combat_bandit_chieftain:
    stop music fadeout 0.5
    play music "audio/mus_combat_mid.ogg" fadein 0.8
    
    $ bandit_round = 1
    $ bandit_hits = 0
    $ bandit_stance = "holding"
    $ bandit_specials_used = []
    $ bandit_fire_rounds = 0
    $ bandit_surrounded = False
    $ bandit_closecall = False
    
    # Carry any ambush bonus
    $ bandit_bonus = combat_bonus_final
    $ combat_bonus_final = 0
    
    narrator "Thirty-five bandits surge from the grass. The chieftain raises his black blade and it erupts into flame."
    
    jump combat_bandit_round

label combat_bandit_round:
    if bandit_round == 1:
        if bandit_bonus > 0:
            narrator "You struck before the circle closed. Some bandits are still rising from the grass."
        else:
            narrator "The bandit ring is complete. Thirty-five men with swords drawn."
            $ bandit_surrounded = True
    
    # --- SITUATION REPORT ---
    if bandit_stance == "holding":
        narrator "You hold formation in the tall grass."
    elif bandit_stance == "reeling":
        narrator "Blood runs from wounds. The bandits are pressing harder."
    else:
        narrator "This is your last chance. The plain burns behind you."
    
    # --- FIRE HAZARD ---
    if bandit_fire_rounds > 0:
        $ bandit_fire_rounds += 1
        narrator "The grass fire spreads. Smoke thickens the air."
        if bandit_fire_rounds >= 5:
            narrator "The blaze is out of control. The plain itself is dying."
    
    # --- PLAYER CHOICE ---
    menu:
        "Target the chieftain directly — break the command":
            $ bonus = 2
            $ targeting_chieftain = True
            narrator "You drive straight for the chieftain, ignoring the foot soldiers."
            jump combat_bandit_attack
        
        "Hold a tight defensive circle":
            $ bonus = 1
            $ bandit_defensive = True
            narrator "You form a ring, keeping each other's backs covered."
            jump combat_bandit_attack
        
        "Use fire — set the grass ablaze":
            if has_item("Flaming Sword +1") or has_item("Ring of Fire Resistance"):
                narrator "You touch flame to the dry grass. It catches instantly."
                $ bandit_fire_rounds = 1
                jump combat_bandit_round
            else:
                $ bonus = -1
                narrator "The fire spreads — but you have no protection from it."
                narrator "The chieftain laughs and steps into the blaze, his ring glowing."
                jump combat_bandit_attack
        
        "Fall back toward the river":
            $ bonus = 0
            narrator "You retreat toward the water, where their numbers mean less."
            jump combat_bandit_attack
        
        "Have Thut identify the chieftain's weakness" if in_party("thut") and "insight" not in bandit_specials_used:
            $ bandit_specials_used.append("insight")
            narrator "Thut watches the chieftain's stance, the way he moves."
            thut "He favors his left side. And he's stalling — he hasn't used his magic yet."
            $ bandit_thut_insight = True
            jump combat_bandit_round
        
        "Have Carmelita create a distraction" if in_party("carmelita") and "opening" not in bandit_specials_used:
            $ bandit_specials_used.append("opening")
            $ bonus = 2
            narrator "Carmelita shouts and gestures, drawing the bandits' attention. You strike at the gap."
            jump combat_bandit_attack
        
        "Surrender — offer your coin and leave":
            narrator "You raise your hands. The chieftain approaches, sword still flaming."
            bandit_chief "Wise. But I think you have more than coin."
            jump game_over_bandits_robbed

label combat_bandit_attack:
    # --- APPLY MODIFIERS ---
    $ total_bonus = bonus
    
    if bandit_bonus > 0:
        $ total_bonus += bandit_bonus
        $ bandit_bonus = 0
    
    if bandit_thut_insight:
        $ total_bonus += 2
        $ bandit_thut_insight = False
    
    if in_party("carmelita"):
        $ total_bonus += get_companion_bonus("carmelita", "bandit_chieftain", "attack")
    
    # Stance penalty
    if bandit_stance == "reeling":
        $ total_bonus -= 1
    elif bandit_stance == "desperate":
        $ total_bonus -= 2
    
    # Fire penalty
    if bandit_fire_rounds >= 3:
        $ total_bonus -= 1
        narrator "The smoke stings your eyes."
    
    # --- ROLL ---
    $ raw, total, outcome = roll_d20(total_bonus)
    narrator "You roll... [raw]!"
    
    # --- RESOLVE ---
    if outcome == "critical_success":
        $ bandit_hits += 2
        narrator "CRITICAL! Your blade finds the gap in his armor!"
        if targeting_chieftain:
            narrator "The chieftain staggers. His men freeze."
        
    elif outcome == "success":
        $ bandit_hits += 1
        narrator "A solid strike! The chieftain is driven back."
        
    elif outcome == "partial":
        narrator "You trade blows. The bandits press harder."
        if bandit_stance == "holding":
            $ bandit_stance = "reeling"
        
    elif outcome == "failure":
        narrator "The chieftain's flaming sword scores a terrible wound."
        if bandit_stance == "holding":
            $ bandit_stance = "reeling"
        elif bandit_stance == "reeling":
            $ bandit_stance = "desperate"
        
    else:  # critical_blunder
        narrator "CRITICAL BLUNDER! The chieftain chants words of power."
        if bandit_fire_rounds > 0:
            narrator "The fire you started spreads to cut off your retreat."
        $ bandit_stance = "desperate"
    
    # --- RESET CLOSECALL ON SUCCESS ---
    if outcome in ["critical_success", "success"]:
        $ bandit_closecall = False
    
    # --- CHECK VICTORY/DEFEAT ---
    if bandit_hits >= 2:
        jump combat_bandit_victory
    
    if bandit_stance == "desperate" and outcome in ["failure", "critical_blunder"]:
        if bandit_closecall:
            jump game_over_bandits
        else:
            $ bandit_closecall = True
            narrator "You barely survive. Blood runs, but you stand. One more mistake ends this."
    
    # --- ENEMY RESPONSE ---
    $ bandit_round += 1
    
    if bandit_round > 2:
        narrator "The fight is exhausting. Both sides are bloodied."
    
    jump combat_bandit_round

label combat_bandit_victory:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    if bandit_hits >= 3:
        narrator "The chieftain falls. Without his command, the thirty-five bandits scatter into the grass."
        $ bandit_chief_killed = True
    else:
        narrator "The chieftain staggers back, wounded. His men break and flee."
    
    jump bandit_loot

label bandit_loot:
    if bandit_chief_killed:
        narrator "You claim the chieftain's sword — it flames on command — and his rings."
        $ add_item("Flaming Sword +1")
        $ add_item("Ring of Fire Resistance")
        narrator "On his body: a crude map. The river, the swamp, the island. Marked with symbols you don't recognize."
        narrator "And a note, in broken Common: 'He promised the thralls would not remember. They remember enough to scream.'"
        
        if in_party("carmelita"):
            carmelita "He knew about Rosentos. He traded with him, or worse."
    else:
        narrator "The bandits flee into the grass. You have the field."
    
    narrator "The plain is quiet. The bandits are gone."
    narrator "You press on. The grass thins. The air changes — wetter, cooler. The river smell is stronger."
    narrator "The swamp is ahead."
    
    jump swamp_entrance_path

label swamp_entrance_path:
    # Music: bleak swamp ambience, cold and still
    $ play_scene_music("audio/mus_explore_swamp.ogg", fadein=2.0)

    # ASSET: The river dissolving into swampland — reeds as far as the eye can see, open patches of still dark water between them, flat grey sky. Two crude log rafts visible at the waterline, loaded with supplies.
    scene bg_swamp_entrance with fade

    narrator "The riverbanks have grown treacherous — mud, reeds, and stagnant pools replace firm ground."
    narrator "You cut timber and build rafts, loading them with supplies. The swamp offers no dry path forward."

    if grisbaldos_cursed:
        narrator "Twice during the building, something moves at the edge of camp. There is never anything there when you look. A pale shimmer lingers between the trees."
    
    narrator "You pole away from the bank. The river dissolves into channels and reeds."
    narrator "The current is slow. The water is black. The world narrows to the sound of poles in mud."
    
    jump swamp_journey

label swamp_journey:
    # ASSET: View from a raft poling through a narrow swamp channel, towering reeds on either side, dark still water below, the channel curving into deeper shadow ahead. A dead tree leans over the water. Overcast sky.
    scene bg_swamp_channel with fade

    narrator "Three days of poling through channels that offer no sense of direction."
    narrator "Fevers visit two companions in the night. The water is never entirely still."
    
    if in_party("carmelita") and in_party("thut"):
        narrator "On the second night, Carmelita and Thut argue quietly by the fire."
        carmelita "We should go faster. Before he knows we're coming."
        thut "Faster gets you killed. The swamp doesn't care about your grandmother's ghost."
        carmelita "Don't you dare—"
        thut "I've watched people charge that island. They don't come back."
        narrator "Silence. Then Carmelita turns away. Thut stares at the water."
        narrator "They don't speak again until morning."
    elif in_party("carmelita"):
        narrator "Carmelita sits at the edge of the raft, legs dangling over the water."
        carmelita "My grandmother used to tell me stories about the swamp. She said it remembers."
        carmelita "She said if you listen at night, you can hear the ones who didn't come back."
        narrator "She listens. You don't hear anything."
    elif in_party("thut"):
        narrator "Thut poles the raft without being asked. He knows the channels."
        thut "This one forks ahead. Left goes to the burned village. Right goes... somewhere else."
        narrator "He pauses."
        thut "I've never gone right. Nobody has who came back."
        narrator "He takes the left fork without asking."

    menu:
        "Investigate the hemisphere of absolute darkness you see in a pool ahead":
            jump slough_of_despair
        "Keep moving — do not stop for every strange thing in this swamp":
            jump burned_village

label slough_of_despair:
    # Music: dramatic stinger then oppressive near-silence
    play music "audio/mus_stinger_despair.ogg"
    pause 3.0
    stop music fadeout 1

    # ASSET: A bleak open swamp pool surrounded by standing reeds. At the centre: a perfect hemisphere of absolute darkness, roughly 15 feet across. No light enters it, no light reflects from it. The reeds are utterly still. A void in the world.
    scene bg_slough_despair with fade

    narrator "The wind drops. All sound stops."
    narrator "In the centre of a stagnant pool: a hemisphere of perfect darkness. No light enters it. No light escapes."
    narrator "Then — a piercing scream erupts from inside it. Swampbirds explode from the reeds in all directions."

    menu:
        "Push the raft into the darkness — someone may need help":
            jump slough_vision
        "Leave it alone — press on":
            $ play_scene_music("audio/mus_explore_swamp.ogg", fadein=1.5)
            narrator "You pole away. For hours afterward, a gnawing guilt persists — the feeling of someone abandoned when they needed you."
            jump burned_village

label slough_vision:
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.5)
    narrator "You push into the hemisphere. Inside: nothing. No walls, no creature, no screaming figure."
    narrator "Only silence. Absolute, crushing silence."
    narrator "Then the darkness speaks. Not in words. In images."
    narrator "A camp. Soldiers. A young man in command — handsome, confident, laughing. Rosentos. Before."
    narrator "An older officer beside him — the colonel. Fondalus' colonel. They clasp arms like brothers."
    narrator "Then: the island. The treasure. A disagreement."
    narrator "The colonel wanted the gold. Rosentos wanted the knowledge. The Essence-Orb. The questions it could answer."
    narrator "The colonel struck first. Left Rosentos on the island with his 'disloyalty' and the swamp closing in."
    narrator "But the swamp did not kill Rosentos. Something else found him. Something older than the cay-men, older than the treasure."
    narrator "It offered him survival. It offered him power. It asked only one thing in return: to feed."
    narrator "The vision ends. You are standing on the raft. Your companions are pale."
    
    $ slough_vision_seen = True
    
    if in_party("carmelita"):
        carmelita "My grandmother never told me that part. She said the colonel abandoned him. She didn't say why."
        narrator "Carmelita is shaking. Not from fear. From something else."
        carmelita "He was betrayed. By his own commander. Left to die."
        carmelita "That doesn't make what he became right. But it makes it... something."
    
    if in_party("thut"):
        thut "The colonel got the gold. Rosentos got the swamp."
        thut "Funny how that works."
        narrator "Thut stares at the darkness for a long moment."
        thut "I watched from the reeds for three years. I could have ended it sooner."
        thut "But I was afraid too. Afraid of becoming something. Or not becoming anything."
    
    narrator "The darkness lifts. Sound returns. The swamp is just the swamp again."
    
    # Apply debuff for investigating
    $ slough_debuffed = True
    narrator "But the vision stays with you. In battles to come, you will fight at a disadvantage — until you prove yourself against a worthy foe."
    
    jump burned_village

label burned_village:
    # Music: grim, the quiet of long abandonment
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.5)

    # ASSET: Ruined swamp village on stilts at the edge of a spongy hummock. Hut frames open to the sky, roofs long missing, floors sagging and splintered. The wood is fire-blackened. Reeds clog the waterways around the stilts. Utterly desolate.
    scene bg_burned_village with fade

    narrator "The desolate frames of ruined huts stand on stilts at the edge of a spongy hummock."
    narrator "Roofs missing. Floors splintered and sagged. The wood is charred. This place burned a long time ago and was never rebuilt."

    menu:
        "Search the standing huts":
            narrator "You climb onto the stilts carefully, testing each board. The floors groan but hold."
            narrator "Junk scattered everywhere — rotted fabric, broken clay, unidentifiable remnants."
            narrator "After a full turn of searching, you find something lodged beneath a collapsed floor section."
            narrator "A piece of carved bone. Writing on it, faint but legible."
            $ add_item("Carved Bone Map Fragment")
            $ bone_map_found = True
            narrator "You make out: 'Truly the days of Kelshet and his evil hordes are numbered!' — but which village Kelshet led, the bone does not say."
            jump burned_village_ghouls
        "This place stinks of death — back onto the raft immediately":
            narrator "Your instincts scream. You push off the stilts and retreat to the raft — just in time."
            jump burned_village_ghouls

label burned_village_ghouls:
    stop music fadeout 0.5
    play music "audio/mus_combat_low.ogg" fadein 0.8

    # ASSET: Night view of the burned village stilts, dark water below. From beneath the water, waterlogged ghouls are climbing the stilts in absolute silence — fifteen of them, grey-white and bloated, dark water streaming from their flesh.
    scene bg_burned_village_night with fade

    narrator "The silence presses in. Something is wrong. The air has gone cold."
    narrator "Then you hear it — a scraping sound. Wood on wood. From beneath the stilts."
    narrator "From the black water beneath the stilts, shapes begin to emerge."
    narrator "They climb silently — fifteen ghouls, dead underwater for a very long time. Dark water streams from their grey flesh."
    narrator "They attack from all sides."

    jump combat_ghouls

label combat_ghouls:
    stop music fadeout 0.5
    play music "audio/mus_combat_low.ogg" fadein 0.8
    
    $ ghoul_round = 1
    $ ghoul_wounds = 0  # Times player got hit (3 = overwhelmed)
    $ ghoul_driven_back = 0  # Times player succeeded (3 = victory)
    $ ghoul_specials_used = []
    $ ghoul_closecall = False
    
    narrator "Fifteen ghouls climb the stilts from the black water. Their eyes are hollow. Their claws are long and pale."
    
    jump combat_ghouls_round

label combat_ghouls_round:
    # --- SITUATION REPORT ---
    if ghoul_round == 1:
        narrator "They emerge from the water in silence — waterlogged, grey-white, bloated from years beneath the surface."
    else:
        narrator "The ghouls press forward. Cold hands reach for you."
    
    # Show wounds vs progress
    narrator "You've driven back [ghoul_driven_back] wave(s). You've taken [ghoul_wounds] hit(s)."
    
    # --- PLAYER CHOICE ---
    menu:
        "Hold a fighting line at the stilt heads":
            $ bonus = 2
            narrator "You concentrate your defense at the single point of approach."
            jump combat_ghouls_attack
        
        "Attack down the stilts — meet them in the water":
            $ bonus = 1
            narrator "You take the fight to them while they climb."
            jump combat_ghouls_attack
        
        "Use fire — torches and flame":
            if has_item("Flaming Sword +1") or has_item("Ring of Fire Resistance"):
                $ bonus = 2
                $ ghoul_fire = True
                narrator "Fire erupts. The ghouls recoil from the light and heat."
            else:
                $ bonus = 1
                narrator "You hold torches forward. The ghouls flinch from the light."
            jump combat_ghouls_attack
        
        "Scramble for the raft — escape":
            jump combat_ghouls_flee
        
        "Have Thut identify their weakness" if in_party("thut") and "insight" not in ghoul_specials_used:
            $ ghoul_specials_used.append("insight")
            narrator "Thut watches the ghouls' movements. His voice is tight."
            thut "They were drowned. Held underwater for years. They still move like swimmers — slow on land, fast in water."
            thut "Keep them off the platform. Don't let them drag you down."
            $ ghoul_thut_insight = True
            jump combat_ghouls_round
        
        "Have Carmelita hold the line" if in_party("carmelita") and "opening" not in ghoul_specials_used:
            $ ghoul_specials_used.append("opening")
            $ bonus = 2
            narrator "Carmelita steps forward, blade steady. 'I'll hold them here. You strike.'"
            jump combat_ghouls_attack

label combat_ghouls_attack:
    # --- APPLY MODIFIERS ---
    $ total_bonus = bonus
    
    if ghoul_thut_insight:
        $ total_bonus += 2  # Better bonus for the insight
    
    if ghoul_fire:
        $ total_bonus += 1
    
    if in_party("carmelita"):
        $ total_bonus += get_companion_bonus("carmelita", "ghouls", "attack")
    
    # Slough debuff
    if slough_debuffed:
        $ total_bonus -= 1
        narrator "The shadow of the Slough still weighs on you."
    
    # --- ROLL ---
    $ raw, total, outcome = roll_d20(total_bonus)
    narrator "You roll... [raw]!"
    
    # --- RESOLVE: 6+ = success (hurt them), <6 = failure (they hurt you) ---
    if total >= 6:
        # Player succeeds - drive back a wave
        $ ghoul_driven_back += 1
        $ ghoul_closecall = False  # Reset on success
        
        if raw == 20:
            narrator "CRITICAL! Your blade cleaves through two ghouls at once. They collapse back into the water."
            $ ghoul_driven_back += 1  # Extra progress on crit
        elif raw >= 15:
            narrator "A solid strike! Ghouls tumble back into the black water, bodies twitching."
        else:
            narrator "You drive them back. The line wavers but holds."
        
        # Check victory
        if ghoul_driven_back >= 3:
            narrator "The last ghouls scramble away into the water. The platform holds."
            jump combat_ghouls_victory
    else:
        # Player fails - take a wound
        $ ghoul_wounds += 1
        
        if raw == 1:
            narrator "CRITICAL BLUNDER! You slip on the wet planks. Cold hands seize you!"
            $ ghoul_wounds += 1  # Extra wound on blunder
        
        narrator "A ghoul's claws rake across your arm. Cold spreads from the wound."
        
        if in_party("carmelita") or in_party("thut"):
            narrator "Your companions pull you back from the edge."
        elif ghoul_wounds >= 3:
            # Overwhelmed - check closecall
            if ghoul_closecall:
                narrator "The cold spreads through your body. You cannot move your legs."
                jump game_over_ghouls_paralyzed
            else:
                $ ghoul_closecall = True
                narrator "You fight off the paralysis. But the cold waits in your veins, ready to finish what it started."
        elif ghoul_wounds >= 2:
            narrator "The cold settles deeper. Your movements are slowing."
        else:
            narrator "Pain flares, then numbness. You shake it off... for now."
        
        # Check if still in fight
        if ghoul_wounds >= 3 and not ghoul_closecall:
            pass  # Already handled above
        elif ghoul_wounds >= 3 and ghoul_closecall:
            jump game_over_ghouls_paralyzed
    
    # --- NEXT ROUND ---
    $ ghoul_round += 1
    jump combat_ghouls_round

label combat_ghouls_victory:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    narrator "The last ghoul sinks back into the black water. The platform holds."
    
    if ghoul_wounds == 0:
        narrator "Clean victory. The cold never touched you."
    elif ghoul_wounds == 1:
        narrator "One wound. The cold lingers, but you can push through."
    else:
        narrator "Both of you are wounded. The cold has settled deep."
        narrator "It will take time to shake it off. If you ever do."
    
    if slough_debuffed:
        narrator "You fought through it — the shadow of the Slough begins to recede."
        $ slough_debuffed = False
    
    jump ghouls_aftermath

label ghouls_aftermath:
    stop music fadeout 1.0
    pause 0.5
    $ play_scene_music("audio/mus_explore_swamp.ogg", fadein=2.0)
    
    narrator "You stand among the ruins. The silence after combat is louder than the fighting."
    
    if ghoul_wounds == 0:
        narrator "No one is seriously wounded. But the ghouls' touch leaves a cold that doesn't fade quickly."
    elif ghoul_wounds == 1:
        narrator "Someone is shaking. Someone else is checking wounds with steady hands."
    else:
        narrator "Both of you are bleeding. The wounds go cold almost immediately."
        narrator "You bandage what you can, but the numbness spreads."
    
    if in_party("carmelita"):
        carmelita "That was too close. We need to keep moving."
    
    if in_party("thut"):
        thut "The second village is not far. We push on."
    
    narrator "You pole away from the burned village before anything else comes out of the water."
    
    jump second_village_approach

label combat_ghouls_flee:
    narrator "You scramble for the raft."
    
    $ raw, total, outcome = roll_d20(1)  # Bonus for choosing escape
    
    if total >= 6:
        narrator "You push off before the ghouls can reach the platform. They do not follow into deep water."
        jump ghouls_aftermath
    else:
        narrator "Ghouls are already on the raft. The platform is swarming."
        $ ghoul_wounds += 1
        narrator "You fight them off, but take a wound in the process."
        jump combat_ghouls_round

label second_village_approach:
    # Music: cautious, inhabited but wrong
    $ play_scene_music("audio/mus_explore_swamp.ogg", fadein=1.5)

    # ASSET: A small lake of open water in the swamp, six small huts on sapling stilts, woven branch platforms, crude reed roofs. A mongrel dog leaps between platforms. Half-rotted dugout canoes tied to the stilts. Furtive movements near the hut doors.
    scene bg_second_village with fade

    narrator "Through the reeds, a small lake of open water opens ahead. Six huts on stilts, woven branch platforms. People move near the doorways."
    narrator "A mongrel dog leaps between platforms. Canoes bob at the stilts, half-rotten."
    narrator "At 150 feet, a shouted voice hails you in an unknown tongue — then switches to Common:"
    narrator "\"You come too soon. Go away. It is not the time.\""

    menu:
        "Reply in Common — announce you are travellers, not enemies":
            jump second_village_korat
        "Say nothing and hold your position":
            narrator "Twenty arrows fly from the huts — warning shots, falling short."
            jump second_village_korat
        "Raise something white — signal peaceful intent":
            jump second_village_korat

label second_village_korat:
    # Music: subdued, a broken place
    $ play_scene_music("audio/mus_second_village.ogg", fadein=1.5)

    # ASSET: Doorway of the largest hut. Chief Korat — gaunt, hollow-eyed, emaciated, wearing ceremonial feathers and a bone necklace over simple woven cloth. He is on his knees, pressing his forehead toward the floor. Terrified submission.
    scene bg_second_village with fade
    show char_korat fearful with dissolve

    narrator "After a burst of shouted argument from inside the huts, a gaunt man steps from the largest doorway."
    narrator "He looks like a man who has not slept peacefully in years. He falls to his knees."

    korat "Please forgive us, masters. Rooms have been prepared for you. Do not punish us, my masters."

    narrator "He presses his forehead to the woven platform."

    menu:
        "Play along — let him believe you serve Rosentos":
            $ korat_suspicious = False
            korat "Of course. The Isle is prepared. Rosentos will be... most pleased by your visit."
            narrator "His smile does not reach his eyes."
            jump second_village_talk
        "Tell him plainly that you do not serve Rosentos":
            $ korat_suspicious = True
            narrator "Korat's servile expression flickers. Something else moves beneath it."
            korat "Ah. I... see. Then you are guests."
            narrator "He smiles too widely. He is already thinking."
            jump second_village_talk

label second_village_talk:
    # ASSET: Interior of a large hut on stilts — reed mats, a small fire pit, crude furniture. Daylight from an open doorway. The hut is worn but lived-in.
    scene bg_second_village_interior with fade

    narrator "Korat withdraws to confer with others. You are left in a large hut."

    menu:
        "Seek out Carmelita — the young woman who speaks Common":
            jump meet_carmelita
        "Seek out Thut — the sullen tracker":
            jump meet_thut
        "Move through the village openly":
            narrator "The natives shrink from you, eyeing you with reverence or terror — you cannot tell which."
            menu:
                "Find Carmelita":
                    jump meet_carmelita
                "Find Thut":
                    jump meet_thut

label meet_carmelita:
    # ASSET: Carmelita — young woman of mixed ancestry, 20s, bright dark eyes, simple woven cloth dress with shell jewellery. Standing in a small doorway, head tilted, watching with cautious hope. Full body, transparent background.
    show char_carmelita curious with dissolve

    narrator "You find a young woman watching you from the doorway of a smaller hut. She steps forward when you approach."

    carmelita "You are not from the island."
    narrator "It is not a question."

    menu:
        "Confirm it — tell her the truth about your mission":
            carmelita "My grandmother was one of the colonel's men. She told me everything — before Rosentos made her... quiet."
            carmelita "I know the channels. I know where the beach is. I know which side of the island the urns are on."
            carmelita "If you are truly going to end him — take me with you."
            $ party_carmelita = True
            narrator "Carmelita joins your party."
            jump second_village_decision
        "Ask what she knows about Rosentos before committing":
            carmelita "He does not eat. He does not age. He takes people in the night and they come back empty."
            carmelita "He is not a man. He has not been a man for a very long time."
            menu:
                "Ask her to guide you":
                    carmelita "Show me you mean to end him. Then yes."
                    $ party_carmelita = True
                    narrator "Carmelita joins your party."
                    jump second_village_decision
                "Thank her and move on":
                    jump second_village_decision

label meet_thut:
    # ASSET: Thut — lean angular man in his 30s, dark skin, rough traveller's clothes, a bone-handled long knife at his belt. Crouching near the platform edge, watching the water, not turning. Sullen and watchful. Full body, transparent background.
    show char_thut suspicious with dissolve

    narrator "A lean man crouches near the platform edge, watching the reeds. He does not turn when you approach."

    thut "You smell like trouble."
    thut "Rosentos' people don't smell like trouble. They smell like nothing. Like dead things that forgot to fall over."
    thut "You're different."

    menu:
        "Tell him exactly what you are here for":
            thut "Good."
            narrator "Just that. Then after a pause:"
            thut "I know every channel to that island. I've watched it from the reeds for three years."
            thut "I'll take you. But when it's done — Korat gets his village back. The people on the island get to go home. That's the price."
            $ party_thut = True
            narrator "Thut joins your party."
            jump second_village_decision
        "Ask what he knows about the island first":
            thut "Stone building in a clearing. Dirt urns on the path — big as a man. Or what used to be one."
            thut "Don't go near the urns in daylight. Whatever's in them sleeps then. You want to go at night."
            menu:
                "Ask him to guide you":
                    thut "If you're serious about killing it — yes."
                    $ party_thut = True
                    narrator "Thut joins your party."
                    jump second_village_decision
                "Thank him and move on":
                    jump second_village_decision

label second_village_decision:
    if korat_suspicious and not party_carmelita and not party_thut:
        narrator "Without allies in the village, Korat acts quickly. Before dawn, you are seized."
        jump captured_by_korat
    elif korat_suspicious:
        narrator "You sense Korat watching every move. Your new allies signal urgency — leave now, before he acts."
        jump isle_approach
    else:
        narrator "You spend the night in the hut. Just before dawn, you slip away with any companions who joined you."
        jump isle_approach

label captured_by_korat:
    # Music: captive, moving toward dread
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.0)

    # ASSET: Inside a dugout canoe at night — the party bound with vine rope in the bottom of the hull, native warriors paddling. Torchlight from a lead canoe. Dark water, dark sky. The dark silhouette of an island against a fading red sky in the distance.
    scene bg_canoe_captive with fade

    narrator "Korat's warriors move swiftly in the night. You are bound at wrists and ankles, lying in the hull of a dugout canoe."
    narrator "Vine rope. Tied by people who have done this before."
    
    if in_party("carmelita"):
        narrator "Carmelita is in the canoe beside yours. She meets your eyes briefly — then looks away."
    
    if in_party("thut"):
        narrator "Thut is not with you. Either he escaped in the confusion or he was never taken."
    
    narrator "Hours pass. The current changes — you feel it in the way the canoe moves. Faster. Deeper."
    narrator "The sky lightens to grey, then fades again. You have been travelling since before midnight."
    
    narrator "A canoe carrying most of your equipment overturns during the crossing. The warriors shout but do not stop."
    narrator "You arrive stripped of most of your gear."
    
    narrator "Ahead: dark trees against a fading red sky. An island."
    
    jump isle_rosentos_landing

label isle_approach:
    # Music: approaching dread, slow build
    $ play_scene_music("audio/mus_isle_rosentos.ogg", fadein=2.0)

    # ASSET: View from a canoe at twilight — a small sandy island ahead, dark tree silhouettes against deep orange and purple sky. A narrow gap in the reeds leading to a spongy beach. The trees look dense and tangled. The light is almost gone.
    scene bg_isle_approach with fade

    narrator "You find the island just as Fondalus described — just before sundown, a small hummock of sandy ground, dark silhouettes of trees against the dying light."
    narrator "A break in the reeds, just wide enough to pass through. Beyond it, a spongy beach and a trail winding up into the woods."

    if in_party("carmelita"):
        carmelita "We must not be here after full dark unless we are ready. Whatever happens — it must be done before dawn."
        narrator "She is quiet for a moment."
        carmelita "My grandmother saw this island. She came here with Rosentos. She left without him."
        carmelita "She spent the rest of her life pretending she didn't know what he became."
        narrator "Her voice is steady. Her hands are not."
        carmelita "I'm not going to pretend."

    if in_party("thut"):
        thut "The urns are on the path, not far from the beach. Don't touch them. Don't even look too long."
        narrator "He pauses. Then, without looking at you:"
        thut "I stayed away because I was afraid. Not of him. Of what I'd do if I went."
        thut "Korat lost his brother to the island. I watched from the reeds for three years because I couldn't face him knowing I was too scared to go myself."
        thut "This is the first time I've said that out loud."
        narrator "He poles the canoe into the gap. He does not look back."

    if has_item("Carved Bone Map Fragment"):
        narrator "The bone map fragment in your pack — a path through the swamp, an island marked with an X. You are here."

    jump isle_rosentos_landing

label isle_rosentos_landing:
    # ASSET: The island beach at dusk — dark sand, twisted trees, a rough trail leading into shadow. A lantern light moving down the trail from the woods toward the beach.
    scene bg_isle_beach with fade

    narrator "You land just after the sun sets. The beach is quiet."
    narrator "Then: a lantern. Someone coming down the trail."
    narrator "A man. About 35, lean and rangy. Battered, weather-beaten face — ugly but not unpleasant. Homemade clothes, a century out of date in their cut. A sword at his side, hands empty."

    # ASSET: Rosentos as he first appears — lean man in crude homemade clothing cut in a style a century out of fashion, carrying a lantern, sword at side but hands empty. Weather-beaten face. Friendly open expression that does not quite reach his eyes.
    show char_rosentos friendly with dissolve

    rosentos "Welcome! Welcome to the isle. I rarely have visitors — I hope the swamp gave you no trouble."
    rosentos "My name is Rosentos. My friends call me the Hideous One — a joke, you understand. My father named this island."

    if in_party("carmelita"):
        carmelita "His clothes. Look at his clothes. The cut — that is not this century."

    if in_party("thut"):
        thut "Don't meet his eyes. Whatever you do — don't hold his gaze."
    
    rosentos "Come. The cabin is not far. Follow me."
    
    # ASSET: A forest path on the island, night. Thick trees, roots crossing the path. Lantern carried by Rosentos ahead, barely illuminating a few feet. Deep shadow everywhere.
    scene bg_isle_path with fade
    
    narrator "He leads you up the trail. The lantern swings ahead, casting moving shadows."
    narrator "The air changes — warmer than the swamp, stiller. No insects. No birds."
    
    if in_party("thut"):
        narrator "Thut stays behind you. He watches the trees, the ground, the darkness between the trunks."
    
    if in_party("carmelita"):
        narrator "Carmelita walks with one hand on her blade. She has not spoken since the beach."
    
    narrator "The path curves. The trees thin. Ahead, the shape of a cabin."
    
    jump meet_rosentos

label meet_rosentos:
    # ASSET: A forest path on the island, night. Thick trees, roots crossing the path. Lantern carried by Rosentos ahead, barely illuminating a few feet. Deep shadow everywhere.
    scene bg_isle_path with fade

    rosentos "I must apologise for the accommodation. I live simply. But you are welcome to everything I have."
    rosentos "My father explored this island before me. He taught me everything. He has been gone for some time now."

    narrator "His manners. His speech. The cut of his clothing. Everything is almost right — and almost a century out of date."

    menu:
        "Ask him how long he has lived here":
            rosentos "All my life. It is all I know."
            narrator "He says this with such practiced ease that you almost believe it."
            jump rosentos_house
        "Ask about the cay-men in the clearing":
            rosentos "The little fellows? Harmless enough. We leave each other alone, mostly."
            narrator "He says this too smoothly. As if it is a prepared answer."
            jump rosentos_house
        "Look directly into his eyes":
            narrator "His gaze is remarkable. Intensely interesting. Strangely compelling. You find yourself wanting to hear more."
            $ rosentos_charmed = True
            rosentos "Come inside. You must be tired after the swamp."
            jump rosentos_house
        "Confront him about the colonel" if slough_vision_seen:
            narrator "You mention the colonel. The name drops like a stone."
            narrator "Rosentos freezes. The friendly mask cracks — not into fury, but into something older."
            rosentos "The swamp showed you."
            narrator "It is not a question."
            rosentos "He left me here. With the treasure I wouldn't share. With the questions I wouldn't stop asking."
            rosentos "The swamp offered me a choice. Die, or become something else."
            narrator "His voice is quiet. Almost human."
            rosentos "I chose survival. Everything after that... was the price."
            narrator "He looks at you. Really looks at you. For the first time, you see the man he was."
            rosentos "You came to kill me. I know."
            rosentos "Come inside. We can talk. Or you can try."
            $ rosentos_charmed = False
            $ rosentos_betrayed_known = True
            jump rosentos_house
        "Announce your purpose — you know what he is":
            $ rosentos_charmed = False
            narrator "The friendly mask drops instantly."
            rosentos_vamp "Then there is no reason to pretend."
            # ASSET: Rosentos transformed — red eyes blazing, fangs visible, the friendly mask completely gone. One hand slightly raised. Behind him in the darkness, the suggestion of vast bat wings.
            show char_rosentos_vamp revealed with dissolve
            jump combat_rosentos

label rosentos_house:
    # Music continues — ominous beneath a false surface
    $ play_scene_music("audio/mus_isle_rosentos.ogg", fadein=1.5)

    # ASSET: Interior of a well-kept wooden cabin — common room, table, chairs, shelves of objects. A single oil lamp. No windows anywhere. No fireplace. No cooking arrangement. No mirrors. Everything neat but wrong, like a stage set.
    scene bg_rosentos_cabin with fade

    narrator "A well-kept cabin in a small clearing. Inside: a common room, neat and clean."
    narrator "No windows. No fireplace. No cooking arrangement. No food. No mirrors."

    rosentos "The island grows very warm — windows only let in insects. The local food requires little preparation. I find I sleep better without mirrors."

    narrator "He has an answer for everything. And every answer arrives just slightly too quickly."

    narrator "He insists on refreshments. From beneath a bench he produces a clay jug — dust-covered, very old."
    narrator "When he pours, the liquid is wrong. Too thick. Too dark. He does not drink. He watches you."

    rosentos "My father laid this vintage down. I have few opportunities to share it."

    narrator "He talks. Too much. About his father — who taught him everything. About the island's climate — why he sleeps days. About visitors."
    rosentos "Not many. A few. They stayed."
    narrator "He smiles at the word 'stayed.' The smile does not move his eyes."

    if in_party("carmelita"):
        narrator "Carmelita's hand drifts to something hidden beneath her belt. Her knuckles are white."
        carmelita "He knew what I was going to say before I said it."

    if in_party("thut"):
        narrator "Thut has not entered the cabin. He 'checks the perimeter' and does not return."
        rosentos "Your friend prefers the outdoors. Wise. The air is fresher there."
    
    menu:
        "Accept the wine and keep him talking":
            narrator "You lift the cup to your lips. The smell is iron and old fruit. You drink — or seem to."
            rosentos "Good. Very good. My visitors always enjoy the vintage."
            narrator "He relaxes. The mask settles more comfortably."
            narrator "His tongue loosens with each question you ask. Casual admissions. Half-truths."
            narrator "The last visitors — how long ago? Difficult to say. Time moves strangely here."
            narrator "They stayed. They had nowhere else to go."
            narrator "His smile does not reach his eyes. He is watching you watching him."
            narrator "He knows you are not what you seem. But he is not ready to act yet."
            jump rosentos_house_investigation
        "Refuse the wine and press on the inconsistencies":
            $ rosentos_charmed = False
            narrator "You set the cup down without drinking."
            narrator "No fireplace. No cooking hearth. No mirrors — not one in the whole cabin."
            rosentos "You are very observant. I like that in a traveller."
            narrator "His tone does not change. But something behind his eyes does. He watches you more carefully now — predatory alertness beneath the smile."
            jump rosentos_house_investigation
        "Ask to see the sleeping arrangements — claim fatigue":
            rosentos "Of course. I have just the place."
            narrator "He gestures toward a door at the back of the cabin."
            narrator "Then pauses. His smile tightens almost imperceptibly."
            rosentos "But first — a drink. To seal our friendship."
            narrator "He pours two glasses. His hand is steady. His eyes are not."
            narrator "He is deciding something. You can see it in the way he measures you."
            
            menu:
                "Accept the drink":
                    narrator "You take the glass. His relief is visible — too visible."
                    narrator "The wine is rich. Warm. It spreads through your chest."
                    narrator "Your vision blurs at the edges. The room tilts."
                    narrator "The last thing you see is his smile — finally unguarded, finally hungry."
                    jump game_over_rosentos_charmed
                "Refuse politely — you've had enough wine":
                    rosentos "Of course. Forgive me. I forget that travellers are cautious."
                    narrator "He drinks both glasses himself. His composure returns."
                    narrator "But something has shifted. He knows you refused. He suspects you suspect."
                    rosentos "The night is young. Perhaps a walk instead? The island is beautiful by moonlight."
                    narrator "He reaches for the door. His hand brushes yours."
                    narrator "Ice cold. And then — nothing. He withdraws."
                    narrator "Perhaps not tonight. He seems to decide."
                    rosentos "Rest well, traveller. I will show you the island in the morning."
                    narrator "He withdraws to a back room. The door closes with a soft click."
                    narrator "Through the window, you watch him transform — mist flowing toward the far side of the island."
                    narrator "Toward the hollow."
                    jump slave_farm
        "Confront him directly — demand the truth":
            $ rosentos_charmed = False
            narrator "The facade drops."
            rosentos_vamp "You are either very brave or very foolish."
            show char_rosentos_vamp revealed with dissolve
            jump combat_rosentos

label rosentos_house_investigation:
    narrator "Rosentos retires late in the night. You hear a door — then silence. He is gone."

    menu:
    "Search the cabin for the secret door he used":
    narrator "You find it behind a shelf — a panel leading out the back of the cabin."
    narrator "You follow the trail in the dark."
    jump slave_farm_early
        "Go directly to the stone urns on the path — that is where he sleeps":
            if in_party("thut"):
                thut "Good. Move now while he is feeding. We have maybe an hour."
            jump rosentos_coffins
        "Follow him — shadow him through the island":
            narrator "You watch from cover as he moves toward the far side of the island. You follow silently."
            jump slave_farm

label slave_farm_early:
    # Music: creeping dread — arriving at the farm via the cabin's secret door
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.5)

    # ASSET: A trail through dense island undergrowth at night, leading from the cabin toward a swampy hollow. Moonlight barely visible through the canopy.
    scene bg_slave_farm with fade

    narrator "The trail from the cabin leads downhill through dense undergrowth, toward the sound of still water."
    narrator "The air changes — warmer, thicker, smelling of bodies and stagnant pools."
    narrator "Then the trees open and you see them."
    narrator "People. Fifteen or more, moving between dilapidated hovels with the slow grace of sleepwalkers."
    narrator "Their faces are peaceful. Their eyes are empty."

    if in_party("carmelita"):
        carmelita "These are the people who went missing. From our village. From the villages before ours."
        carmelita "He leads you straight to them. He is not ashamed. He thinks this is hospitality."

    if in_party("thut"):
        thut "He has fed from them for years. They cannot act against him. They cannot even think against him."

    jump slave_farm_encounter

label slave_farm:
    # Music: grim, quiet horror
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.5)

    # ASSET: A swampy hollow, moonlight on dark water. Dilapidated hovels, small gardens. Fifteen people moving with the slow, lethargic grace of sleepwalkers, faces peaceful and empty. Rosentos visible in the distance among them.
    scene bg_slave_farm with fade

    narrator "A hollow at the island's edge. Dilapidated hovels, small gardens. People moving in the moonlight with the slow grace of those who are no longer entirely themselves."
    narrator "Their faces are peaceful. Their eyes are empty."

    if in_party("carmelita"):
        carmelita "These are the people who went missing. From our village. From the villages before ours."

    if in_party("thut"):
        thut "He has fed from them for years. They cannot act against him. They cannot even think against him."

    jump slave_farm_encounter

label slave_farm_encounter:
    narrator "One of the enthralled approaches you. Not aggressive. Smiling. Vacant."
    narrator "A woman — or she was, once. Her movements are fluid and unhurried, like someone walking through a pleasant dream."

    narrator "'You're new,' she says. 'He'll like you. He likes new people. He liked me, once.'"
    narrator "She shows you her forearm. Bite marks. Old, healed, but many of them. Layered like years of bad weather."
    narrator "'He only takes a little. It's not so bad. You get used to the dreams.'"
    
    if in_party("carmelita"):
        narrator "Carmelita freezes."
        carmelita "That's... that's Maren. She was my neighbor. She went fishing one morning and never came back."
        carmelita "That was four years ago."
        narrator "Maren smiles at Carmelita. There is no recognition in her eyes."
        carmelita "She doesn't know me. She doesn't know anyone."
        narrator "Carmelita's hand goes to her blade. Then stops. She cannot do it."
    
    if in_party("thut"):
        narrator "Thut stands very still. He is looking past the woman — at a man sitting alone by a hovel."
        narrator "The man is old. Sunken cheeks. Empty eyes. He stares at his hands like he's forgotten what they're for."
        thut "That's Korat's brother. Venn."
        thut "He went fishing eight years ago. Korat never stopped waiting."
        narrator "Thut's voice is flat. Controlled. His hands are not."
        thut "I watched from the reeds for three years. I could have come sooner."
        narrator "He does not finish the thought. He doesn't need to."

    narrator "After feeding, Rosentos moves toward the path of stone urns. He transforms into mist and enters one before dawn."

    menu:
        "Try to wake them — shake them, shout, use holy symbols":
            narrator "You try everything. You shake them. You shout. You hold up what faith you carry."
            narrator "They smile through it. 'Don't worry,' they say. 'He'll be back soon. He always comes back.'"
            narrator "They cannot be freed while he lives. You see that now. The only mercy is the stake."
            $ slave_farm_witnessed = True
            jump farm_aftermath
        "Ask them where Rosentos sleeps":
            narrator "The woman tilts her head, still smiling."
            narrator "'In the big urns. The stone ones. He likes the third one best — it's sunny in the morning, he says.'"
            narrator "They betray him without knowing they betray him. The enthralled mind has no secrets because it has no self."
            $ slave_farm_betrayed = True
            jump farm_aftermath
        "Kill them quickly — mercy before the confrontation":
            narrator "You draw your blade. They do not run. They smile as you approach."
            narrator "'He'll bring me back,' one says. 'He brings everyone back.'"
            narrator "You do it anyway. When it's done, the silence is worse than the smiling."
            $ slave_farm_mercy_killed = True
            $ rosentos_charmed = False
            jump farm_aftermath
        "Leave them and move to the urns":
            narrator "You step around them. Their eyes follow you, still smiling."
            narrator "'Come visit,' they call after you. 'After you've met him. You'll understand then.'"
            jump farm_aftermath

label farm_aftermath:
    narrator "You walk away from the hovels. Behind you, voices call out — friendly, vacant, wrong."
    narrator "'Come back soon. He likes new people.'"
    
    if in_party("carmelita"):
        narrator "Carmelita is shaking. Not from fear. From rage."
        carmelita "They don't even know they're prisoners."
    
    if in_party("thut"):
        narrator "Thut's jaw is set. He does not look back."
        thut "The urns. Now."
    
    narrator "The path leads uphill. Stone shapes loom in the darkness."
    
    jump rosentos_coffins

label rosentos_coffins:
    # Music: tense, searching
    $ play_scene_music("audio/mus_explore_dark.ogg", fadein=1.0)

    # ASSET: A path at night, five massive stone urns — 5 feet in diameter, heavy smooth stone lids, featureless. Standing along the path like grey monuments. Torchlight from the party throws deep shadows. Ancient and threatening.
    scene bg_coffin_urns with fade

    narrator "Five stone urns stand along the path — each five feet across, topped with heavy smooth lids."
    
    if in_party("thut"):
        narrator "Thut walks to the first urn without hesitation. He places his hands on the stone."
        thut "Three years I watched these from the reeds. Three years I told myself someone else would do this."
        narrator "He pushes. The lid grinds. His muscles shake. Then it tips."
        thut "Empty. The first one is always empty. He's in one of the others."
        narrator "There is something in his voice that was not there before. Not fear. Determination."
    else:
        narrator "You approach the first urn. The stone is cold to the touch."

    if slave_farm_mercy_killed:
        narrator "A shriek rips through the island air. The nearest urn explodes outward — stone shards flying."
        narrator "Rosentos bursts from the grave earth, already transformed, already furious. He felt the deaths through the blood-link."
        rosentos_vamp "YOU KILLED THEM. THEY WERE MINE."
        show char_rosentos_vamp battle with dissolve
        jump combat_rosentos

    if slave_farm_betrayed:
        narrator "You go straight for the third urn — the one the thralls told you about. 'It's sunny in the morning,' she said."
        narrator "You tip it. Inside: Rosentos, dormant in a bed of dark earth. The enthralled mind had no secrets."
        jump rosentos_found_sleeping

    narrator "It takes four of you, ropes, and nearly an hour to tip the first urn. Empty. Only grave soil."

    menu:
        "Work through the remaining urns":
            $ raw, total, outcome = roll_d20(0)
            if outcome in ["critical_success", "success", "partial"]:
                narrator "You tip the second — empty. You try the third. The lid cracks."
                narrator "Inside: Rosentos, dormant in a bed of dark earth."
                jump rosentos_found_sleeping
            else:
                narrator "A column of mist erupts from inside the third urn before you can tip it. He is awake."
                show char_rosentos_vamp battle with dissolve
                jump combat_rosentos
        "Scatter the grave soil from all the urns — deny him refuge":
            narrator "You work quickly, scattering the earth from each urn."
            narrator "A shriek of mist erupts from one. Rosentos tears free, enraged — but with no grave earth, he cannot regenerate properly."
            $ combat_bonus_final = 2
            show char_rosentos_vamp battle with dissolve
            jump combat_rosentos

label rosentos_found_sleeping:
    narrator "He lies in the urn, pale and utterly still. This is the moment."
    narrator "The man who led two hundred soldiers to their deaths."
    narrator "The monster who has kept fifteen souls enslaved for a hundred years."
    
    if grisbaldos_oath_taken:
        narrator "You remember the oath. Grisbaldos' voice in the possessed companion's mouth: 'Find Rosentos. Slay him.'"
    
    narrator "You raise the stake."

    menu:
        "Drive it home — end it":
            narrator "The moment stretches. Then you drive it home."
            jump rosentos_destroyed_sleeping
        "Wake him first — you want him to know why he dies":
            if grisbaldos_oath_taken:
                narrator "You pull him from the earth. His eyes open — red and hateful."
                rosentos_vamp "You..."
                narrator "\"I swore an oath,\" you say. \"For Grisbaldos.\""
                show char_rosentos_vamp battle with dissolve
                jump combat_rosentos
            else:
                narrator "His eyes open. Red and hateful. Whatever you meant to say dies in your throat."
                show char_rosentos_vamp battle with dissolve
                jump combat_rosentos

label rosentos_destroyed_sleeping:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    hide char_rosentos_vamp with vpunch
    narrator "The body crumbles to ash in the grave earth. Just like that — a hundred years of evil, ended."
    $ rosentos_slain = True

    if grisbaldos_oath_taken:
        narrator "A cold wind passes through the island. Then absolute stillness. Somewhere, a soldier is finally at rest."

    if in_party("carmelita"):
        carmelita "It's done. Oh gods. It's actually done."

    if in_party("thut"):
        thut "Scatter his earth. Make certain. Then we go to the cay-men."
    
    narrator "You scatter every grain of grave soil. The silence after is total."
    narrator "The forest waits. Through the trees, the cay-men's clearing."
    
    jump caymen_village

label combat_rosentos:
    stop music fadeout 0.5
    $ play_scene_music("audio/mus_boss_rosentos.ogg", fadein=0.8)
    
    $ rosentos_round = 1
    $ rosentos_hits = 0
    $ rosentos_stance = "holding"
    $ rosentos_specials_used = []
    $ rosentos_grave_earth_scattered = False
    $ rosentos_charm_saved = False
    $ rosentos_dawn_timer = 0
    $ rosentos_closecall = False
    $ rosentos_intro_shown = False
    
    # Carry any pre-fight bonuses
    $ rosentos_bonus = combat_bonus_final
    $ combat_bonus_final = 0
    
    # Keep the current scene - don't override (urns vs path handled by calling label)
    show char_rosentos_vamp battle with dissolve
    
    rosentos_vamp "You come here to destroy me? A hundred years I have waited. You are not the first to try."
    
    jump combat_rosentos_round

label combat_rosentos_round:
    # --- ROUND OPENING ---
    if rosentos_round == 1 and not rosentos_intro_shown:
        narrator "Rosentos rises before you, fully revealed. Red eyes blaze in the darkness. Behind him, the suggestion of vast wings."
        $ rosentos_intro_shown = True
    
    # --- DAWN TIMER ---
    if rosentos_grave_earth_scattered:
        $ rosentos_dawn_timer += 1
        if rosentos_dawn_timer >= 3:
            narrator "The eastern sky is beginning to pale. Dawn approaches."
        elif rosentos_dawn_timer >= 5:
            jump combat_rosentos_dawn_victory
    
    # --- STANCE ---
    if rosentos_stance == "holding":
        narrator "You hold formation in the darkness. His eyes search for yours."
    elif rosentos_stance == "reeling":
        narrator "Blood runs from wounds. Rosentos presses harder."
    else:
        narrator "This is your last stand. His gaze is relentless."
    
    # --- REGENERATION CHECK ---
    if not rosentos_grave_earth_scattered and rosentos_round > 1:
        narrator "His wounds close as you watch. He regenerates."
    
    # --- COMPANION WARNINGS ---
    if rosentos_round == 1:
        if in_party("carmelita"):
            carmelita "His gaze — if he catches your eyes, it's over. Don't look directly at him!"
            $ rosentos_charm_bonus = True
        if in_party("thut"):
            thut "The heart. Everything else just slows him. Drive for the heart."
    
    # --- PLAYER CHOICE ---
    menu:
        "Attack directly — blades and holy symbols":
            $ bonus = 1
            narrator "You charge in, brandishing your weapons."
            if has_item("Sword +3: Armory of Morphos"):
                $ bonus += 2
                narrator "The sword finds its mark."
            jump combat_rosentos_attack
        
        "Scatter his grave earth — cut off regeneration":
            $ bonus = 0
            $ rosentos_grave_earth_scattered = True
            narrator "You split up, rushing to scatter the soil from the remaining urns."
            narrator "He shrieks as his connection to the earth severs."
            jump combat_rosentos_round
        
        "Hold defensive — avoid his gaze":
            $ bonus = 0
            $ rosentos_defensive = True
            narrator "You form a tight group, weapons raised, watching each other's backs."
            jump combat_rosentos_attack
        
        "Drive him toward the east — stall for dawn":
            $ bonus = -1
            $ rosentos_dawn_timer += 1
            narrator "You retreat toward the eastern treeline, buying time."
            jump combat_rosentos_attack
        
        "Have Carmelita shield you from his gaze" if in_party("carmelita") and "carmelita_gaze" not in rosentos_specials_used:
            $ rosentos_specials_used.append("carmelita_gaze")
            narrator "Carmelita steps close, her shoulder brushing yours. She keeps her body between you and Rosentos."
            narrator "She does not look at him. She watches his shadow instead."
            $ rosentos_charm_saved = True
            jump combat_rosentos_round
        
        "Have Thut identify his weakness" if in_party("thut") and "insight" not in rosentos_specials_used:
            $ rosentos_specials_used.append("insight")
            narrator "Thut studies Rosentos' movements."
            thut "When he transforms, there's a moment where he's vulnerable. Like a held breath."
            $ rosentos_thut_insight = True
            jump combat_rosentos_round
        
        "Use a holy symbol" if has_item("Holy Symbol"):
            $ bonus = 2
            narrator "You hold up your holy symbol. He flinches back."
            jump combat_rosentos_attack
        
        "Surrender to his gaze":
            narrator "His eyes hold yours. The world softens."
            jump game_over_rosentos_charmed

label combat_rosentos_attack:
    # --- APPLY MODIFIERS ---
    $ total_bonus = bonus
    
    if rosentos_bonus > 0:
        $ total_bonus += rosentos_bonus
        $ rosentos_bonus = 0
    
    # Companion bonuses
    if in_party("carmelita") and rosentos_round == 1:
        $ total_bonus += 1
        narrator "Carmelita watches for his gaze, calling warnings."
    
    if in_party("thut") and rosentos_round == 1:
        $ total_bonus += 1
        narrator "Thut identifies the vital points."
    
    if rosentos_charmed and rosentos_round == 1:
        $ total_bonus += 1
        narrator "His focus slips — you caught him off guard."
        $ rosentos_charmed = False
    
    if slave_farm_witnessed:
        $ total_bonus += 1
        narrator "The empty eyes of the thralls burn in your memory. Righteous fury steadies your hand."
        $ slave_farm_witnessed = False
    
    if rosentos_grave_earth_scattered:
        $ total_bonus += 1
        narrator "Without his grave earth, he cannot regenerate."
    
    if rosentos_thut_insight:
        $ total_bonus += 2
        $ rosentos_thut_insight = False
    
    # Stance penalty
    if rosentos_stance == "reeling":
        $ total_bonus -= 1
    elif rosentos_stance == "desperate":
        $ total_bonus -= 2
    
    # --- ROLL ---
    $ raw, total, outcome = roll_d20(total_bonus)
    narrator "You roll... [raw]!"
    
    # --- CHARM GAZE CHECK ---
    if not rosentos_defensive and not rosentos_charm_saved:
        $ charm_roll, charm_total, charm_outcome = roll_d20(-2)
        if charm_outcome in ["failure", "critical_blunder"]:
            narrator "His gaze catches yours. The world goes soft and warm."
            narrator "You do not want to fight. You want to stay."
            jump game_over_rosentos_charmed
    
    # --- RESOLVE ---
    if outcome == "critical_success":
        $ rosentos_hits += 2
        narrator "CRITICAL! Your blade finds his heart!"
        
    elif outcome == "success":
        $ rosentos_hits += 1
        narrator "A solid strike! Rosentos staggers back."
        
    elif outcome == "partial":
        narrator "You trade wounds. He heals — you don't."
        if rosentos_stance == "holding":
            $ rosentos_stance = "reeling"
        
    elif outcome == "failure":
        narrator "His claws rake across your chest. Blood sprays."
        if rosentos_stance == "holding":
            $ rosentos_stance = "reeling"
        elif rosentos_stance == "reeling":
            $ rosentos_stance = "desperate"
        
        # Charm check
        if not rosentos_defensive:
            narrator "His eyes hold yours for a moment too long."
        
    else:  # critical_blunder
        narrator "CRITICAL BLUNDER! He transforms — a massive wolf-shape."
        narrator "Fangs tear through your lines."
        $ rosentos_stance = "desperate"
    
    # --- RESET CLOSECALL ON SUCCESS ---
    if outcome in ["critical_success", "success"]:
        $ rosentos_closecall = False
    
    # --- CHECK VICTORY/DEFEAT ---
    if rosentos_hits >= 4:
        jump combat_rosentos_victory
    
    if rosentos_grave_earth_scattered and rosentos_dawn_timer >= 5:
        jump combat_rosentos_dawn_victory
    
    if rosentos_stance == "desperate" and outcome in ["failure", "critical_blunder"]:
        if not rosentos_grave_earth_scattered:
            if rosentos_closecall:
                jump game_over_rosentos
            else:
                $ rosentos_closecall = True
                narrator "You barely survive. Blood runs, but you stand. One more mistake ends this."
        else:
            narrator "Dawn is coming. You hold on."
    
    # --- ENEMY RESPONSE ---
    $ rosentos_round += 1
    
    if rosentos_round == 3:
        narrator "The fight is exhausting. Neither side has won yet."
    elif rosentos_round == 4:
        narrator "Rosentos snarls. 'You are persistent. The others were not.'"
    elif rosentos_round >= 5:
        narrator "How much longer can this go on?"
    
    jump combat_rosentos_round

label combat_rosentos_victory:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    hide char_rosentos_vamp with vpunch
    
    if rosentos_hits >= 5:
        narrator "Rosentos crumbles to ash before he can even scream. It is over that quickly."
    else:
        narrator "You press the advantage. A second strike. The ash settles on the dark soil."
    
    $ rosentos_slain = True
    
    if grisbaldos_oath_taken:
        narrator "A cold wind crosses the island. Then nothing. Grisbaldos is at peace."
    
    if in_party("carmelita"):
        narrator "Carmelita stands over the ash. She does not move."
        carmelita "A hundred years. And it ends like this."
        narrator "She looks at her hands. They are shaking."
        carmelita "My grandmother spent her whole life pretending she didn't know what happened here."
        carmelita "She couldn't face it. She couldn't face him."
        narrator "A long silence."
        carmelita "I faced him."
        narrator "She says it like she's trying to believe it. Maybe she will, in time."
    
    if in_party("thut"):
        thut "Scatter his grave earth. All of it. Make sure."
        narrator "Thut does it himself. Scooping the soil with his bare hands, scattering it to the wind."
        narrator "When it is done, his hands are black with earth. He stares at them."
        thut "Korat's brother. The others. They're free now."
        narrator "He does not say if that is enough."
    
    narrator "You scatter every grain of grave soil. When it is done, the island feels different."
    narrator "Lighter. As if something that was holding its breath has finally let go."
    
    narrator "Dawn is breaking. The forest is quiet."
    
    if in_party("carmelita"):
        carmelita "The cay-men's village is through the trees. The treasure is there."
    
    narrator "You walk through the forest. The trees part."
    
    jump caymen_village

label combat_rosentos_dawn_victory:
    $ play_scene_music("audio/mus_victory.ogg", fadein=1.0)
    
    narrator "The first grey light touches the sky."
    narrator "Rosentos stops. His expression changes — from fury to something like recognition."
    
    hide char_rosentos_vamp with dissolve
    narrator "He transforms to mist, fleeing toward his coffins."
    
    if rosentos_grave_earth_scattered:
        narrator "But there is nothing to return to. You scattered his grave earth."
        narrator "The mist circles. Then, as the sun crests the trees, it disperses."
    else:
        narrator "You pursue. You reach the coffins before he can reform."
        narrator "The stake finds his heart as the first true dawn breaks."
    
    $ rosentos_slain = True
    
    if grisbaldos_oath_taken:
        narrator "As the light touches the isle, something departs the air. A long-held breath, finally released."
    
    jump rosentos_cabin_loot

label rosentos_cabin_loot:
    narrator "With Rosentos destroyed, you search his cabin."
    narrator "Old journals from the expedition. Maps of the swamp. A chest of dusty coins."
    $ add_item("Rosentos' Journal")
    $ add_item("Dusty Coins (500 gp)")
    narrator "The journals speak of the cay-men, the treasure — and the creature he became."
    narrator "You leave the cabin. The island is quiet now. The trees open ahead."
    jump caymen_village

label caymen_village:
    # Music: alien, watchful, not hostile
    $ play_scene_music("audio/mus_caymen_village.ogg", fadein=1.5)

    # ASSET: A forest clearing on the island, packed dirt, a small compound of woven reeds and packed earth at the centre. Large dirt mounds with 1-foot openings boring into them. Groups of 8-to-12-inch reptilian humanoids stand in the clearing — some on the compound walls with tiny javelins, wearing bone and feather headdresses.
    scene bg_caymen_village with fade

    narrator "The trees open into a wide clearing. Packed dirt, a small compound of woven reeds at its heart. Large dirt mounds with one-foot openings."
    narrator "Small creatures stand in the clearing — no more than a foot tall, reptilian, intelligent eyes. Ten of them swarm the compound walls with tiny javelins the moment they see you."

    if in_party("carmelita"):
        carmelita "Cay-men. I have heard of them. They are clever. More clever than you think."

    if in_party("thut"):
        thut "Don't move. Don't raise your weapons. Let them come to you."

    menu:
        "Stand completely still — make no threatening moves":
            jump caymen_negotiation
        "Raise weapons and advance on the compound":
            jump caymen_fight

label caymen_fight:
    stop music fadeout 0.5
    play music "audio/mus_combat_low.ogg" fadein 0.8
    $ combat_bonus = 0

    narrator "The cay-men volley javelins from the walls. For every one you cut down, five more appear."

    menu:
        "Press through to the treasure building":
            $ combat_bonus += 0
            narrator "You push forward through the swarm."
        "Hold a defensive position — let them tire":
            $ combat_bonus += 1
            narrator "You form a circle, letting them exhaust their volleys."
        "Target the shaman — break their coordination":
            $ combat_bonus += 2
            narrator "You drive for the figure in the elaborate headdress."

    $ raw, total, outcome = roll_d20(combat_bonus)
    narrator "You roll... [raw]!"

    if outcome in ["critical_success", "success"]:
        narrator "You fight through. The cay-men scatter. The treasure compound is open."
        jump treasure_room
    elif outcome == "partial":
        narrator "You breach the compound with wounds. The cay-men scatter but have cost you dearly."
        jump treasure_room
    else:
        narrator "The cay-men hold. You fall back."
        narrator "They do not pursue. They watch from the walls."
        narrator "After a long silence, the shaman appears."
        jump caymen_negotiation

label caymen_negotiation:
    $ play_scene_music("audio/mus_caymen_village.ogg", fadein=1.0)

    # ASSET: Cay-men shaman on the compound wall — slightly larger than the rest, elaborate feather headdress, carved staff. Sharp, intelligent eyes. Other cay-men visible on the wall behind him.
    show char_caymen_shaman neutral with dissolve

    narrator "A figure appears on the compound wall. Older. An elaborate feather headdress, a carved staff."
    narrator "His eyes miss nothing."

    caymen_shaman "You stop. You no attack. This is good."
    caymen_shaman "You come from bad-man-no-man? From Rosentos-island?"

    caymen_shaman "We guard the Black Sage's word. Long before bad-man-no-man, before your colonel, before the villages on stilts."
    caymen_shaman "The orb is not power. It is a promise. Trinkla promised knowledge to those who would listen. Half true, half false — this is the price of hearing."
    caymen_shaman "We do not ask the orb questions. We keep others from asking. The last question asked here — before your kind came — was a thousand years ago."
    caymen_shaman "The asker wanted to know if he would be remembered. The orb said yes."
    caymen_shaman "The orb lied. Or told truth. We do not know. The asker is dust. We remember his name. That is all."

    menu:
        "Tell him Rosentos is destroyed" if rosentos_slain:
            caymen_shaman "..."
            caymen_shaman "Dead. Dead truly?"
            narrator "You describe what happened. The shaman's eyes are still and unreadable for a long moment."
            caymen_shaman "We know when bad-man-no-man is dead. We feel the island go quiet."
            caymen_shaman "You did this thing. We will not forget."
            jump caymen_rosentos_question
        "Say you have come for the treasure and mean no harm":
            caymen_shaman "Treasure is not yours. What you give us for treasure?"
            jump treasure_negotiation
        "Ask them about Rosentos":
            caymen_shaman "Bad-man-no-man. Very old. Not alive, not dead. He send warriors here many times. We lose many."
            caymen_shaman "We guard treasure from him. Long time. Very, very long."
            menu:
                "Tell him Rosentos is destroyed" if rosentos_slain:
                    caymen_shaman "Then deal is already done. You come."
                    jump caymen_rosentos_question
                "Ask what it would take to earn the treasure":
                    jump treasure_negotiation

label caymen_rosentos_question:
    menu:
        "Ask why they didn't destroy Rosentos themselves":
            caymen_shaman "We are small. He was not. Also — he did not ask the orb. He only wanted the gold."
            caymen_shaman "A man who does not seek knowledge is not our concern. A man who keeps others from seeking knowledge — this we guard against."
            caymen_shaman "Rosentos kept many from reaching us. This was... acceptable."
            narrator "The implication settles: they used him as a filter, letting him prey on the unworthy. A hundred years of complicity, measured in one-foot-tall pragmatism."
            jump treasure_deal
        "Say nothing more — proceed to the treasure":
            jump treasure_deal

label treasure_negotiation:
    caymen_shaman "You kill bad-man-no-man. Then treasure is yours. This is deal."

    menu:
        "Agree to the deal":
            if rosentos_slain:
                caymen_shaman "Then deal is already done. You come."
                jump treasure_deal
            else:
                narrator "You have not killed him yet. You have made the promise."
                narrator "The shaman nods and withdraws. You move to finish what you started."
                jump rosentos_coffins
        "Refuse — try to take the treasure without conditions":
            narrator "The shaman's eyes go flat."
            caymen_shaman "Then we fight."
            jump caymen_fight

label treasure_deal:
    $ play_scene_music("audio/mus_caymen_village.ogg", fadein=1.0)
    caymen_shaman "Come. We show you."
    narrator "The cay-men part. The shaman leads you through the compound gate."
    jump treasure_room

label treasure_room:
    # Music: wonder and ancient power
    play music "audio/mus_stinger_reveal.ogg"
    pause 2.5
    $ play_scene_music("audio/mus_isle_rosentos.ogg", fadein=1.5)

    # ASSET: Interior of a small ancient stone chamber — torches in iron brackets, floor swept clean. A pedestal shaped like a dragon's foot carved from a single enormous bone. On it: a large semitransparent sphere pulsating with living darkness from within. Around the base: coins and jewellery. The sphere dominates everything.
    scene bg_treasure_room with fade

    narrator "The treasure building is stone — ancient, predating the cay-men by centuries. The air inside is cool and still."
    narrator "In the centre of the chamber: a pedestal shaped like a dragon's foot, carved from a single bone. On it, a large semitransparent sphere — living darkness moves inside it, slow and pulsing."

    caymen_shaman "Essence-Orb of Trinkla. The Black Sage."
    caymen_shaman "Ask one question, each person, each moon. Half the time — true answer. Half the time — wrong answer. No way to know which."
    caymen_shaman "Power is bound to stone, pedestal, building. Take the stone — the power breaks. Return it — the power comes back."

    narrator "Around the base of the pedestal: coins, matched jewellery, and arms of exceptional quality."

    menu:
        "Take the Essence-Orb of Trinkla — dangerous knowledge is still knowledge":
            $ add_item("Essence-Orb of Trinkla")
            narrator "The sphere pulses coldly in your hands. Fifty percent true. Fifty percent absolutely wrong. No way to tell which."
            narrator "You carry the darkness with you as you leave."
            jump ending_victory
        "Take the gold and jewellery — practical wealth over uncertain power":
            $ add_item("Matched Jewellery Set (5 pieces)")
            $ add_item("Ring of Regeneration")
            narrator "Five thousand gold pieces. Five pieces of matched jewellery — each worth five hundred gold, or thirty-five hundred as a complete set."
            narrator "A ring of regeneration, deep red stone set in worked bone."
            jump ending_victory
        "Take the magical arms — a warrior's haul":
            $ add_item("Sword +3: Armory of Morphos")
            $ add_item("20 Arrows +1")
            $ add_item("Stone of Controlling Earth Elementals")
            narrator "A sword of exceptional quality — intelligent, Lawful, able to find traps, detect magic, and strike with extraordinary force."
            narrator "Twenty arrows of quality. A smooth grey stone that hums faintly."
            jump ending_victory
        "Leave it all here — honour the cay-men's long guardianship":
            narrator "You leave the chamber empty-handed. The shaman watches you from the doorway."
            caymen_shaman "You came for nothing you could carry. This has happened before. Once."
            caymen_shaman "The asker who wanted to be remembered — he left the treasure too. Eventually."
            caymen_shaman "You are welcome here. Always. We will remember your name."
            jump ending_honour

# ============================================================
# ENDINGS
# ============================================================

label ending_victory:
    $ renpy.hide_screen('inventory_screen')
    $ play_scene_music("audio/mus_ending_triumph.ogg", fadein=2.0)

    # ASSET: The island beach at dawn — dark sand, the party pushing off in canoes, dawn light breaking over the swamp behind them. The water glitters gold. The cay-men watch from the treeline in small groups.
    scene bg_isle_beach_dawn with fade

    narrator "You leave the Isle of Rosentos as the first true dawn breaks over the swamp."
    narrator "The water glitters gold. Behind you, the island is quiet."

    if in_party("carmelita"):
        carmelita "A hundred years. Can you imagine? A hundred years this place held in fear."

    if in_party("thut"):
        thut "Korat's village is free. The people on the slave farm will wake confused — but free. That matters more than any treasure."

    if grisbaldos_oath_taken:
        narrator "Somewhere, you feel certain, an old soldier's ghost has finally found rest."

    narrator "The Veteran's Tale is finished. The treasure is yours."

    jump isle_departure

label ending_honour:
    $ renpy.hide_screen('inventory_screen')
    $ play_scene_music("audio/mus_ending_triumph.ogg", fadein=2.0)

    # ASSET: Same dawn beach, but the party's posture is lighter — unburdened. The cay-men shaman stands at the waterline watching the canoes depart, expression one of solemn approval.
    scene bg_isle_beach_dawn with fade

    narrator "You leave the isle with empty hands and a clear conscience."
    narrator "The treasure remains in the stone chamber, in the care of those who guarded it for a century."
    narrator "The shaman watches from the waterline until you are lost in the reeds."

    if in_party("thut"):
        thut "Some things should stay where they are."

    if in_party("carmelita"):
        carmelita "We ended it. That is enough."

    narrator "You have destroyed the evil that haunted this place. That is enough."
    narrator "The Veteran's Tale is finished."

    jump isle_departure

label isle_departure:
    scene bg_isle_beach_dawn with dissolve
    
    narrator "You push the canoes into the dark water. The island recedes behind you."
    
    if in_party("carmelita"):
        narrator "Carmelita does not look back. Her grandmother's ghost can rest now."
    
    if in_party("thut"):
        narrator "Thut poles the canoe himself. He knows these channels by heart."
    
    narrator "The swamp swallows you. The island vanishes in the reeds."
    
    jump luln_return

# ============================================================
# EPILOGUE — THE RETURN
# ============================================================

label luln_return:
    # Music: reflective, the journey unwinding
    $ play_scene_music("audio/mus_explore_river.ogg", fadein=2.0)

    # --- The River Journey Back ---
    # ASSET: View from a raft poling through the swamp channels, but now the light is morning gold. The water is calm. The reeds part easily. The feeling is of a place exhaling.
    scene bg_swamp_channel with fade

    narrator "The return through the swamp is nothing like the approach."
    narrator "The channels feel known now, the water less threatening. Where the current fought you before, it carries you. Where the mist pressed close, it parts."

    if rosentos_slain:
        narrator "The swamp feels lighter. As if something vast and patient has stopped holding its breath."

    if has_item("Essence-Orb of Trinkla"):
        narrator "The orb pulses in your pack. You feel it through the canvas — a slow, cold heartbeat that is not yours. It has not spoken. You have not asked."

    narrator "Three days of poling through channels that no longer confuse. The rafts move easily. Nobody runs a fever."

    # --- Korat's Village ---
    # ASSET: The second village on stilts, but now in daylight — people moving freely, children visible, the atmosphere entirely changed.
    scene bg_second_village with fade

    narrator "You pass through Korat's village at midday. The change is immediate."

    if in_party("thut"):
        narrator "Thut steps onto the platform and walks to his old hut without a word. He emerges carrying a small bundle — something wrapped in oilcloth."
        narrator "He does not explain. He does not need to."

    if in_party("carmelita"):
        narrator "Carmelita speaks to the villagers in their own tongue. You watch their faces change as she translates the news."
        narrator "One woman sits down slowly on the platform edge. Another laughs — a strange, broken sound, like a door opening after years."

    if not in_party("carmelita") and not in_party("thut"):
        narrator "The villagers move differently — no longer flinching at shadows, no longer watching the western treeline."
        narrator "Sleepwalkers from the island have returned, confused and blinking. Some sit at the edge of the platform, staring at their hands."
        narrator "A weight has lifted. They do not have words for it yet."

    # --- The Plain Crossing ---
    $ play_scene_music("audio/mus_explore_river.ogg", fadein=1.5)

    # ASSET: The flat grassy plain, now peaceful under open sky. No ambush, no tension — just grass and sky and the road home.
    scene bg_bandits_plain with fade

    if bandit_chief_killed:
        narrator "The bandit chief's territory. Grass has already begun to grow over the trampled site where you fought. Insects hum where men bled."
        narrator "His horse is nowhere to be seen. The plains are quiet."
    else:
        narrator "The bandit chief's territory. He does not appear. But once, from a distant rise, you see a lean black horse watching."
        narrator "It stands motionless against the sky for a long moment. Then it turns and is gone."

    # --- Grisbaldos' Grove ---
    if grisbaldos_oath_taken and rosentos_slain:
        # ASSET: The oak grove in daylight — birds, sunlight through leaves, the cairn stones warm and moss-covered. Peaceful.
        scene bg_grisbaldos_grove with fade

        if grisbaldos_contradiction_known:
            narrator "The oak grove is just a grove now. Birds. Sunlight. The cairn stones are warm under your hand."
            narrator "You still don't know if he was a martyr or a coward. But you know he was angry. And you know he's gone now."
        else:
            narrator "The oak grove is quiet. Sunlight. Birds. The cairn has not moved. But the air is different."
            narrator "A soldier's ghost, finally at rest. Whatever he was in life, he held on long enough to see the end."

    if grisbaldos_cursed and rosentos_slain:
        scene bg_grisbaldos_grove with fade

        narrator "The oak grove. You did not plan to stop, but your feet bring you here."
        narrator "The ghost appears one last time — faint in the daylight, barely a shimmer between the branches."
        narrator "It nods. Once. Then it dissipates like morning fog, and the grove is just a grove."

    # --- Luln Arrival ---
    $ play_scene_music("audio/mus_luln_tavern.ogg", fadein=2.0)

    # ASSET: The Luln tavern interior, same as the opening — but now the light is warmer, the fire livelier. Fondalus sits at the same table, same cup. He looks up as you enter.
    scene bg_luln_tavern with fade
    show char_fondalus neutral with dissolve

    narrator "The tavern in Luln. The same smoky warmth. The same low beams."
    narrator "Fondalus is there, same table, same cup. He looks up when you enter. He knows without asking."

    fondalus "You found him, then."

    menu:
        "Tell him everything — the truth, all of it":
            fondalus "I buried three men under that oak. Grisbaldos made four, if you count the ghost."
            if rosentos_slain:
                fondalus "A hundred years. And you ended it in what — a week?"
                narrator "He shakes his head. Not in disbelief. In something older than that."
            jump luln_return_final
        "Say nothing — let silence tell the story":
            narrator "You sit down across from him. You do not speak. He studies your face."
            fondalus "That bad. Or that good. I can never tell with travellers."
            jump luln_return_final

label luln_return_final:
    show char_fondalus weary with dissolve

    if has_item("Essence-Orb of Trinkla"):
        fondalus "That thing in your pack. I recognise the description. The Black Sage. We were warned about her, back then."
        fondalus "You're carrying a question with no right answers."
        narrator "He says it without judgement. He has carried worse."

    if not has_item("Essence-Orb of Trinkla") and not has_item("Matched Jewellery Set (5 pieces)") and not has_item("Sword +3: Armory of Morphos"):
        fondalus "You went all that way for nothing?"
        narrator "A pause."
        fondalus "...No. Not nothing. I know what you left behind. I left things too."

    if in_party("carmelita"):
        narrator "Carmelita sits at the end of the table. She does not drink. She watches the door — the habit of someone used to watching for danger."
        narrator "She will not go back to the village. That much is clear. Whatever comes next, it will not be the swamp."

    if in_party("thut"):
        narrator "Thut stands near the tavern door, not quite inside, not quite out. He watches the road."
        narrator "He said he would leave once the village was free. He has not left yet."

    narrator "Fondalus buys the round. Or you do. It does not matter who pays."
    narrator "The fire settles. The candles gutter. Outside, the road leads back to a world that knows nothing of swamps, or vampires, or orbs that lie half the time."

    narrator "The clink of cups. The story is over."

    jump ending_screen

# ============================================================
# ENDING SCREEN
# ============================================================

label ending_screen:
    $ renpy.hide_screen('inventory_screen')
    scene black with fade
    
    pause 1.0
    
    narrator "THE END"
    
    pause 1.0
    
    # --- COMPANION EPILOGUES ---
    if in_party("carmelita"):
        narrator "CARMELITA"
        if rosentos_slain:
            narrator "She never returned to the swamp village. She found work in Luln as a guide for river expeditions."
            narrator "She writes to her grandmother's surviving relatives — the ones who still remember the name Rosentos. She tells them it's over. She doesn't say how she knows."
            narrator "Sometimes, at night in the tavern, someone asks about the swamp. She tells them it's dangerous. She tells them to stay away."
            if slave_farm_mercy_killed:
                narrator "She never speaks of Maren. But on quiet nights, she wakes reaching for a blade that isn't there."
                narrator "She tells herself it was mercy. Some nights, she almost believes it."
            elif slave_farm_witnessed:
                narrator "She writes to Maren's family. She tells them Maren is at peace. She does not say what peace meant on that island."
            else:
                narrator "She does not mention the island. She does not mention Maren. She does not mention that she faced the thing her grandmother couldn't."
            narrator "But she does not avoid it either. And when the wind comes from the west, she does not flinch."
        else:
            narrator "She returned to the village. She speaks of the isle only when asked, and then only in fragments."
            narrator "She keeps a small lock of something grey and brittle in a locket she never opens."
            narrator "She never married. She never left the swamp again."
            narrator "On the anniversary of the expedition, she walks to the waterline and stares west."
            narrator "She never says what she's looking for."
    
    if in_party("thut"):
        narrator "THUT"
        if rosentos_slain:
            narrator "He returned to the village only long enough to settle his affairs. Then he left again."
            if slave_farm_witnessed or slave_farm_mercy_killed:
                narrator "But first, he told Korat about Venn."
                narrator "He told him what the island did to his brother. What was left of him. How he smiled."
                narrator "Korat listened without speaking. Then he went to the waterline and did not come back for a long time."
                narrator "When he returned, he asked Thut to leave. Thut understood."
            narrator "He told Korat's successor he was going north. He told you he was going to find a quiet place."
            narrator "Months later, a messenger brings you a small wrapped package — no note, no return address."
            narrator "Inside: a single river stone, polished smooth by swamp water. It is warm to the touch, and stays warm."
            narrator "You never see Thut again. But sometimes, when you're near water, you feel watched. Not with malice. With something like peace."
        else:
            narrator "He vanished before the return journey reached the plain. His tracks ended at the riverbank."
            narrator "Carmelita said he told her he was done with the outside. She did not explain what she meant."
            narrator "Years later, a trader from the deep swamp brings word: a lean man lives alone on an island far upriver. He speaks to no one."
            narrator "The trader says the man watches the reeds. Always the reeds. As if waiting for something to come out of them."
            narrator "Nothing ever does."
    
    # --- FATE SUMMARY ---
    if rosentos_slain:
        narrator "ROSENTOS: Destroyed. His grave earth scattered, his coffin breached. The swamp will remember."
        if slave_farm_mercy_killed:
            narrator "THE THRALLS: Dead by your hand before the confrontation. Fifteen people who will never wake up."
            narrator "You told yourself it was mercy. The swamp does not judge. But it remembers."
        elif slave_farm_witnessed:
            narrator "THE THRALLS: Freed when Rosentos died. They woke confused and afraid."
            narrator "Some found their way home. Some could not remember where home was."
            narrator "Maren sat by the waterline for three days before someone from the village recognized her."
        else:
            narrator "THE THRALLS: You left them smiling in the dark. When Rosentos died, the smiles stopped."
            narrator "They woke to silence. To emptiness. To the sudden, terrible weight of memory."
            narrator "Some found their way back. Some did not want to."
    else:
        narrator "ROSENTOS: He endures. The coffin still holds. The swamp still breathes."
        narrator "But the treasure is gone from the isle. And that is something."
        if slave_farm_witnessed:
            narrator "THE THRALLS: They continue as before. Smiling. Dreaming. Feeding him."
            narrator "They do not know you came. They do not know you left."
    
    if grisbaldos_oath_taken:
        narrator "GRISBALDOS: The oath is fulfilled. Whatever he was — martyr or coward — his restless century is done."
        narrator "The oak grove is just a grove now. Sunlight and birds and the slow work of moss."
    elif grisbaldos_cursed:
        narrator "GRISBALDOS: The oath was broken. But he faded anyway, his anger worn thin by time."
        narrator "The oak grove still feels heavy. Some weights never fully lift."
    
    # --- ROSENTOS' TRUTH ---
    if slough_vision_seen and rosentos_slain:
        narrator "ROSENTOS' TRUTH: You knew what he was before you killed him. The betrayal. The colonel's blade in his back. The swamp's offer."
        narrator "He chose survival. Everything after was the price."
        narrator "You killed him anyway. Because survival for him meant death for others."
        narrator "The truth did not make it easier. But it made it honest."
    elif rosentos_slain:
        narrator "ROSENTOS' TRUTH: You killed a monster. You did not know the man."
        narrator "Perhaps it is better that way. Monsters are simpler."
    
    # --- TREASURE'S WEIGHT ---
    if has_item("Essence-Orb of Trinkla"):
        if grisbaldos_oath_taken:
            narrator "THE TREASURE: You swore an oath and took the orb. Fifty percent true. Fifty percent lies. You carry questions with no right answers."
            narrator "Grisbaldos would have understood. Or maybe not. Ghosts are simpler than the living."
        elif grisbaldos_cursed:
            narrator "THE TREASURE: You refused the oath but took the orb anyway. The ghost watches. It will always watch."
            narrator "The orb pulses in the dark. It asks its own questions. You have not answered yet."
        else:
            narrator "THE TREASURE: The orb waits. You have not asked it anything yet."
            narrator "You will. Eventually. Everyone does."
    elif has_item("Matched Jewellery Set (5 pieces)"):
        if grisbaldos_oath_taken:
            narrator "THE TREASURE: Gold and jewels. A fortune by any measure. You swore the oath and claimed the reward."
            narrator "A soldier's debt paid in coin. Grisbaldos would have approved."
        elif grisbaldos_cursed:
            narrator "THE TREASURE: You refused the oath but took the treasure anyway. Gold is heavier than you remember."
            narrator "The ghost watches from the oak. It will always watch."
        else:
            narrator "THE TREASURE: Gold and jewels. The expedition's reward. Fondalus will not ask what it cost."
    elif has_item("Sword +3: Armory of Morphos"):
        if grisbaldos_oath_taken:
            narrator "THE TREASURE: A sword that finds traps, detects magic, strikes with terrible force. You swore the oath and claimed the blade."
            narrator "It will serve you well. Or it will serve itself. Intelligent weapons are like that."
        elif grisbaldos_cursed:
            narrator "THE TREASURE: You refused the oath but took the sword anyway. It hums in the dark. It knows things."
            narrator "The ghost watches. The blade watches back."
        else:
            narrator "THE TREASURE: A sword of power. It will serve you well. Or it will serve itself."
    else:
        if grisbaldos_oath_taken:
            narrator "THE TREASURE: You left it all. The cay-men keep what they guarded."
            narrator "You swore the oath. That was enough. The treasure was never the point."
        elif grisbaldos_cursed:
            narrator "THE TREASURE: You left it all. But you refused the oath too."
            narrator "The ghost fades. The treasure stays. What was the point?"
        else:
            narrator "THE TREASURE: You left it all. The cay-men keep what they guarded."
            narrator "Some things are worth more where they are."
    
    # --- FINAL WORDS ---
    pause 1.0
    
    narrator "The Veteran's Tale is told. The treasure of the Hideous One — whatever form it takes — has been claimed."
    narrator "The swamp still waits. New roads will be built. New expeditions will go west."
    narrator "But for now, the tavern in Luln is warm. The fire is low. The cups are full."
    narrator "And somewhere in the dark water, something vast and patient has stopped dreaming."
    
    pause 2.0
    
    scene black with fade
    
    pause 1.0
    
    narrator "Treasure of the Hideous One"
    narrator "Based on AC2 by David Cook"
    narrator "A D&D Expert Mini-Adventure for Character Levels 4–7"
    
    pause 2.0
    
    $ renpy.full_restart()

# ============================================================
# ART ASSET MANIFEST
# ============================================================
# TARGET: Image generator input
# FORMAT: 1920x1080 PNG for backgrounds | Transparent PNG ~600px tall for characters
# STYLE NOTE: Dark colonial swamp fantasy illustration, painterly and atmospheric.
#             Muted greens, muddy browns, deep blacks with amber lantern and cold
#             supernatural highlights. The swamp is a living presence made visible.
#             Inspired by classic D&D Expert Set box art — gritty, grounded, no anime.
#             Key contrast: warm amber safety vs. cold green/blue supernatural threat.
#
# BACKGROUNDS:
#
#   bg_luln_tavern.png
#   Prompt: Interior of a rough frontier tavern, low smoke-blackened wooden beams,
#           tallow candles and rush lights on long communal tables, a barely-alive fire
#           in a stone hearth. Clay mugs and cups scattered. An aged soldier sits
#           centre-frame, forearms on table, deeply weathered. Warm amber-orange
#           candlelight, deep shadow throughout.
#   Mood: humble, worn, carrying an old story
#   Lighting: warm amber from candles and hearth, deep surrounding shadow
#
#   bg_luln_road.png
#   Prompt: Flat frontier road heading west from a small settlement, morning mist
#           burning off, dry grass on both sides, the road a dirt track curving toward
#           a distant river glinting in hazy light. Party silhouettes from behind.
#           Wide overcast sky, slightly hazy.
#   Mood: departure, open, cautious
#   Lighting: pale morning sun from the right, mist diffusing the light
#
#   bg_riverbank_hydra.png
#   Prompt: Muddy river bank, tall yellowing reeds, grey-green river water. Ten dark
#           shapes floating near the shore that could be crocodile heads — but their
#           spacing is wrong. Something massive lurks just below the surface. Late
#           flat afternoon light. Danger implicit in the stillness.
#   Mood: deceptive, ancient danger, false calm
#   Lighting: flat grey-green afternoon light, no warm tones
#
#   bg_grisbaldos_grove.png
#   Prompt: A rise above a river bend, ancient oak trees forming a dense canopy,
#           dappled late afternoon light through the leaves. Thick gnarled roots.
#           Centre: a rotting stump surrounded by scattered mossy stones — remnants
#           of a collapsed cairn. A shaft of light falls on the stump.
#   Mood: ancient, mournful, something unresolved
#   Lighting: dappled afternoon light, one shaft of light on the stump
#
#   bg_grisbaldos_grove_night.png
#   Prompt: Same oak grove, night. Moonlight barely penetrating the canopy.
#           Pale green light drifts between the trees in balls. A shaft of cold
#           light rises from the earth of the cairn — a ghost is beginning to form,
#           transparent, tattered uniform, arms outstretched.
#   Mood: terrifying, cold, supernatural
#   Lighting: near darkness, pale moonlight, cold green supernatural light
#
#   bg_bandits_plain.png
#   Prompt: Five-foot-tall yellowing grass rising above a steep riverbank, dustclouds
#           in the air. A figure in demonic-looking black polished armour with metal
#           studs rises from the grass, holding a glittering black blade. A lean black
#           horse with phosphorescent-outlined eyes stands beside it. The grass around
#           the horse's hooves smokes faintly.
#   Mood: ambush, theatrical menace, false drama
#   Lighting: harsh afternoon sun, dusty air, bright and merciless
#
#   bg_swamp_entrance.png
#   Prompt: The edge of a river dissolving into swampland — reeds as far as the eye
#           can see, dark open water pools between them. Two crude log rafts at the
#           waterline loaded with supplies. Cold flat grey sky.
#   Mood: bleak, isolated, the point of no return
#   Lighting: overcast flat grey light, no warm tones
#
#   bg_swamp_channel.png
#   Prompt: View from a raft poling through a narrow swamp channel, towering reeds
#           on either side, dark still water below, the channel curving into deeper
#           shadow ahead. A dead tree leans over the water. Utterly isolated.
#   Mood: claustrophobic, disorienting, oppressive
#   Lighting: overcast diffused light, deep shadow under the reeds
#
#   bg_slough_despair.png
#   Prompt: Bleak open swamp pool surrounded by standing reeds in a ring. At the
#           centre of the dark water: a perfect hemisphere of absolute darkness,
#           roughly 15 feet across. No light enters it, no light reflects from it.
#           The reeds are utterly still.
#   Mood: existential dread, supernatural wrongness, void
#   Lighting: flat overcast light except the hemisphere which is pure void
#
#   bg_burned_village.png
#   Prompt: Ruined swamp village on stilts at a spongy hummock's edge. Hut frames
#           open to the sky, roofs missing, floors sagging and splintered. The wood
#           is fire-blackened throughout. Reeds clog the waterways. Grey, dead.
#   Mood: desolate, long abandonment, death
#   Lighting: flat grey overcast, no warmth anywhere
#
#   bg_burned_village_night.png
#   Prompt: Same village at night. Dark water below the stilts. From the black water,
#           fifteen waterlogged ghouls are climbing the stilts in absolute silence —
#           grey-white and bloated, dark water streaming from their flesh.
#   Mood: horror, silence, the dead rising
#   Lighting: near darkness, faint moonlight, the ghouls barely visible
#
#   bg_second_village.png
#   Prompt: A small lake of open water in the swamp with six small huts on sapling
#           stilts, woven branch platforms, crude reed roofs. A mongrel dog leaps
#           between platforms. Half-rotted dugout canoes tied to stilts. Furtive
#           movements near the hut doors. Afternoon light on water.
#   Mood: inhabited, fearful, cautious
#   Lighting: weak afternoon light, warm but tired, reflecting off the water
#
#   bg_second_village_interior.png
#   Prompt: Interior of a large hut on stilts — reed matting, a barely-lit fire pit,
#           crude wooden furniture. Daylight from an open doorway showing the lake and
#           other huts beyond. Simple, worn, lived-in and frightened.
#   Mood: enclosed, uncertain, a place under someone else's power
#   Lighting: dim firelight from the pit, daylight from the doorway
#
#   bg_canoe_captive.png
#   Prompt: Inside a dugout canoe at night — bound party in the hull, native warriors
#           paddling. Torchlight from a lead canoe. Dark water, dark sky. In the
#           distance, a dark island silhouette against a fading red sunset.
#   Mood: captive, helpless, dread of destination
#   Lighting: torchlight from lead canoe, last of twilight on horizon
#
#   bg_isle_approach.png
#   Prompt: View from a canoe at twilight, approaching a small sandy island. Dark
#           tree silhouettes against deep orange and purple sky. A narrow gap in the
#           reeds leading to a spongy beach. The trees look dense and wrong.
#   Mood: arrival, threshold, something irreversible ahead
#   Lighting: deep twilight, orange-purple sky, dark silhouettes
#
#   bg_isle_beach.png
#   Prompt: The spongy beach of the island at dusk — dark sand, twisted trees, a
#           rough trail leading up into shadow. A warm lantern light moves down the
#           trail from the woods toward the beach. The warmth of it is somehow wrong.
#   Mood: false welcome, the predator approaching
#   Lighting: last of twilight from above, warm lantern light from the trail below
#
#   bg_isle_path.png
#   Prompt: A forest path on the island at night. Thick trees, roots crossing the
#           path. A lantern carried by a figure ahead illuminates only a few feet.
#           Deep shadow everywhere. Close and disorienting.
#   Mood: enclosed, disorienting, the host is not safe
#   Lighting: single lantern, everything else dark
#
#   bg_isle_path_night.png
#   Prompt: Same path, but a vampire is revealed — red eyes gleaming in the darkness,
#           fangs visible, a massive bat-shape shadow rising behind the figure. The
#           lantern dropped and illuminates the path from below.
#   Mood: revelation, horror, confrontation
#   Lighting: lantern on ground illuminating from below, cold moonlight from above
#
#   bg_rosentos_cabin.png
#   Prompt: Interior of a well-kept wooden cabin — common room, table, chairs,
#           shelves. A single oil lamp. No windows. No fireplace. No mirrors.
#           Everything too neat, like a stage set rather than a home. Wrong.
#   Mood: false safety, uncanny, something deeply wrong
#   Lighting: single oil lamp warm circle, deep shadow beyond
#
#   bg_slave_farm.png
#   Prompt: A swampy hollow at night, moonlight on dark water. Dilapidated hovels,
#           small gardens. Fifteen people moving with the slow grace of sleepwalkers,
#           faces peaceful, eyes empty. A man in old-fashioned clothes moves among
#           them. Disturbing in its quietness.
#   Mood: violation, the banal horror of total control
#   Lighting: pale cold moonlight reflecting off the water
#
#   bg_coffin_urns.png
#   Prompt: A path at night, five massive stone urns — 5 feet across, heavy smooth
#           lids, featureless. Lined along the path like grey monuments. Torchlight
#           from the party throws deep shadows behind them. Ancient.
#   Mood: gravity, the weight of what sleeps inside
#   Lighting: torchlight, deep shadow, cold stone texture
#
#   bg_caymen_village.png
#   Prompt: A wide forest clearing, packed dirt, a small compound of woven reeds at
#           the centre. Large dirt mounds with one-foot openings. Groups of one-foot-
#           tall intelligent reptilian humanoids — some on compound walls with tiny
#           javelins, wearing bone and feather headdresses. Alien and watchful.
#   Mood: alien, defended, ancient guardianship
#   Lighting: daylight, dappled through forest canopy
#
#   bg_treasure_room.png
#   Prompt: Interior of a small ancient stone chamber — torches in iron brackets.
#           A pedestal shaped like a dragon's foot carved from a single enormous bone.
#           On it: a large semitransparent sphere with living darkness pulsing inside.
#           Coins and jewellery at its base. The sphere dominates the room.
#   Mood: ancient power, dangerous knowledge, wonder
#   Lighting: torch brackets on walls, the sphere emitting a cold dark pulse of its own
#
#   bg_isle_beach_dawn.png
#   Prompt: The island beach at dawn — dark sand, canoes pushing off, the party
#           visible from behind. Dawn light breaking over the swamp behind the island.
#           The water glitters gold. Cay-men watch from the treeline.
#   Mood: triumph, release, dawn after darkness
#   Lighting: golden dawn light from the east, the island behind in silhouette
#
# CHARACTERS:
#
#   char_fondalus_neutral.png
#   Prompt: Aged soldier in his 60s, deeply weathered face, grey stubble, heavy
#           dark brown wool travelling cloak. Seated at a table, forearms resting,
#           clay cup in both hands. Full body, dark fantasy illustration.
#   Expression: grave, world-weary, honest
#   Pose: seated, leaning forward, cup in both hands
#   Background: transparent
#
#   char_fondalus_weary.png
#   Prompt: Same aged soldier, same clothes. He has pushed a rough parchment map
#           across the table. He looks done — relieved to have told the story.
#   Expression: weary, unburdened, distant
#   Pose: seated, leaning back, one hand on the map on the table
#   Background: transparent
#
#   char_grisbaldos_ghost_neutral.png
#   Prompt: Ghost of a soldier from a century ago — transparent, tattered military
#           uniform in an old style, arms outstretched, head lolling to one side.
#           Thick dark rope burns at the neck. Pale green glow throughout.
#   Expression: vacant, yearning, reaching
#   Pose: standing, arms outstretched, head lolling sideways
#   Background: transparent
#
#   char_grisbaldos_ghost_demanding.png
#   Prompt: Same ghost. Now pointing directly at the viewer — arm fully outstretched,
#           finger levelled. Expression cold, accusatory, implacable. The green light
#           is brighter and steadier.
#   Expression: cold, accusatory, demanding
#   Pose: standing, one arm pointing directly at viewer
#   Background: transparent
#
#   char_korat_fearful.png
#   Prompt: Gaunt village chief, hollow-eyed, emaciated, 40s. Ceremonial feathers
#           and a bone necklace over simple woven cloth. He is on his knees, forehead
#           pressed nearly to the floor. Terrified submission.
#   Expression: terrified submission, hollow-eyed
#   Pose: kneeling, kowtowing, forehead nearly to the floor
#   Background: transparent
#
#   char_carmelita_curious.png
#   Prompt: Young woman of mixed ancestry, 20s, bright dark eyes, simple woven cloth
#           dress, shell jewellery at neck and wrists. Standing in a doorway, head
#           tilted slightly, watching with cautious hope. Full body.
#   Expression: curious, cautious, hopeful
#   Pose: standing in a doorway frame, arms at sides, slightly turned
#   Background: transparent
#
#   char_thut_suspicious.png
#   Prompt: Lean angular man, 30s, dark skin, rough traveller's clothes, bone-handled
#           long knife at his belt. Crouching slightly, head turned sidelong to regard
#           the viewer. Sullen and watchful. Not hostile — assessing.
#   Expression: sullen, watchful, assessing
#   Pose: crouching slightly, head turned sidelong, arms loose
#   Background: transparent
#
#   char_rosentos_friendly.png
#   Prompt: Lean man in apparent 30s, crude homemade clothing cut in a style a
#           century out of fashion. Carrying a lantern, sword at his side, hands
#           otherwise empty. Weather-beaten face, rather ugly but not unpleasant.
#           Friendly open expression that does not fully reach his eyes.
#   Expression: friendly, slightly too smooth, not-quite-right
#   Pose: standing, lantern in one hand, other slightly raised in greeting
#   Background: transparent
#
#   char_rosentos_vamp_revealed.png
#   Prompt: Same man, same clothes — but eyes are red and gleaming, fangs visible
#           between parted lips. The friendly mask completely gone. The lantern
#           dropped. Behind him in shadow, the suggestion of great bat wings forming.
#   Expression: cold, predatory, ancient, revealed
#   Pose: standing, arms slightly spread, fangs visible
#   Background: transparent
#
#   char_rosentos_vamp_battle.png
#   Prompt: Rosentos in full vampire mode — red eyes blazing, fangs bared, one hand
#           raised in a gesture of power. Behind him a massive bat shadow rises. He
#           is partially transforming between man and monster.
#   Expression: furious, predatory, a hundred years of patience broken
#   Pose: combat stance, one hand raised, partially transformed
#   Background: transparent
#
#   char_caymen_shaman_neutral.png
#   Prompt: A cay-men shaman — one foot tall, intelligent reptilian humanoid, older
#           than the others. Elaborate headdress of bone and long feathers, a carved
#           wooden staff. Standing on a wall, regarding the viewer with sharp eyes.
#   Expression: watchful, intelligent, weighing every word
#   Pose: standing on a wall, staff in one hand, regarding the viewer
#   Background: transparent
#
# ============================================================

# ============================================================
# MUSIC MANIFEST
# ============================================================
# TARGET: Music generator / composer input
# FORMAT: OGG preferred | Loopable unless marked [STING]
# MASTER TONE: Dark colonial swamp fantasy. Acoustic instruments dominate:
#              low cello, bass lute, bone flute, sparse hand drum, low brass.
#              The swamp is a living presence — humid, threatening, ancient.
#              Rosentos has a leitmotif: a descending minor cello line, elegant
#              and deeply wrong. The supernatural is cold, not loud.
#
# TRACKS:
#
#   mus_luln_tavern.ogg
#   Used at: veterans_tale
#   Description: Warm, slightly melancholy tavern ambience. A safe place but
#                shadowed by an old story. Like a folk song in a minor key played
#                by someone who knows how it ends.
#   Tempo: slow-medium
#   Instrumentation: acoustic lute, low cello, hand drum, quiet fiddle
#   Loop: yes
#   Duration: 2 min
#
#   mus_explore_river.ogg
#   Used at: luln_departure, hydra_riverbank (ambient), bandits_plain (pre-encounter),
#            combat_hydra_win, combat_hydra_partial, combat_bandit_win, combat_bandit_partial
#   Description: Open travel music, flat plains and river country. Forward-moving
#                but with an undertone of things that could go wrong.
#   Tempo: medium
#   Instrumentation: lute, travelling drum, light strings, occasional horn
#   Loop: yes
#   Duration: 2 min
#
#   mus_explore_haunted.ogg
#   Used at: grisbaldos_grove, grisbaldos_ghost_encounter (after stinger)
#   Description: The oak grove at dusk and night. Wind through old trees, something
#                unresolved in the air. A haunting melody that almost sounds like
#                a lullaby.
#   Tempo: slow
#   Instrumentation: solo bone flute, sparse low strings, wind texture
#   Loop: yes
#   Duration: 2.5 min
#
#   mus_stinger_ghost.ogg
#   Used at: grisbaldos_ghost_encounter (reveal)
#   Description: The ghost appears — cold, sudden, a shaft of pale green light
#                rising from the earth. Something stops the heart.
#   Tempo: — [STING]
#   Instrumentation: high strings glissando, choir breath, cold reverb tail
#   Loop: no
#   Duration: 5 sec
#
#   mus_combat_mid.ogg
#   Used at: combat_hydra, combat_bandit_chieftain
#   Description: Urgent, driving mid-intensity combat. Natural world danger, not
#                supernatural. Fast rhythm, aggressive strings, forward pressure.
#   Tempo: fast
#   Instrumentation: driving strings, percussion, bass lute, horn stabs
#   Loop: yes
#   Duration: 90 sec
#
#   mus_combat_low.ogg
#   Used at: combat_ghouls, caymen_fight
#   Description: Grim, grinding combat. Not glamorous — survival. Slow driving beat,
#                dissonant undertones, the feeling of fighting in the dark.
#   Tempo: medium-fast
#   Instrumentation: low strings, bone drum, dissonant brass
#   Loop: yes
#   Duration: 90 sec
#
#   mus_stinger_despair.ogg
#   Used at: slough_of_despair
#   Description: A hemisphere of void in the world. Not a monster — something worse.
#                Silence broken by a single discordant chord, then nothing.
#   Tempo: — [STING]
#   Instrumentation: full silence broken by one dense discordant cluster chord
#   Loop: no
#   Duration: 4 sec
#
#   mus_explore_swamp.ogg
#   Used at: swamp_entrance_path, swamp_journey, burned_village (approach),
#            second_village_approach, combat_ghouls_win, combat_ghouls_partial,
#            combat_ghouls_lose, combat_ghouls_critical_fail
#   Description: The swamp as a living presence — oppressive, humid, vast. Something
#                always moving just out of sight. Slow and disorienting.
#   Tempo: slow
#   Instrumentation: low drone strings, bone flute, water sounds, distant bird calls
#   Loop: yes
#   Duration: 3 min
#
#   mus_explore_dark.ogg
#   Used at: slough_of_despair (after entering), burned_village, slave_farm,
#            rosentos_coffins, rosentos_house_investigation, captured_by_korat
#   Description: Active dread — you are in the wrong place and you know it. For
#                searching undead places and approaching known danger.
#   Tempo: slow
#   Instrumentation: bass cello, sparse percussion, dissonant held notes
#   Loop: yes
#   Duration: 2.5 min
#
#   mus_second_village.ogg
#   Used at: second_village_korat, second_village_talk, meet_carmelita, meet_thut
#   Description: A village alive but broken. People who were free once. Subdued
#                hope under oppressive fear. A gentle theme twisted wrong.
#   Tempo: slow-medium
#   Instrumentation: lute, low drum, solo voice humming in a minor key
#   Loop: yes
#   Duration: 2 min
#
#   mus_stinger_reveal.ogg
#   Used at: treasure_room (entering)
#   Description: The treasure chamber. Wonder and ancient danger together. The
#                sphere pulsating. Something enormous in a small room.
#   Tempo: — [STING]
#   Instrumentation: deep resonant bell, choir breath, slow swell
#   Loop: no
#   Duration: 6 sec
#
#   mus_isle_rosentos.ogg
#   Used at: isle_approach, isle_rosentos_landing, meet_rosentos, rosentos_house,
#            rosentos_house_investigation, combat_rosentos_win, combat_rosentos_partial,
#            treasure_room (after stinger)
#   Description: The island's theme — Rosentos' leitmotif. A descending minor cello
#                line, elegant and deeply wrong. Beautiful in an unsettling way.
#   Tempo: slow
#   Instrumentation: solo cello descending minor line, sparse harpsichord, low strings
#   Loop: yes
#   Duration: 3 min
#
#   mus_boss_rosentos.ogg
#   Used at: combat_rosentos
#   Description: Boss fight — Rosentos fully revealed. A hundred years of predatory
#                patience turned violent. Relentless, aristocratic horror.
#   Tempo: fast
#   Instrumentation: church organ, driving strings, choir, distorted harpsichord
#   Loop: yes
#   Duration: 2 min
#
#   mus_caymen_village.ogg
#   Used at: caymen_village, caymen_negotiation, treasure_deal, caymen_fight (ambient)
#   Description: The cay-men — alien, ancient, small but deeply serious. Strange
#                music from a strange people. Not threatening. Simply other.
#   Tempo: medium
#   Instrumentation: bone instruments, unusual percussion, clicking rhythms, low flute
#   Loop: yes
#   Duration: 2 min
#
#   mus_victory.ogg
#   Used at: combat_hydra_critical_win, combat_ghouls_critical_win,
#            combat_rosentos_critical_win, rosentos_destroyed_sleeping
#   Description: Victory sting — brief, bright, earned.
#   Tempo: — [STING]
#   Instrumentation: brass fanfare, single percussion strike, held chord
#   Loop: no
#   Duration: 5 sec
#
#   mus_ending_triumph.ogg
#   Used at: ending_victory, ending_honour
#   Description: The adventure is over. Not a triumphant march — a quiet dawn.
#                Earned peace. The light returning after a very long darkness.
#   Tempo: slow, building gently
#   Instrumentation: full ensemble building from solo lute: strings, choir,
#                    light percussion, ending on a long held high note
#   Loop: no
#   Duration: 3 min
#
# ============================================================
