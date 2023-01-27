from typing import Dict

from entity import Entity
from point2d import Point2d
from simplecurve import SimpleCurve
import entity_factories

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
