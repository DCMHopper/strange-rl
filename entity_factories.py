from components.ai import HostileAI
from components.consumable import HealingConsumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
	char = "@",
	color = (255, 255, 255),
	name = "Edwards",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 30, defense = 2, power = 5),
	inventory = Inventory(capacity=26)
)

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

smart_bandage = Item(
	char = "!",
	color = (255, 0, 127),
	name = "Smart Bandage",
	consumable = HealingConsumable(amount = 8)
)