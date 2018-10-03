"""Everything related to army bahvior"""
from sc2.constants import (
    ADEPTPHASESHIFT,
    AUTOTURRET,
    BUNKER,
    CREEPTUMOR,
    CREEPTUMORQUEEN,
    CREEPTUMORBURROWED,
    CREEPTUMORMISSILE,
    DISRUPTORPHASED,
    DRONE,
    EFFECT_INJECTLARVA,
    EGG,
    INFESTEDTERRAN,
    INFESTEDTERRANSEGG,
    LARVA,
    PHOTONCANNON,
    PLANETARYFORTRESS,
    PROBE,
    QUEENSPAWNLARVATIMER,
    SCV,
    SPINECRAWLER,
    ZERGLING,
    ZERGLINGATTACKSPEED,
)


class army_control:
    def __init__(self):
        self.selected_worker = None

    def army_micro(self):
        """Micro function, its just slight better than a-move, need A LOT of improvements.
        Name army_micro because it is in army.py."""
        targets = None
        filtered_enemies = None
        enemy_building = self.known_enemy_structures
        if self.known_enemy_units:
            excluded_units = {
                ADEPTPHASESHIFT,
                DISRUPTORPHASED,
                EGG,
                LARVA,
                INFESTEDTERRANSEGG,
                INFESTEDTERRAN,
                AUTOTURRET,
            }
            filtered_enemies = self.known_enemy_units.not_structure.exclude_type(excluded_units)
            static_defence = self.known_enemy_units.of_type({SPINECRAWLER, PHOTONCANNON, BUNKER, PLANETARYFORTRESS})
            targets = static_defence | filtered_enemies.not_flying
        atk_force = self.zerglings | self.ultralisks
        # enemy_detection = self.known_enemy_units.not_structure.of_type({OVERSEER, OBSERVER})
        for attacking_unit in atk_force:
            if attacking_unit.tag in self.retreat_units:
                if self.units.structure.owned.exclude_type(
                    {CREEPTUMORQUEEN, CREEPTUMOR, CREEPTUMORBURROWED,  CREEPTUMORMISSILE}
                ).closer_than(15, attacking_unit.position):
                    self.retreat_units.remove(attacking_unit.tag)
                continue
            if targets and targets.closer_than(17, attacking_unit.position):
                # retreat if we are not fighting at home
                if (self.townhalls and
                    not self.units.structure.closer_than(15, attacking_unit.position)
                    and len(filtered_enemies.exclude_type({DRONE, SCV, PROBE}).closer_than(15, attacking_unit.position))
                    >= len(self.zerglings.closer_than(15, attacking_unit.position))
                    + len(self.ultralisks.closer_than(15, attacking_unit.position)) * 4
                ):
                    self.actions.append(
                        attacking_unit.move(
                            self.townhalls.closest_to(self._game_info.map_center).position.towards(
                                self._game_info.map_center, 10
                            )
                        )
                    )
                    self.retreat_units.add(attacking_unit.tag)
                    continue
                in_range_targets = targets.in_attack_range_of(attacking_unit)
                if attacking_unit.type_id == ZERGLING:
                    if in_range_targets:
                        if (
                            self.already_pending_upgrade(ZERGLINGATTACKSPEED) == 1
                            and attacking_unit.weapon_cooldown <= 0.25
                        ):  # more than half of the attack time with adrenal glands (0.35)
                            self.attack_lowhp(attacking_unit, in_range_targets)
                            continue  # these continues are needed so a unit doesnt get multiple orders per step
                        elif (
                            attacking_unit.weapon_cooldown <= 0.35
                        ):  # more than half of the attack time with adrenal glands (0.35)
                            self.attack_lowhp(attacking_unit, in_range_targets)
                            continue
                        else:
                            self.actions.append(attacking_unit.attack(targets.closest_to(attacking_unit.position)))
                            continue
                    else:
                        self.actions.append(attacking_unit.attack(targets.closest_to(attacking_unit.position)))
                        continue
                else:
                    self.actions.append(attacking_unit.attack(targets.closest_to(attacking_unit.position)))
                    continue
            elif enemy_building.closer_than(30, attacking_unit.position):
                self.actions.append(attacking_unit.attack(enemy_building.closest_to(attacking_unit.position)))
                continue

            elif self.time < 1000 and not self.close_enemies_to_base:
                self.idle_unit(attacking_unit)
                continue

            else:
                if enemy_building:
                    self.actions.append(attacking_unit.attack(enemy_building.closest_to(attacking_unit.position)))
                    continue
                elif targets:
                    self.actions.append(attacking_unit.attack(targets.closest_to(attacking_unit.position)))
                    continue
                else:
                    self.attack_startlocation(attacking_unit)

    def idle_unit(self, unit):
        if (
            len(self.ultralisks.ready) < 4
            and self.supply_used not in range(198, 201)
            and len(self.zerglings.ready) < 41
            and self.townhalls
            and self.retreat_units
        ):
            self.actions.append(
                unit.move(
                    self.townhalls.closest_to(self._game_info.map_center).position.towards(
                        self._game_info.map_center, 11
                    )
                )
            )
        else:
            self.attack_startlocation(unit)

    def attack_startlocation(self, unit):
        if self.enemy_start_locations:
            self.actions.append(unit.attack(self.enemy_start_locations[0]))

    def detection_control(self):
        atk_force = self.zerglings | self.ultralisks
        if self.overseers:
            selected_ov = self.overseers.first
            if atk_force:
                self.actions.append(selected_ov.move(atk_force.closest_to(selected_ov.position)))
            elif self.townhalls:
                self.actions.append(selected_ov.move(self.townhalls.closest_to(selected_ov.position)))

    async def queens_abilities(self):
        """Injection and creep spread"""
        queens = self.queens
        hatchery = self.townhalls
        if hatchery:
            # lowhp_ultralisks = self.ultralisks.filter(lambda lhpu: lhpu.health_percentage < 0.27)
            for queen in queens.idle:
                # if not lowhp_ultralisks.closer_than(8, queen.position):
                selected = hatchery.closest_to(queen.position)
                if queen.energy >= 25 and not selected.has_buff(QUEENSPAWNLARVATIMER):
                    self.actions.append(queen(EFFECT_INJECTLARVA, selected))
                    continue
                elif queen.energy >= 26:
                    await self.place_tumor(queen)

                # elif queen.energy >= 50:
                #     self.actions.append(queen(TRANSFUSION_TRANSFUSION, lowhp_ultralisks.closest_to(queen.position)))

            for hatch in hatchery.ready.noqueue:
                if not queens.closer_than(4, hatch):
                    for queen in queens:
                        if not self.townhalls.closer_than(4, queen):
                            self.actions.append(queen.move(hatch.position))
                            break

    def scout_map(self):
        if not self.drones:
            return
        waypoints = [point for point in self.expansion_locations]
        start = self.start_location
        scout = self.drones.closest_to(start)
        waypoints.sort(key=lambda p: ((p[0] - start[0]) ** 2 + (p[1] - start[1]) ** 2))
        for point in waypoints:
            self.actions.append(scout.move(point, queue=True))
