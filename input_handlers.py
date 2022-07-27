from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod.event
import actions
from actions import Action, BumpAction, PickupAction, WaitAction
import color
import exceptions

if TYPE_CHECKING:
	from engine import Engine
	from entity import Item

MOVE_KEYS = {
	# Arrow Keys
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad Keys
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi Keys
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1)
}

WAIT_KEYS = {
	tcod.event.K_PERIOD,
	tcod.event.K_KP_5,
	tcod.event.K_CLEAR
}

CURSOR_Y_KEYS = {
	tcod.event.K_UP: -1,
	tcod.event.K_DOWN: 1,
	tcod.event.K_PAGEUP: -10,
	tcod.event.K_PAGEDOWN: 10
}

class EventHandler(tcod.event.EventDispatch[Action]):
	def __init__(self, engine: Engine):
		self.engine = engine

	def handle_events(self, event: tcod.event.Event) -> None:
		self.handle_action(self.dispatch(event))

	def handle_action(self, action: Optional[Action]) -> bool:
		# returns True if action will advance a turn
		if action is None:
			return False

		try:
			action.perform()
		except exceptions.Impossible as exc:
			self.engine.message_log.add_message(exc.args[0], color.impossible)
			return False # skip update on exceptions

		self.engine.handle_enemy_turns()
		self.engine.update_fov()
		return True

	def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
		if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
			self.engine.mouse_location = event.tile.x, event.tile.y

	def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
		raise SystemExit()

	def on_render(self, console: tcod.Console) -> None:
		self.engine.render(console)

class MainGameEventHandler(EventHandler):

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		action: Optional[Action] = None

		key = event.sym
		player = self.engine.player

		if key in MOVE_KEYS:
			dx, dy = MOVE_KEYS[key]
			action = BumpAction(player, dx, dy)
		elif key in WAIT_KEYS:
			action = WaitAction(player)

		elif key == tcod.event.K_v:
			self.engine.event_handler = HistoryViewer(self.engine)
		elif key == tcod.event.K_COMMA:
			action = PickupAction(player)
		elif key == tcod.event.K_i:
			self.engine.event_handler = InventoryActivateHandler(self.engine)
		elif key == tcod.event.K_d:
			self.engine.event_handler = InventoryDropHandler(self.engine)

		elif key == tcod.event.K_ESCAPE:
			raise SystemExit()

		return action

class GameOverEventHandler(EventHandler):

	def ev_keydown(self, event: tcod.event.KeyDown) -> None:
		key = event.sym

		if key == tcod.event.K_ESCAPE:
			raise SystemExit()

class HistoryViewer(EventHandler):
	def __init__(self, engine: Engine):
		super().__init__(engine)
		self.log_length = len(engine.message_log.messages)
		self.cursor = self.log_length - 1

	def on_render(self, console: tcod.Console) -> None:
		super().on_render(console)

		log_console = tcod.Console(console.width - 6, console.height - 6)

		log_console.draw_frame(0, 0, log_console.width, log_console.height)
		log_console.print_box(0, 0, log_console.width, 1, "┤Message history├", alignment = tcod.CENTER)

		self.engine.message_log.render_messages(
			log_console,
			1,
			1,
			log_console.width - 2,
			log_console.height - 2,
			self.engine.message_log.messages[ :self.cursor + 1]
		)
		log_console.blit(console, 3, 3)

	def ev_keydown(self, event: tcod.event.KeyDown) -> None:
		key = event.sym

		if key in CURSOR_Y_KEYS:
			adjust = CURSOR_Y_KEYS[event.sym]
			if adjust < 0 and self.cursor == 0:
				# move from top to bottom if you're on the edge and move upward
				self.cursor = self.log_length - 1
			elif adjust > 0 and self.cursor == self.log_length - 1:
				# move from bottom to top similarly
				self.cursor = 0
			else:
				# move within the list, snapping (clamping) to top and bottom
				self.cursor = max(0, min(self.cursor+adjust, self.log_length - 1))

		elif key == tcod.event.K_HOME:
			# snap to top
			self.cursor = 0
		elif key == tcod.event.K_END:
			# snap to bottom
			self.cursor = self.log_length - 1
		else:
			# any other key exits the message log screen
			self.engine.event_handler = MainGameEventHandler(self.engine)

class AskUserEventHandler(EventHandler):

	def handle_action(self, action: Optional[Action]) -> bool:
		# resets the handler and returns True if moves a turn
		if super().handle_action(action):
			self.engine.event_handler = MainGameEventHandler(self.engine)
			return True
		return False

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		# by default any key press except modifiers exits this handler
		if event.sym in {
			tcod.event.K_LSHIFT,
			tcod.event.K_RSHIFT,
			tcod.event.K_LCTRL,
			tcod.event.K_RCTRL,
			tcod.event.K_LALT,
			tcod.event.K_RALT
		}:
			return None

		return self.on_exit()

	def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
		# by default any mouse click exits this handler
		return self.on_exit()

	def on_exit(self) -> Optional[Action]:
		# by default returns to main game handler
		self.engine.event_handler = MainGameEventHandler(self.engine)
		return None

class InventoryEventHandler(AskUserEventHandler):

	TITLE = "<MISSING TITLE>"

	def on_render(self, console: tcod.Console) -> None:
		# renders an inventory menu 
		super().on_render(console)

		inventory_length = len(self.engine.player.inventory.items)
		height = max(inventory_length + 2, 3)

		width = len(self.TITLE) + 4

		if self.engine.player.x <= 31:
			x = 64 - width
		else:
			x = 0
		y = 0

		console.draw_frame(x=x, y=y, width=width, height=height,title=self.TITLE, clear=True, fg=(201, 226, 255), bg=(0,42,24))

		if inventory_length > 0:
			for i, item in enumerate(self.engine.player.inventory.items):
				item_key = chr(ord("a") + i)
				console.print(x + 1, y + 1 + i, f"({item_key}) {item.name}")
		else:
			console.print(x + 1, y + 1, "(nothing left...)")

	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		player = self.engine.player
		key = event.sym
		index = key - tcod.event.K_a

		if 0 <= index <= 26:
			try:
				selected_item = player.inventory.items[index]
			except IndexError:
				self.engine.message_log.add_message("No item there.", color.invalid)
				return None
			return self.on_item_select(selected_item)
		return super().ev_keydown(event)

	def on_item_select(self, item: Item) -> Optional[Action]:
		# called when valid item selected
		raise NotImplementedError()

class InventoryActivateHandler(InventoryEventHandler):
	# using an inventory item
	# currently assumes all items are consumables
	TITLE = "Select an item to use"

	def on_item_select(self, item: Item) -> Optional[Action]:
		return item.consumable.get_action(self.engine.player)

class InventoryDropHandler(InventoryEventHandler):
	# dropping an inventory item
	TITLE = "Select an item to drop"

	def on_item_select(self, item: Item) -> Optional[Action]:
		return actions.DropItem(self.engine.player, item)