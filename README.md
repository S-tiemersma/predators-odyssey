# Predator’s Odyssey

Welcome to **Predator’s Odyssey**, a small prototype that lays the groundwork for a much larger open‑world monster RPG.  This repository contains a simple command‑line game written in Python along with a design document outlining the long‑term vision for the project.

The intent of this prototype is twofold:

1. **Demonstrate core mechanics** – Absorption of enemy abilities, basic combat, and skill fusion.
2. **Serve as a learning exercise** – If you're new to programming or game development this project provides a structured yet approachable starting point.  The code is heavily commented to explain what’s happening.

Feel free to run the game, read through the code, and expand upon it.  There’s plenty of room for growth as you become more comfortable with Python and game development concepts.

## Getting Started

### Requirements

* Python 3.8 or later.
* No external libraries are required; everything is built with the Python standard library.

### Running the Prototype

1. Clone or download the repository (if you’re reading this via a ZIP or on a different computer, skip this step).
2. Navigate into the project folder and run:

```bash
python src/main.py
```

3. Follow the on‑screen prompts.  Your goal is to survive successive battles, absorb new skills, and experiment with fusions.  When you reach the surface the prototype ends.

## Directory Layout

| Path | Purpose |
|---|---|
| `src/` | Contains all game code.  Start with `main.py`. |
| `design_doc.md` | A high‑level game design document describing the full vision of **Predator’s Odyssey**. |

## Extending the Prototype

This repository only scratches the surface of what “Predator’s Odyssey” could be.  Here are some ideas for how you might expand it:

* Replace the command‑line interface with a graphical user interface (e.g. using `pygame` or Godot when you feel comfortable installing external libraries).
* Implement different biomes with distinct enemy types.
* Add a save system so that you can return to your monster later.
* Introduce AI adventurer parties that adapt to your abilities.

The design document in this repo goes into much greater detail about the long‑term vision.  Use it as inspiration and a road map as your skills grow.
