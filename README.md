# Strange-RL

This is an ASCII roguelike based off `python-tcod` and the associated [Roguelike Tutorial](https://rogueliketutorials.com/)

Conceptually this game is about walking through asteroids

I'm not keeping a devlog or anything right now, because other than some flavor elements I'm following the tutorial code almost exactly. If I end up extending this game beyond that tutorial, I'll add a changelog and possibly more documentation around development

## Known Issues

These are gameplay-breaking bugs that will either be addressed in the Road Map (pre-0.1 release) or in bug fixes (after 0.1 release)

- [ ] AoE targeting reticule does not align with which tiles will actually receive damage.
- [ ] AoE targeting reticule also blocks sprites where the frame is being drawn

## Road Map

Goals for mechanics, content or anything else not currently in the game and not already implied by the basic mechanics of a roguelike.

- Graphics
	- [ ] Floor-highlight AoE reticule
	- [ ] Animated tile effects
	- [ ] Custom sprites (or at least better colors)
	- [ ] Flavor images
- Overworld
	- [ ] Destination select at the end of each level
	- [ ] Different generation for Morgan and non-Morgan levels
	- [ ] Special Ceres level rules
	- [ ] Special final level rules
	- [ ] Possibility to meet Morgan's Lieutenants early
- Proc Gen
	- [ ] Overhaul map generation
	- [ ] Special themed rooms
- Gameplay
	- [ ] Destination clue system
	- [ ] NPCs, including terminals
	- [ ] Dialogue boxes
	- [ ] Friendly, neutral or mutually hostile AI
	- [ ] Player economy
- Story
	- [ ] Intro sequence giving context for the game
	- [ ] Random encounter triggers