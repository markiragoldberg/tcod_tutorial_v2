from typing import Dict

from entity import Entity
from procgen import enemy_chances, get_entities_at_random
import entity_factories


def count_generated_entities(total_entities: int, floor: int) -> Dict[Entity, int]:
    entities = get_entities_at_random(enemy_chances, total_entities, floor)
    entity_counts: Dict[Entity, int] = {}
    for enty in entities:
        if enty in entity_counts:
            entity_counts[enty] += 1
        else:
            entity_counts[enty] = 1
    return entity_counts


def approximately_equal(x: float, y: float, epsilon: float = 0.02) -> bool:
    return abs(x - y) < x * epsilon


def test_get_entities_at_random() -> None:
    entity_counts = count_generated_entities(1000, floor=1)
    assert entity_counts[entity_factories.orc] == 1000

    total_entities = 100000
    entity_counts = count_generated_entities(total_entities, floor=3)
    assert approximately_equal(
        entity_counts[entity_factories.orc], (total_entities * 80) / 95
    )
    entity_counts = count_generated_entities(total_entities, floor=5)
    assert approximately_equal(
        entity_counts[entity_factories.orc], (total_entities * 80) / 110
    )
    entity_counts = count_generated_entities(total_entities, floor=7)
    assert approximately_equal(
        entity_counts[entity_factories.orc], (total_entities * 80) / 140
    )
