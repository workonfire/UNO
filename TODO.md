# To-do list

Goals:
- Easy to use API
- Multiplayer
- Interface (cards etc.) displayed as ASCII art with ncurses
- Fully customizable rooms with custom game rules

What to implement:
- A serious queue system that supports more than two players
- Try to remember what functional cards were skipped due to lack of a queue system
- Tab-completion
- More verbose `--debug` option
- A plugin system? (like `plugins/something-trigger.py`)
- A custom rules system (`Dict[str, Any]`), this includes:
  - bluffing
  - option to pass when drawing cards
- A menu
- Auto-save system
- Aliases like `4B`, `*` and auto-correction like `4lbue` -> `4 BLUE`
