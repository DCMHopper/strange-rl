from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity

# Generic action class which all other inherit
class Action:
	def __init__(self, entity: Entity) -> None:
		super().__init__()
		self.entity = entity

	@property
	def engine(self) -> Engine:
		return self.entity.game_map.engine

	def perform(self) -> None:
		# Override this method in subclasses
		raise NotImplementedError()


# Quit the game
class EscapeAction(Action):
	def perform(self) -> None:
		raise SystemExit()


# Generic directional action
class ActionWithDirection(Action):
	def __init__(self, entity: Entity, dx: int, dy:int):
		super().__init__(entity)

		self.dx = dx
		self.dy = dy

	@property
	def dest_xy(self) -> Tuple[int, int]:
		return self.entity.x + self.dx, self.entity.y + self.dy
	

	@property
	def blocking_entity(self) -> Optional[Entity]:
		return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
	

	def perform(self) -> None:
		raise NotImplementedError()


# Directional melee attack
class MeleeAction(ActionWithDirection):

	def perform(self) -> None:
		target = self.blocking_entity

		if not target:
			return

		print(f"You swing at the {target.name}!")


# Directional movement action
class MovementAction(ActionWithDirection):

	def perform(self) -> None:
		dest_x, dest_y = self.dest_xy

		if not self.engine.game_map.in_bounds(dest_x, dest_y):
			return
		if not self.engine.game_map.tiles["walkable"][dest_x,dest_y]:
			return
		if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
			return

		self.entity.move(self.dx, self.dy)


# Selects melee or movement based on blocking entity in target cell
class BumpAction(ActionWithDirection):

	def perform(self) -> None:
		if self.blocking_entity:
			return MeleeAction(self.entity, self.dx, self.dy).perform()
		else:
			return MovementAction(self.entity, self.dx, self.dy).perform()