"""
Predator’s Odyssey – Command‑line Prototype
==========================================

This script implements a very simple, text‑based version of the core gameplay loop
described in the design document.  You begin as a newborn monster at the bottom
of a dungeon.  Each turn you can fight a random enemy, absorb one of its
abilities, and optionally fuse two of your skills into a more powerful one.

The code is written for clarity, not efficiency.  Comments throughout explain
what each section does.  Feel free to modify and extend this code to your
liking!

To play, run:
    python src/main.py

Note: This game uses Python’s built‑in `input()` function for user input.
"""

import random
from typing import Dict, List, Tuple


class Skill:
    """Represents a skill or ability that can be learned or absorbed."""

    def __init__(self, name: str, description: str, category: str) -> None:
        self.name = name
        self.description = description
        self.category = category

    def __str__(self) -> str:
        return f"{self.name} ({self.category}) – {self.description}"


class FusionTable:
    """Defines all valid fusions between pairs of skills.

    The key is a frozenset of two skill names.  The value is a Skill
    representing the fused ability.  This structure allows fusions to be
    commutative (A+B and B+A produce the same result).
    """

    def __init__(self) -> None:
        self._table: Dict[frozenset[str], Skill] = {}
        self._register_default_fusions()

    def _register_default_fusions(self) -> None:
        """Populate the fusion table with a handful of curated fusions."""
        def add(skill_a: str, skill_b: str, result: Skill) -> None:
            self._table[frozenset([skill_a, skill_b])] = result

        # Example fusions from the design document
        add(
            "Thread Shot",
            "Acid Glob",
            Skill(
                name="Acidic Web",
                description="Fires a sticky web that deals damage over time and slows victims.",
                category="Venom",
            ),
        )
        add(
            "Water Jet",
            "Electric Current",
            Skill(
                name="Conductive Spray",
                description="A stream of water that electrocutes multiple foes.",
                category="Water/Lightning",
            ),
        )
        add(
            "Fireball",
            "Wind Burst",
            Skill(
                name="Flaming Cyclone",
                description="A fiery vortex that pulls in enemies while burning them.",
                category="Fire/Wind",
            ),
        )
        # You can expand this table with additional curated fusions.

    def fuse(self, skill_a: Skill, skill_b: Skill) -> Skill | None:
        """Return the fusion of two skills if it exists, otherwise None."""
        key = frozenset([skill_a.name, skill_b.name])
        return self._table.get(key)


class Creature:
    """Base class for both the player and enemies."""

    def __init__(self, name: str, max_health: int, skills: List[Skill]) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.skills: List[Skill] = skills[:]

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - amount)

    def attack_power(self) -> int:
        """
        Compute a simple attack power based on the number of skills and a random
        factor.  In a real game each skill would contribute its own damage,
        elemental types, etc.  Here we simply multiply the count of skills by
        a random number between 1 and 3.
        """
        return len(self.skills) * random.randint(1, 3)

    def absorb_skill(self, skill: Skill) -> None:
        """Learn a new skill (if you don't already know it)."""
        if skill.name not in {s.name for s in self.skills}:
            self.skills.append(skill)


class Player(Creature):
    """Represents the player's monster character."""

    def __init__(self) -> None:
        # Start with a small amount of health and two random basic skills
        starting_skills = random.sample(BASIC_SKILLS, 2)
        super().__init__(name="You", max_health=15, skills=starting_skills)
        self.layer = -10  # Start at the bottom layer of the dungeon

    def evolve(self) -> None:
        """Placeholder for evolution logic.  You could expand this to modify
        health, add passive buffs, or visually transform the creature.
        """
        # For now we simply increase the max health and heal slightly
        self.max_health += 5
        self.health = self.max_health
        print("\n[EVOLUTION] You feel your body changing, your skin thickens and your vitality grows!\n")

    def choose_skill_to_absorb(self, enemy: Creature) -> Skill:
        """Prompt the player to pick one of the enemy's skills to absorb."""
        unique_skills = [s for s in enemy.skills if s.name not in {sk.name for sk in self.skills}]
        if not unique_skills:
            # If no unique skills are available, return a random one anyway
            return random.choice(enemy.skills)
        while True:
            print("Which skill would you like to absorb?")
            for i, skill in enumerate(unique_skills, start=1):
                print(f"  {i}. {skill}")
            try:
                choice = int(input("Enter the number of the skill: "))
                if 1 <= choice <= len(unique_skills):
                    return unique_skills[choice - 1]
            except ValueError:
                pass
            print("Invalid selection.  Please choose a valid number.")

    def choose_fusion(self, fusion_table: FusionTable) -> None:
        """
        Allow the player to fuse two of their skills.  Shows valid fusion outcomes
        and performs the fusion if desired.  If no valid fusion exists, the
        function returns without changing anything.
        """
        if len(self.skills) < 2:
            print("You need at least two skills to attempt a fusion.\n")
            return
        # Build list of all possible pairs and their fusions
        pairs: List[Tuple[int, int, Skill]] = []
        for i in range(len(self.skills)):
            for j in range(i + 1, len(self.skills)):
                s1, s2 = self.skills[i], self.skills[j]
                fusion = fusion_table.fuse(s1, s2)
                if fusion:
                    pairs.append((i, j, fusion))
        if not pairs:
            print("None of your current skills can be fused together right now.\n")
            return
        print("Possible fusions:")
        for idx, (i, j, result) in enumerate(pairs, start=1):
            print(f"  {idx}. {self.skills[i].name} + {self.skills[j].name} ⇒ {result.name}")
        while True:
            try:
                choice = input("Enter the number of the fusion to perform (or press Enter to cancel): ")
                if choice == "":
                    print("Fusion cancelled.\n")
                    return
                choice_int = int(choice)
                if 1 <= choice_int <= len(pairs):
                    i, j, result_skill = pairs[choice_int - 1]
                    # Remove the two skills and add the fusion
                    old_names = (self.skills[i].name, self.skills[j].name)
                    # Remove higher index first to avoid reindexing issues
                    for index in sorted([i, j], reverse=True):
                        del self.skills[index]
                    self.absorb_skill(result_skill)
                    print(f"\nYou fused {old_names[0]} and {old_names[1]} into {result_skill.name}!\n")
                    return
            except ValueError:
                pass
            print("Invalid choice.  Please enter a valid number or press Enter to cancel.")


class Enemy(Creature):
    """Represents a randomly generated enemy encountered in the dungeon."""

    def __init__(self, player_layer: int) -> None:
        # Difficulty and health scale slightly with the player’s current layer
        name = random.choice(["Goblin", "Slime", "Spider", "Bat", "Kobold", "Imp"])
        max_health = 5 + max(0, -player_layer - 10) * 2  # deeper layers have tougher foes
        # Enemies know one or two random skills
        num_skills = random.randint(1, 2)
        skills = random.sample(BASIC_SKILLS, num_skills)
        super().__init__(name=name, max_health=max_health, skills=skills)


# Define a pool of basic skills that enemies and the player may start with.
# In a complete game these would be loaded from a database or JSON file.
BASIC_SKILLS: List[Skill] = [
    Skill(name="Fireball", description="Hurl a small orb of fire.", category="Fire"),
    Skill(name="Thread Shot", description="Shoot a sticky thread that briefly snares foes.", category="Wind"),
    Skill(name="Acid Glob", description="Spit a glob of acid that corrodes armour.", category="Venom"),
    Skill(name="Water Jet", description="Send a focused jet of water at high pressure.", category="Water"),
    Skill(name="Electric Current", description="Emit a surge of electricity.", category="Lightning"),
    Skill(name="Stone Shard", description="Launch a sharp shard of rock.", category="Earth"),
    Skill(name="Wind Burst", description="Release a concussive blast of air.", category="Wind"),
    Skill(name="Shadow Sneak", description="Momentarily fade into shadows, avoiding harm.", category="Dark"),
]


def battle(player: Player, enemy: Enemy) -> bool:
    """
    Run a very simple battle between the player and an enemy.

    Each turn both combatants deal damage based on their attack power.
    The function returns True if the player wins and False otherwise.
    """
    print(f"\n--- A wild {enemy.name} appears! ---")
    print(f"It has {enemy.health} HP and knows: {', '.join(s.name for s in enemy.skills)}\n")
    while player.is_alive() and enemy.is_alive():
        # Player attacks first
        player_damage = player.attack_power()
        enemy.take_damage(player_damage)
        print(f"You hit the {enemy.name} for {player_damage} damage.  (Enemy HP: {enemy.health}/{enemy.max_health})")
        if not enemy.is_alive():
            print(f"\nYou defeated the {enemy.name}!\n")
            return True
        # Enemy retaliates
        enemy_damage = enemy.attack_power()
        player.take_damage(enemy_damage)
        print(f"The {enemy.name} hits you for {enemy_damage} damage.  (Your HP: {player.health}/{player.max_health})")
        if not player.is_alive():
            print("\nYou have been defeated...")
            return False
    return False


def play_game() -> None:
    """Main game loop."""
    print("Welcome to Predator’s Odyssey!\n")
    fusion_table = FusionTable()
    player = Player()
    print("You awaken in the depths of a dark dungeon.  You feel strangely hungry...\n")
    # Main loop continues until player reaches the surface or dies
    while True:
        print(f"Current Layer: {player.layer}  |  HP: {player.health}/{player.max_health}\n")
        print("Skills:")
        for skill in player.skills:
            print(f"  - {skill.name}")
        print("\nWhat would you like to do?")
        print("  1. Explore (fight a random enemy)")
        print("  2. Fuse skills")
        print("  3. Ascend to the next layer")
        print("  4. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            enemy = Enemy(player.layer)
            if battle(player, enemy):
                # Absorb a skill from the enemy
                skill = player.choose_skill_to_absorb(enemy)
                player.absorb_skill(skill)
                print(f"You devour the {enemy.name} and learn {skill.name}!\n")
                # Occasionally trigger an evolution after a successful fight
                if random.random() < 0.2:
                    player.evolve()
            else:
                # Player died
                print("\nGAME OVER – your journey ends here.\n")
                break
        elif choice == "2":
            player.choose_fusion(fusion_table)
        elif choice == "3":
            if player.layer == -1:
                print("You push aside a crumbling tomb door and step out into the sunlight!  The surface world sprawls before you.\n")
                print("For now, this is the end of the prototype.  You survived the depths and emerged stronger than before.\n")
                break
            player.layer += 1
            # Heal slightly upon ascending a layer
            player.health = min(player.max_health, player.health + 3)
            print(f"You climb up to Layer {player.layer}.  The air feels a bit lighter.  You regain some health.\n")
        elif choice == "4":
            print("Thanks for playing!\n")
            break
        else:
            print("Invalid choice.  Please enter 1, 2, 3 or 4.\n")


if __name__ == "__main__":
    play_game()
