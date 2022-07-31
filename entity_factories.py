from components.ai import HostileAI
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
	char = "@",
	color = (255, 255, 255),
	name = "Edwards",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 42, defense = 2, power = 5),
	inventory = Inventory(capacity=26)
)

# == ENEMIES ==

junkie = Actor(
	char = "j",
	color = (218, 192, 96),
	name = "a junkie",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 10, defense = 0, power = 3),
	inventory = Inventory(capacity=0)
)

roider = Actor(
	char = "R",
	color = (208, 64, 192),
	name = "the roider",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 18, defense = 1, power = 5),
	inventory = Inventory(capacity=0)
)

dust_goon = Actor(
	char = "c",
	color = (255, 202, 57),
	name = "the duster goon",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 14, defense = 0, power = 3),
	inventory = Inventory(capacity=0)
)

dust_sicario = Actor(
	char = "C",
	color = (197, 145, 0),
	name = "the sicario",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 16, defense = 3, power = 5),
	inventory = Inventory(capacity=0)
)

# == ITEMS ==

smart_bandage = Item(
	char = "!",
	color = (255, 0, 127),
	name = "Smart Bandage",
	consumable = consumable.HealingConsumable(amount = 8)
)

printed_gun = Item(
	char = "=",
	color = (201, 108, 182),
	name = "3D Printed Gun",
	consumable = consumable.BallisticDamageConsumable(damage = 15, max_range = 6)
)


mace = Item(
	char = "~",
	color = (201, 63, 255),
	name = "Mace Spray",
	consumable = consumable.ConfusionConsumable(ticks = 4)
)

explosive_grenade = Item(
	char = "~",
	color = (255, 135, 0),
	name = "Explosive Grenade",
	consumable = consumable.ExplosionDamageConsumable(damage = 10, radius = 2)
)