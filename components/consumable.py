from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible

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