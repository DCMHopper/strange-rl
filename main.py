#!/usr/bin/env python3
import copy
import tcod

from engine import Engine
import entity_factories
from input_handlers import EventHandler
from procgen import generate_dungeon

def main() -> None:
	screen_width = 64
	screen_height = 69

	map_width = 64
	map_height = 64

	room_max_size = 16
	room_min_size = 4
	max_rooms = 32
	max_monsters_per_room = 2

	tileset = tcod.tileset.load_tilesheet(
		"tiles.png",32,8,tcod.tileset.CHARMAP_TCOD
	)

	event_handler = EventHandler()

	player = copy.deepcopy(entity_factories.player)

	game_map = generate_dungeon(
		max_rooms = max_rooms,
		room_min_size = room_min_size,
		room_max_size = room_max_size,
		map_width = map_width,
		map_height = map_height,
		max_monsters_per_room = max_monsters_per_room,
		player = player)

	engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

	with tcod.context.new_terminal(
		screen_width,
		screen_height,
		tileset = tileset,
		title = "StrangeRL",
		vsync = True,
	) as context:
		root_console = tcod.Console(screen_width, screen_height, order="F")

		while True:
			engine.render(console=root_console, context=context)

			events = tcod.event.wait()
			engine.handle_events(events)



if __name__ == "__main__":
	main()