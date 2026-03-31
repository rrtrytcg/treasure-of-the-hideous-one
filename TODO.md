# TODO - Treasure of the Hideous One

## Completed
- [x] A1. Denouement scenes (ending screen, companion epilogues, fate summary)
- [x] A2. Transitions (14 transition fixes across all scenes)
- [x] B. Companion arcs (Carmelita + Thut depth, 9 new moments)
- [x] C. Make Slave Farm Matter (epilogue consequences, Carmelita/Maren, Thut/Venn)
- [x] D. Midpoint Reversal (slough of despair vision, Rosentos betrayal reveal)
- [x] Combat system overhaul (multi-round, game over endings, D&D stats)

## Remaining Story Improvements

### E. Meaningful Ending Divergence
- [x] Ending should vary based on key choices (oath, slave farm, treasure)
- [x] Currently only 2 endings (take treasure vs leave treasure)
- [x] Add: oath fulfilled + treasure taken = different epilogue
- [x] Add: mercy-killed thralls = different epilogue

## Art & Assets (ComfyUI pipeline ready)
- [ ] Generate `bg_bandits_plain.png` — plain grass landscape, no figures
- [ ] Generate `char_bandit_chief.png` — demonic humanoid + black warhorse, centered
- [ ] Generate remaining sprites/backgrounds per ASSET comments (see all `# ASSET:` comments in `treasure_of_the_hideous_one.rpy`)

## Polish
- [ ] Smoke test all paths (`python tools\smoke_playthrough.py`)
- [ ] Check all menu choices lead somewhere valid
- [ ] Verify companion conditional blocks work with both/one/none
- [ ] Review game over screens for consistency

## New Features (Future)
- [ ] Cay-men village side quest
- [ ] Swamp random encounters
- [ ] Inventory screen enhancements
- [ ] Save/load system polish
