from components.ai import HostileAI
from components.fighter import Fighter
from entity import Actor

player = Actor(
	char = "@",
	color = (255, 255, 255),
	name = "Edwards",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 30, defense = 2, power = 5)
)

junkie = Actor(
	char = "j",
	color = (218, 192, 96),
	name = "a junkie",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 10, defense = 0, power = 2)
)

roider = Actor(
	char = "R",
	color = (208, 64, 192),
	name = "the roider",
	ai_cls = HostileAI,
	fighter = Fighter(hp = 18, defense = 1, power = 4)
)