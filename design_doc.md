# Predator’s Odyssey – Design Document

## 1. High‑Level Overview

**Predator’s Odyssey** is a single‑player action–RPG where you begin life as a fragile monster hatchling deep within a colossal dungeon.  Instead of looting swords and armour, you devour fallen foes to steal their abilities and mutate your own body.  As you ascend through the dungeon’s layers and emerge onto the surface, the difficulty shifts from a struggle for survival to a test of mastery against the world’s apex predators.  The player’s choices determine whether they will become the ecosystem’s tyrant, protector, or something in between.

This document lays out a broad vision for the game and offers a road map for future development.  The accompanying Python prototype implements a few foundational mechanics in a text‑only environment.

## 2. Core Mechanics and Loops

### 2.1 Predator Loop

1. **Defeat** – Engage hostile creatures in turn‑based or action combat.
2. **Absorb** – After winning, consume the enemy to extract one of its innate skills.
3. **Analyse** – Evaluate your growing list of abilities; decide which to keep, swap out, or sacrifice for mutations.
4. **Evolve** – Combine or fuse abilities into bespoke spells or physical alterations (e.g. “Thread Shot” + “Acid Glob” ⇒ “Acidic Web”).  Mutations can change your stats, shape, or traversal options.

### 2.2 On‑the‑Fly Spell Weaving

Any two learned skills may be fused to produce a new power.  These fusions are not purely combinatorial; they are hand‑authored to feel impactful and unique.  At launch there are 25 curated fusions.  For example:

| Components | Result | Description |
|---|---|---|
| Thread Shot + Acid Glob | **Acidic Web** | Fires a sticky web that deals damage over time and slows victims. |
| Water Jet + Electric Current | **Conductive Spray** | A stream of water that electrocutes multiple foes. |
| Fireball + Wind Burst | **Flaming Cyclone** | A fiery vortex that pulls in enemies while burning them. |

### 2.3 Resource‑Free Casting

Early skills consume environmental resources: you need water to shoot Water Jets or rocks to create Stone Bullets.  Late‑game casting conjures elements from pure mana at the cost of significant energy, but the player never manages hunger or thirst.

### 2.4 Reactive Factions & Nemeses

The overworld is populated by adventurer parties, tribes of monsters, and legendary beasts.  AI factions adapt to your actions: if you frequently hunt goblins, their shamans may learn your Acidic Web and use it against you.  Provoking a powerful nemesis triggers a quest line culminating in climactic battles.

### 2.5 Open‑World Freedom

There are no timers forcing progression.  Difficulty is geographic: the depths of the dungeon and “Legend Mark” zones on the surface hold the most dangerous foes, while the surrounding wilderness is forgiving and ideal for experimentation.

## 3. Progression Outline

1. **Birth (Layer ‑10)** – Learn movement and the basics of absorption.  Obtain your first two skills.
2. **Mid‑Layers (Layers ‑9 to ‑2)** – Encounter mini‑bosses guarding unique skills.  Unlock Tier‑1 mutation (choose between Acid Slime form or Web Spinner form).  Experiment with fusions and defeat procedurally generated parties.
3. **Surface Breakout (Layer ‑1)** – Crash through a crumbling crypt and see daylight.  Normal wildlife and low‑level adventurers pose little threat.  Feel powerful.
4. **World Tier Discovery** – “Legend Mark” zones reveal enormous titans that still dwarf you.  Their defeat requires careful build crafting and multiple fusions.
5. **End Game** – Decide whether to exterminate other apex predators, coexist, or even reshape the ecosystem by challenging the world’s guardian beasts.  Unlock Tier‑3 mutation states with dramatic visual morphs.

## 4. Content Targets (Version 1.0)

* **Biomes** – 4 surface biomes (e.g. lush forest, desert, volcanic region, frozen mountains) plus the multi‑layer dungeon beneath.
* **Skills** – 70 base skills spread across Water, Wind, Earth, Fire, Venom and Lightning categories.
* **Fusions** – 25 hand‑crafted fusions that feel game‑changing.
* **Evolution Tree** – 3 tiers with 27 nodes total, each accompanied by visual changes to the player’s monster body.
* **Bosses** – 12 story bosses and procedurally remixed “Rift” encounters for replayability.
* **Playtime** – 40–80 hours to achieve 100 % completion, yet drop‑in–drop‑out friendly.

## 5. Prototype Implementation Notes

The provided prototype in `src/main.py` is deliberately minimalistic.  It runs in a terminal and illustrates the predator loop by letting you fight enemies, absorb skills, and perform simple fusions.  Combat resolution is extremely simplified to keep the code readable.

Future implementations might migrate to a real game engine such as **Godot** (which is free and beginner‑friendly) or **Unity**.  When you’re ready to graduate from text‑only, consider experimenting with `pygame` or the Godot API to render sprites, handle input, and build a more dynamic combat system.

## 6. Glossary

* **Skill** – A discrete ability (e.g. Fireball, Thread Shot).  Can be active (cast on command) or passive (constant buff).
* **Fusion** – A unique ability created by combining two base skills (e.g. Acidic Web).
* **Mutation** – A permanent alteration to your monster’s body that unlocks new traversal options, resistances, or attack types.
* **Legend Mark** – Zones on the surface map that house optional end‑game bosses.
