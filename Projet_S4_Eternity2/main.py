"""Entry point wrapper that defers importing the heavy `game` module.

The project calls `pygame.init()` at import time inside `game.py`, which
breaks when packaging for the web with pygbag if imported too early. To
support both desktop and pygbag (browser) builds we import `game` only
inside `main()` after detecting the environment.
"""

import importlib
import sys
import asyncio

async  def main():
    """Run the game. Detect if running under pygbag and import `game`
    at runtime so pygame can initialize correctly in the web build.
    """
    is_pygbag = False
    try:
        # Importing pygbag when running inside the browser build will
        # succeed. We only use its presence as a hint; no direct calls
        # are required for a basic wrapper.
        import pygbag  # type: ignore
        is_pygbag = True
    except Exception:
        is_pygbag = False

    # Import the game module lazily to avoid top-level pygame.init() side
    # effects during module import (important for pygbag/emscripten).
    game = importlib.import_module("game")

    # Run the game. On desktop, handle KeyboardInterrupt to ensure
    # pygame quits cleanly. In pygbag (browser) KeyboardInterrupt is
    # unlikely, so just run.
    if is_pygbag:
        game.run_game()
    else:
        try:
            game.run_game()
        except KeyboardInterrupt:
            try:
                import pygame

                pygame.quit()
            except Exception:
                pass
    await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
