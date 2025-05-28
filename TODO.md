# To-do list

Goals:
- Easy to use API
- Multiplayer
- Interface (cards etc.) displayed as ASCII art with ncurses
- Fully customizable rooms with custom game rules

What to implement:
- Try to remember what functional cards were skipped due to lack of a queue system
- Tab-completion
- ASCII art
- More verbose `--debug` option
- A plugin system? (like `plugins/something-trigger.py`)
- A custom rules system (`dict[str, Any]`), this includes:
  - bluffing
  - option to pass when drawing cards
  - "redirecting" cards to the opponent
- A menu
- Auto-save system
- Aliases like `4B`, `*` and auto-correction like `4lbue` -> `4 BLUE`
- Remove the infinite deck system... there is a FINITE amount of +4's, +2's etc...
- Discord Rich Presence integration

Developer notes:
- Optimize `list()/[*]` and `set()`
