from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple
import random

import tcod

from game_map import GameMap
from point2d import Point2d
from simplecurve import SimpleCurve
import entity_factories
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

max_items_by_floor = SimpleCurve()
max_items_by_floor.add_point(Point2d(1, 1))
max_items_by_floor.add_point(Point2d(4, 2))

max_monsters_by_floor = SimpleCurve()
max_monsters_by_floor.add_point(Point2d(1, 2))
max_monsters_by_floor.add_point(Point2d(4, 3))
max_monsters_by_floor.add_point(Point2d(6, 5))

health_potion_by_floor = SimpleCurve()
health_potion_by_floor.add_point(Point2d(0, 35))

confusion_scroll_by_floor = SimpleCurve()
confusion_scroll_by_floor.add_point(Point2d(1, 0))
confusion_scroll_by_floor.add_point(Point2d(2, 10))

lightning_scroll_by_floor = SimpleCurve()
lightning_scroll_by_floor.add_point(Point2d(3, 0))
lightning_scroll_by_floor.add_point(Point2d(4, 25))

sword_by_floor = SimpleCurve()
sword_by_floor.add_point(Point2d(3, 0))
sword_by_floor.add_point(Point2d(4, 5))

sword_by_floor = SimpleCurve()
sword_by_floor.add_point(Point2d(3, 0))
sword_by_floor.add_point(Point2d(4, 5))

fireball_scroll_by_floor = SimpleCurve()
fireball_scroll_by_floor.add_point(Point2d(5, 0))
fireball_scroll_by_floor.add_point(Point2d(6, 25))

chain_mail_by_floor = SimpleCurve()
chain_mail_by_floor.add_point(Point2d(5, 0))
chain_mail_by_floor.add_point(Point2d(6, 15))

item_curves_by_floor: Dict[Entity, SimpleCurve] = {
    entity_factories.health_potion: health_potion_by_floor,
    entity_factories.confusion_scroll: confusion_scroll_by_floor,
    entity_factories.lightning_scroll: lightning_scroll_by_floor,
    entity_factories.sword: sword_by_floor,
    entity_factories.fireball_scroll: fireball_scroll_by_floor,
    entity_factories.chain_mail: chain_mail_by_floor,
}

orc_curve: SimpleCurve = SimpleCurve()
orc_curve.add_point(Point2d(1, 80))

troll_curve: SimpleCurve = SimpleCurve()
troll_curve.add_point(Point2d(2, 0))
troll_curve.add_point(Point2d(3, 15))
troll_curve.add_point(Point2d(5, 30))
troll_curve.add_point(Point2d(7, 60))

enemy_chances: Dict[Entity, SimpleCurve] = {
    entity_factories.orc: orc_curve,
    entity_factories.troll: troll_curve,
}


def get_max_value_for_floor(max_value_curve: SimpleCurve, floor: int) -> int:
    return int(max_value_curve(floor))


def get_entities_at_random(
    entity_weight_curves: Dict[Entity, SimpleCurve], number_of_entities: int, floor: int
) -> List[Entity]:
    entities = []
    chances = []

    for entity, curve in entity_weight_curves.items():
        chance = curve(floor)
        if chance > 0:
            entities.append(entity)
            chances.append(chance)

    chosen_entities = []

    chosen_entities = random.choices(entities, weights=chances, k=number_of_entities)

    return chosen_entities


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_curves_by_floor, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
