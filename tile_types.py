from typing import Tuple
import numpy as np

# graphics structure defined in Console.tiles_rgb
graphic_dt = np.dtype([
		("ch", np.int32), # Unicode codepoint
		("fg", "3B"),
		("bg", "3B"),
	])

tile_dt = np.dtype([
		("walkable", np.bool),
		("transparent", np.bool),
		("dark", graphic_dt),
		("light", graphic_dt),
	])

def new_tile(
	*,
	walkable: int,
	transparent: int,
	dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
	light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
	return np.array( (walkable, transparent, dark, light), dtype=tile_dt )

# unexplored, unseen tiles
SHROUD = np.array( (ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt )

floor = new_tile(
	walkable=True,
	transparent=True,
	dark=( ord(" "), (255, 255, 255), (24, 12, 12) ),
	light=( ord(" "), (255, 255, 255), (64, 72, 72) )
)
wall = new_tile(
	walkable=False,
	transparent=False,
	dark=( ord(" "), (255, 255, 255), (108, 96, 96) ),
	light=( ord(" "), (255, 255, 255), (192, 200, 208) )
)