from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING
import color
import exceptions

if TYPE_CHECKING:
	from engine import Engine
	from entity import Actor, Entity, Item

# Generic action class which all other inherit
class Action:
	def __init__(self, entity: Actor) -> None:
		super().__init__()
		self.entity = entity

	@property
	def engine(self) -> Engine:
		return self.entity.game_map.engine

	def perform(self) -> None:
		# Override this method in subclasses
		raise NotImplementedError()

class WaitAction(Action):
	def perform(self) -> None:
		pass

# generic item usage
class ItemAction(Action):
	def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
		super().__init__(entity)
		self.item = item
		if not target_xy:
			target_xy = entity.x, entity.y
		self.target_xy = target_xy

	@property
	def target_actor(self) -> Optional[Actor]:
		return self.engine.game_map.get_actor_at_location(*self.target_xy)
	

	def perform(self) -> None:
		# passes this action to the consumable to provide context
		self.item.consumable.activate(self)

# get item off floor
class PickupAction(Action):
	def __init__(self, entity: Actor):
		super().__init__(entity)

	def perform(self) -> None:
		actor_location_x = self.entity.x
		actor_location_y = self.entity.y
		inventory = self.entity.inventory

		for item in self.engine.game_map.items:
			if actor_location_x == item.x and actor_location_y == item.y:
				if len(inventory.items) >= inventory.capacity:
					raise exceptions.Impossible("Edwards has full pockets.")

				self.engine.game_map.entities.remove(item)
				item.parent = self.entity.inventory
				inventory.items.append(item)

				self.engine.message_log.add_message(f"The {item.name} disappears into one of Edwards's pockets.")
				return

		raise exceptions.Impossible("Edwards grabs at the floor, but only comes up with a handful of rock dust.")

class DropItem(ItemAction):
	def perform(self) -> None:
		self.entity.inventory.drop(self.item)

# Generic directional action
class ActionWithDirection(Action):
	def __init__(self, entity: Actor, dx: int, dy:int):
		super().__init__(entity)

		self.dx = dx
		self.dy = dy

	@property
	def dest_xy(self) -> Tuple[int, int]:
		return self.entity.x + self.dx, self.entity.y + self.dy
	

	@property
	def blocking_entity(self) -> Optional[Entity]:
		return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

	@property
	def target_actor(self) -> Optional[Actor]:
		return self.engine.game_map.get_actor_at_location(*self.dest_xy)
	

	def perform(self) -> None:
		raise NotImplementedError()

# Directional melee attack
class MeleeAction(ActionWithDirection):

	def perform(self) -> None:
		target = self.target_actor

		if not target:
			raise exceptions.Impossible("Nothing to attack.")

		damage = self.entity.fighter.power - target.fighter.defense
		attack_desc = f"{self.entity.name.capitalize()} swings at {target.name}"

		if self.entity is self.engine.player:
			attack_color = color.player_atk
		else:
			attack_color = color.enemy_atk

		if damage > 0:
			self.engine.message_log.add_message(f"{attack_desc} for {damage} damage!", attack_color)
			target.fighter.hp -= damage
		else:
			self.engine.message_log.add_message(f"{attack_desc}, but doesn't leave a scratch...", attack_color)


# Directional movement action
class MovementAction(ActionWithDirection):

	def perform(self) -> None:
		dest_x, dest_y = self.dest_xy

		if not self.engine.game_map.in_bounds(dest_x, dest_y):
			raise exceptions.Impossible("The way is blocked.")
		if not self.engine.game_map.tiles["walkable"][dest_x,dest_y]:
			raise exceptions.Impossible("Edwards is backed against the wall...")
		if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
			raise exceptions.Impossible("There's someone in the way.")

		self.entity.move(self.dx, self.dy)


# Selects melee or movement based on blocking entity in target cell
class BumpAction(ActionWithDirection):

	def perform(self) -> None:
		if self.target_actor:
			return MeleeAction(self.entity, self.dx, self.dy).perform()
		else:
			return MovementAction(self.entity, self.dx, self.dy).perform()