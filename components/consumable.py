from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import actions
import color
import components.ai
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import SingleTargetHandler, AreaTargetHandler

if TYPE_CHECKING:
	from entity import Actor, Item

class Consumable(BaseComponent):
	parent: Item

	def get_action(self, consumer: Actor) -> Optional[actions.Action]:
		# try to return the action associated with the parent item
		return actions.ItemAction(consumer, self.parent)

	def activate(self, action: actions.ItemAction) -> None:
		raise NotImplementedError()

	def consume(self) -> None:
		item = self.parent
		inventory = item.parent
		if isinstance(inventory, components.inventory.Inventory):
			inventory.items.remove(item)

class HealingConsumable(Consumable):
	def __init__(self, amount: int):
		self.amount = amount

	def activate(self, action: actions.ItemAction) -> None:
		consumer = action.entity
		amount_recovered = consumer.fighter.heal(self.amount)

		if amount_recovered > 0:
			self.engine.message_log.add_message(f"Edwards uses the {self.parent.name}, recovering {amount_recovered} health.", color.health_recovered)
			self.consume()
		else:
			raise Impossible(f"Edwards doesn't have the kind of wounds that will heal.")

class ConfusionConsumable(Consumable):
	def __init__(self, ticks: int):
		self.ticks = ticks

	def get_action(self, consumer: Actor) -> Optional[actions.Action]:
		self.engine.message_log.add_message("Select a target.", color.needs_target)
		self.engine.event_handler = SingleTargetHandler(self.engine, callback = lambda xy: actions.ItemAction(consumer, self.parent, xy))
		return None

	def activate(self, action: actions.ItemAction) -> None:
		consumer = action.entity
		target = action.target_actor

		if not self.engine.game_map.visible[action.target_xy]:
			raise Impossible("You can't hit what you can't see...")
		if not target:
			raise Impossible("Don't waste that on empty air!")

		self.engine.message_log.add_message(f"{target.name.capitalize()} is left stumbling, reeling, swiping at the air.", color.status_applied)

		target.ai = components.ai.ConfusedAI(entity=target, previous_ai=target.ai, ticks=self.ticks)
		self.consume()

class ExplosionDamageConsumable(Consumable):
	def __init__(self, damage: int, radius: int):
		self.damage = damage
		self.radius = radius

	def get_action(self, consumer: Actor) -> Optional[actions.Action]:
		self.engine.message_log.add_message("Select a target.", color.needs_target)
		self.engine.event_handler = AreaTargetHandler(
			self.engine,
			radius = self.radius,
			callback = lambda xy: actions.ItemAction(consumer, self.parent, xy)
		)
		return None

	def activate(self, action: actions.ItemAction) -> None:
		target_xy = action.target_xy

		if not self.engine.game_map.visible[target_xy]:
			raise Impossible("Best not to use that blindly...")

		targets_hit = False

		for actor in self.engine.game_map.actors:
			if actor.distance(*target_xy) <= self.radius:
				self.engine.message_log.add_message(f"The blast catches {actor.name}, dealing {self.damage} damage.")
				actor.fighter.take_damage(self.damage)
				targets_hit = True

		if not targets_hit:
			self.engine.message_log.add_message("The explosion booms in the cramped space, but no one is hurt.")
		self.consume()


class BallisticDamageConsumable(Consumable):
	def __init__(self, damage: int, max_range: int):
		self.damage = damage
		self.max_range = max_range

	def activate(self, action: actions.ItemAction) -> None:
		consumer = action.entity
		target = None
		closest_distance = self.max_range + 1.0

		for actor in self.engine.game_map.actors:
			if actor is not consumer and self.parent.game_map.visible[actor.x, actor.y]:
				distance = consumer.distance(actor.x, actor.y)

				if distance < closest_distance:
					target = actor
					closest_distance = distance

		if target:
			self.engine.message_log.add_message(f"{consumer.name.capitalize()} shoots {target.name}, dealing {self.damage} damage.")

			target.fighter.take_damage(self.damage)
			self.consume()
		else:
			raise Impossible(f"Edwards raises the weapon, but no target presents itself.")

