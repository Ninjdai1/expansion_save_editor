Expansion save editor (Yet another gen 3 pokemon save editor)
========

The goal of this save editor is to provide an easy way to edit a pokeemerald-expansion-based rom hack's save file by directly parsing the rom file to fetch the available pokemon, moves, items or abilities dynamically in order to support fakemons aswell as custom moves, items and abilities out of the box.

> [!NOTE]  
> As of the 16th of January, an implementation of an "API" in pokeemerald-expansion is being discussed on the RHH discord, in [this thread](https://discord.com/channels/419213663107416084/1196199792343265381). If the API ends up working and merged into the expansion, ESE will be obsolescent, as the API would allow cross-version compatibility for external tools. I've therefore stopped working on ESE until the API gets merged/refused, at which point I'll update this page. If the API gets merged, this repository will become archived for future reference. If no one writes a python interpreter for the API before me, I'll create a library for this purpose, and I'll remake ESE using the library.

Usage
-------------
ESE's only requirement is python3.

To use ESE, have `pokeemerald.gba` and `pokeemerald.sav` in the same directory as main.py, and run
```
python main.py
```
Current state
-------------
ESE is currently able to read all the species, abilities, moves and items in a romhack based on 1.7.2 / upcoming of [pokeemerald expansion](https://github.com/rh-hideout/pokeemerald-expansion) as long as it doesn't change the used structs' structure.
It is also able to export the current party of the save to competitive format.

Roadmap
-------------
The current goals are:
* Forward compability (allow reading from the expansion's structs even if they are changed using offsets stored in RHH header)
* Working save edition

Also planned, but not WIP:
* PKHEX-compatible vanilla mons export (.pk*)

Not planned:
* Backwards-compatibility with versions of the expansion older than 1.8, as important features and bugfixes required for ESE to work are only available starting from 1.8 (namely, https://github.com/rh-hideout/pokeemerald-expansion/pull/3980, https://github.com/rh-hideout/pokeemerald-expansion/pull/3861, https://github.com/rh-hideout/pokeemerald-expansion/pull/3831)

Feel free to open issues/PRs that are outside of the stated goals ! If a feature is said not planned, that only means I don't plan to work on it, but I can still accept a PR !

Credits
-------------
ads04r for theire [Gen3Save python library](https://github.com/ads04r/Gen3Save/tree/master) on which a lot of the code is based/reused.

Bulbapedia's [save data structure page](https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)) which taught me a lot about the save data structure in pokeemerald
