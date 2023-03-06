from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define

from components.base_component import BaseComponent
from components.inventory import Inventory

if TYPE_CHECKING:
    from typing import List, Union

    from entity import Item


@define
class Cooldown:
    length: int = 1
    remaining: int = 0
    messages: Union[List[str], None] = None


class Firearm(BaseComponent):
    parent: Item

    def __init__(
        self,
        damage: int,
        max_ammo: int = 1,
        ammo: int = 1,
        burst: int = 1,
        radius: int = 0,
        cooldown: Union[Cooldown, None] = None,
    ):
        self.damage = damage
        self.ammo = self.max_ammo = max_ammo
        self.burst = burst
        self.radius = radius
        self.cooldown = cooldown

    def can_shoot(self) -> bool:
        if self.ammo <= 0 or (self.cooldown and self.cooldown.remaining > 0):
            return False
        return True

    def skip_turn(self) -> None:
        if self.cooldown and self.cooldown.remaining > 0:
            self.cooldown.remaining -= 1
            if self.cooldown.messages:
                if (
                    self.cooldown.remaining < len(self.cooldown.messages)
                    and isinstance(self.parent.parent, Inventory)
                    and self.parent.parent.parent is self.parent.gamemap.engine.player
                ):
                    self.parent.gamemap.engine.message_log.add_message(
                        self.cooldown.messages[self.cooldown.remaining]
                    )


class Shotgun(Firearm):
    def __init__(self) -> None:
        super().__init__(
            damage=24,
            max_ammo=16,
            cooldown=Cooldown(messages=["You pump your shotgun."]),
        )


class Chaingun(Firearm):
    def __init__(self) -> None:
        super().__init__(damage=16, max_ammo=60, burst=3)


class RocketLauncher(Firearm):
    def __init__(self) -> None:
        super().__init__(
            damage=24,
            max_ammo=8,
            radius=2,
            cooldown=Cooldown(messages=["You reload your rocket launcher."]),
        )
