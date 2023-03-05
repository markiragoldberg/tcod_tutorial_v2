from __future__ import annotations

from typing import TYPE_CHECKING
import lzma
import pickle

from tcod.console import Console
from tcod.map import compute_fov

from components.ai import HostileEnemy
from message_log import MessageLog
import exceptions
import render_functions

if TYPE_CHECKING:
    from typing import List, Union

    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.target: Union[Actor, None] = None
        self.targets: List[Actor] = []

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=99,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

        # Cache potential targets
        self.targets = self.game_map.get_visible_targets(self.player)
        # Deselect current target if dead or not visible
        if self.target is not None and (
            self.target not in self.targets
            or not isinstance(self.target.ai, HostileEnemy)
        ):
            self.target = None
        # Automatically retarget closest enemy if no current target
        if self.targets and not self.target:
            self.target = self.targets[0]

    def nextTarget(self) -> None:
        if self.target and len(self.targets) > 1:
            i = self.targets.index(self.target)
            i = (i + 1) % len(self.targets)
            self.target = self.targets[i]

    def previousTarget(self) -> None:
        if self.target and len(self.targets) > 1:
            i = self.targets.index(self.target)
            self.target = self.targets[i - 1]

    def render(self, console: Console) -> None:
        self.game_map.render(console, self.target)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
