from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING
import numpy as np
import tcod
from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction

if TYPE_CHECKING:
	from entity import Actor

class BaseAI(Action):
	entity: Actor

	def perform(self) -> None:
		raise NotImplementedError()

	# Compute and return a path to the destination, or if invalid, return an empty list
	def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:

		cost = np.array(self.entity.game_map.tiles["walkable"], dtype=np.int8)

		for entity in self.entity.game_map.entities:
			# penalizes paths blocked by other entities
			if entity.blocks_movement and cost[entity.x, entity.y]:
				cost[entity.x, entity.y] += 10

		graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
		pathfinder = tcod.path.Pathfinder(graph)

		pathfinder.add_root((self.entity.x, self.entity.y))

		path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

		return [(index[0], index[1]) for index in path]

class ConfusedAI(BaseAI):
	def __init__(self, entity: Actor, previous_ai: Optional[BaseAI], ticks: int):
		super().__init__(entity)
		self.previous_ai = previous_ai
		self.ticks = ticks

	def perform(self) -> None:
		if self.ticks <= 0:
			self.engine.message_log.add_message(f"{self.entity.name.capitalize()} shakes it off.")
			self.entity.ai = self.previous_ai

		else:
			dx, dy = random.choice([
				(-1, -1),
				(0, -1),
				(1, -1),
				(-1, 0),
				(1, 0),
				(-1, 1),
				(0, 1),
				(1, 1)
			])
			self.ticks -= 1
			return BumpAction(self.entity, dx, dy).perform()

class HostileAI(BaseAI):
	def __init__(self, entity: Actor):
		super().__init__(entity)
		self.path: List[Tuple[int, int]] = []

	def perform(self) -> None:
		target = self.engine.player
		dx = target.x - self.entity.x
		dy = target.y - self.entity.y
		distance = max(abs(dx), abs(dy)) # Chebyshev distance

		if self.engine.game_map.visible[self.entity.x,self.entity.y]:
			if distance <= 1:
				return MeleeAction(self.entity, dx, dy).perform()

			self.path = self.get_path_to(target.x, target.y)

		if self.path:
			dest_x, dest_y = self.path.pop(0)
			return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

		return WaitAction(self.entity).perform()