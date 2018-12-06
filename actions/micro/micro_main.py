"""Everything related to controlling army units goes here"""
import numpy as np
from sc2.constants import (
    ADEPTPHASESHIFT,
    AUTOTURRET,
    BUNKER,
    DISRUPTORPHASED,
    DRONE,
    EGG,
    EVOLVEGROOVEDSPINES,
    EVOLVEMUSCULARAUGMENTS,
    INFESTEDTERRAN,
    INFESTEDTERRANSEGG,
    LARVA,
    MUTALISK,
    HYDRALISK,
    PHOTONCANNON,
    PLANETARYFORTRESS,
    PROBE,
    QUEEN,
    SCV,
    SPINECRAWLER,
    ZERGLING,
    ZERGLINGATTACKSPEED,
)

from actions.micro.micro_helpers import Micro
from actions.micro.unit.hydralisks import HydraControl
from actions.micro.unit.zerglings import ZerglingControl


class ArmyControl(ZerglingControl, HydraControl, Micro):
    """Can be improved"""

    def __init__(self, ai):
        self.ai = ai
        self.retreat_units = set()
        self.baneling_sacrifices = {}
        self.rally_point = None
        self.zergling_atk_speed = False
        self.hydra_move_speed = False
        self.hydra_atk_range = False

    async def should_handle(self, iteration):
        """Requirements to run handle"""
        local_controller = self.ai
        return (
            local_controller.zerglings
            | local_controller.ultralisks
            | local_controller.mutalisks
            | local_controller.hydras
        )

    async def handle(self, iteration):  # needs further refactoring(too-many-branches)
        """It surrounds and target low hp units, also retreats when overwhelmed,
         it can be improved a lot but is already much better than a-move
        Name army_micro because it is in army.py."""
        local_controller = self.ai
        action = local_controller.add_action
        enemy_building = local_controller.enemy_structures
        map_center = local_controller.game_info.map_center
        bases = local_controller.townhalls
        self.behavior_changing_upgrades_check()
        if bases.ready:
            self.rally_point = bases.ready.closest_to(map_center).position.towards(map_center, 10)
        # enemy_detection = enemy_units.not_structure.of_type({OVERSEER, OBSERVER})
        combined_enemies, targets, atk_force, hydra_targets = self.set_unit_groups()
        for attacking_unit in atk_force:
            if self.dodge_effects(attacking_unit):
                continue
            unit_position = attacking_unit.position
            attack_command = attacking_unit.attack
            if self.anti_proxy_trigger(attacking_unit):
                if self.attack_enemy_proxy_units(targets, attacking_unit):
                    continue
                else:
                    action(attacking_unit.move(local_controller.spines.closest_to(attacking_unit)))
                    continue
            if self.anti_terran_bm(attacking_unit):
                continue
            if attacking_unit.tag in self.retreat_units and bases:
                self.has_retreated(attacking_unit)
                continue
            if attacking_unit.type_id == HYDRALISK and hydra_targets and hydra_targets.closer_than(17, unit_position):
                if self.retreat_unit(attacking_unit, combined_enemies):
                    continue
                if self.micro_hydras(hydra_targets, attacking_unit):
                    continue
            if targets and targets.closer_than(17, unit_position):
                if self.retreat_unit(attacking_unit, combined_enemies):
                    continue
                if await self.handling_walls_and_attacking(attacking_unit, targets):
                    continue
            elif enemy_building.closer_than(30, unit_position):
                action(attack_command(enemy_building.closest_to(unit_position)))
                continue
            elif local_controller.time < 1000 and not local_controller.close_enemies_to_base:
                self.idle_unit(attacking_unit)
                continue
            else:
                if self.keep_attacking(attacking_unit, targets):
                    continue
                elif bases:
                    self.move_to_rallying_point(attacking_unit)

    def move_to_rallying_point(self, unit):
        """Set the point where the units should gather"""
        if unit.position.distance_to_point2(self.rally_point) > 5:
            self.ai.add_action(unit.move(self.rally_point))

    def has_retreated(self, unit):
        """Identify if the unit has retreated"""
        if self.ai.townhalls.closer_than(15, unit.position):
            self.retreat_units.remove(unit.tag)

    def retreat_unit(self, unit, combined_enemies):
        """Tell the unit to retreat when overwhelmed"""
        local_controller = self.ai
        if (
            local_controller.townhalls
            and not local_controller.close_enemies_to_base
            and not local_controller.structures.closer_than(7, unit.position)
            and len(combined_enemies.closer_than(20, unit.position))
            >= np.sum(
                np.array(
                    [
                        len(local_controller.zerglings.closer_than(13, unit.position)),
                        len(local_controller.ultralisks.closer_than(13, unit.position)),
                        len(local_controller.hydras.closer_than(13, unit.position)),
                    ]
                )
                * np.array([1, 3, 8])
            )
        ):
            self.move_to_rallying_point(unit)
            self.retreat_units.add(unit.tag)
            return True
        return False

    def idle_unit(self, unit):
        """Control the idle units, by gathering then or telling then to attack"""
        local_controller = self.ai
        if (
            local_controller.supply_used not in range(198, 201)
            and np.sum(
                np.array(
                    [
                        len(local_controller.zerglings.ready),
                        len(local_controller.hydras.ready),
                        len(local_controller.ultralisks.ready),
                    ]
                )
                * np.array([1, 2, 4])
            )
            < 41
            and local_controller.townhalls
            and self.retreat_units
            and not local_controller.counter_attack_vs_flying
        ):
            self.move_to_rallying_point(unit)
            return True
        if not local_controller.close_enemy_production or local_controller.time >= 480:
            enemy_building = local_controller.enemy_structures
            if enemy_building and local_controller.townhalls:
                self.attack_closest_building(unit)
            else:
                self.attack_startlocation(unit)
        return False

    def attack_closest_building(self, unit):
        """Attack the starting location"""
        local_controller = self.ai
        enemy_building = local_controller.enemy_structures.not_flying
        if enemy_building:
            local_controller.add_action(
                unit.attack(enemy_building.closest_to(local_controller.furthest_townhall_to_map_center))
            )

    def attack_startlocation(self, unit):
        """It tell to attack the starting location"""
        local_controller = self.ai
        if local_controller.enemy_start_locations:
            local_controller.add_action(unit.attack(local_controller.enemy_start_locations[0]))

    def anti_proxy_trigger(self, unit):
        """It triggers the anti-proxy logic"""
        local_controller = self.ai
        spines = local_controller.spines
        return (
            local_controller.close_enemy_production
            and spines
            and not spines.closer_than(2, unit)
            and (local_controller.time <= 480 or len(local_controller.zerglings) <= 14)
        )

    def attack_enemy_proxy_units(self, targets, unit):
        """Attack the proxy army if it get too close to the ramp"""
        return (
            targets
            and targets.closer_than(5, unit)
            and unit.type_id == ZERGLING
            and self.micro_zerglings(unit, targets)
        )

    def set_unit_groups(self):
        """Set the targets, combined_enemies and atk_force"""
        targets = None
        hydra_targets = None
        combined_enemies = None
        local_controller = self.ai
        enemy_units = local_controller.enemies
        enemy_building = local_controller.enemy_structures
        if enemy_units:
            excluded_units = {
                ADEPTPHASESHIFT,
                DISRUPTORPHASED,
                EGG,
                LARVA,
                INFESTEDTERRANSEGG,
                INFESTEDTERRAN,
                AUTOTURRET,
            }
            filtered_enemies = enemy_units.not_structure.exclude_type(excluded_units)
            static_defence = enemy_building.of_type({SPINECRAWLER, PHOTONCANNON, BUNKER, PLANETARYFORTRESS})
            combined_enemies = filtered_enemies.exclude_type({DRONE, SCV, PROBE}) | static_defence
            targets = static_defence | filtered_enemies.not_flying
            hydra_targets = static_defence | filtered_enemies
        atk_force = (
            local_controller.zerglings
            | local_controller.ultralisks
            | local_controller.mutalisks
            | local_controller.hydras
        )
        if local_controller.floating_buildings_bm and local_controller.supply_used >= 199:
            atk_force = atk_force | local_controller.queens
        return combined_enemies, targets, atk_force, hydra_targets

    def anti_terran_bm(self, unit):
        """Logic for countering the floating buildings bm"""
        local_controller = self.ai
        enemy_building = local_controller.enemy_structures
        flying_buildings = enemy_building.flying
        if unit.type_id in (MUTALISK, QUEEN, HYDRALISK) and flying_buildings:
            local_controller.add_action(unit.attack(flying_buildings.closest_to(unit.position)))
            return True
        return False

    async def handling_walls_and_attacking(self, unit, target):
        """It micros normally if no wall, if there is one attack it"""
        local_controller = self.ai
        unit_position = unit.position
        closest_target = target.closest_to
        attack_command = unit.attack
        action = local_controller.add_action
        if await local_controller.client.query_pathing(unit, closest_target(unit).position):
            if unit.type_id == ZERGLING:
                return self.micro_zerglings(unit, target)
            action(attack_command(closest_target(unit_position)))
            return True
        action(attack_command(local_controller.enemies.not_flying.closest_to(unit_position)))
        return True

    def keep_attacking(self, unit, target):
        """It keeps the attack going if it meets the requirements no matter what"""
        local_controller = self.ai
        unit_position = unit.position
        attack_command = unit.attack
        action = local_controller.add_action
        enemy_building = local_controller.enemy_structures
        if not self.retreat_units or local_controller.close_enemies_to_base or local_controller.time >= 1000:
            if enemy_building:
                action(attack_command(enemy_building.closest_to(unit_position)))
                return True
            if target:
                action(attack_command(target.closest_to(unit_position)))
                return True
            self.attack_startlocation(unit)
            return True
        return False

    def behavior_changing_upgrades_check(self):
        """Check for upgrades the will change how the units behavior are calculated"""
        local_controller = self.ai
        if not self.zergling_atk_speed and local_controller.hives:
            self.zergling_atk_speed = local_controller.already_pending_upgrade(ZERGLINGATTACKSPEED) == 1
        if not self.hydra_move_speed and local_controller.hydradens:
            self.hydra_move_speed = local_controller.already_pending_upgrade(EVOLVEMUSCULARAUGMENTS) == 1
        if not self.hydra_atk_range and local_controller.hydradens:
            self.hydra_atk_range = local_controller.already_pending_upgrade(EVOLVEGROOVEDSPINES) == 1