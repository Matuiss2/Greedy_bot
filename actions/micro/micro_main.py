"""Everything related to controlling army units goes here"""
from sc2.constants import UnitTypeId
from actions.micro.army_value_tables import ArmyValues
from actions.micro.unit.zergling_control import ZerglingControl
from actions.micro.specific_units_behaviors import SpecificUnitsBehaviors


class ArmyControl(ZerglingControl, SpecificUnitsBehaviors, ArmyValues):
    """Can be improved performance wise also few bugs on some of it's elements"""

    def __init__(self, main):
        self.main = main
        self.retreat_units = set()
        self.baneling_sacrifices = {}
        self.targets = self.atk_force = self.hydra_targets = None
        self.army_types = {UnitTypeId.ZERGLING, UnitTypeId.HYDRALISK, UnitTypeId.MUTALISK, UnitTypeId.ULTRALISK}

    async def should_handle(self):
        """Requirements to run handle"""
        return self.main.units.of_type(self.army_types)

    async def handle(self):
        """Run the logic for all unit types, it can be improved a lot but is already much better than a-move"""
        self.set_unit_groups()
        await self.do_or_die_prompt()
        for attacking_unit in self.atk_force:
            if self.avoid_effects(attacking_unit):
                continue
            if self.avoid_disruptor_shots(attacking_unit):
                continue
            if self.anti_proxy_prompt:
                if self.attack_enemy_proxy_units(attacking_unit):
                    continue
                self.move_to_rallying_point(self.targets, attacking_unit)
                continue
            if self.anti_terran_bm(attacking_unit):
                continue
            if attacking_unit.tag in self.retreat_units:
                self.has_retreated(attacking_unit)
                continue
            if self.specific_hydra_behavior(self.hydra_targets, attacking_unit):
                continue
            if await self.specific_zergling_behavior(self.targets, attacking_unit):
                continue
            if self.target_buildings(attacking_unit):
                continue
            if not self.main.close_enemies_to_base:
                self.delegate_idle_unit(attacking_unit)
                continue
            if self.keep_attacking(attacking_unit):
                continue
            self.move_to_rallying_point(self.targets, attacking_unit)

    @property
    def anti_proxy_prompt(self):
        """Requirements for the anti-proxy logic"""
        return (
            self.main.close_enemy_production
            and self.main.spines
            and (self.main.time <= 480 or self.main.zergling_amount <= 14)
        )

    def anti_terran_bm(self, unit):
        """Logic for countering the floating buildings bm"""
        if self.main.flying_enemy_structures and unit.can_attack_air:
            self.main.add_action(unit.attack(self.main.flying_enemy_structures.closest_to(unit.position)))
            return True
        return False

    def attack_closest_building(self, unit):
        """Attack the closest enemy building"""
        enemy_building = self.main.enemy_structures.not_flying
        if enemy_building:
            self.main.add_action(unit.attack(enemy_building.closest_to(self.main.furthest_townhall_to_center)))

    def attack_enemy_proxy_units(self, unit):
        """Requirements to attack the proxy army if it gets too close to the ramp"""
        return (
            self.targets
            and unit.type_id == UnitTypeId.ZERGLING
            and self.targets.closer_than(5, unit)
            and self.microing_zerglings(unit, self.targets)
        )

    async def do_or_die_prompt(self):
        """Just something to stop it going idle, attack with everything if nothing else can be done,
         or rebuild the main if we can, probably won't make much difference since its very different"""
        if not self.main.ready_bases:
            if self.main.minerals < 300:
                for unit in self.atk_force | self.main.drones:
                    self.main.add_action(unit.attack(self.main.enemy_start_locations[0]))
            else:
                await self.main.expand_now()

    def has_retreated(self, unit):
        """Identify if the unit has retreated(a little bugged it doesn't always clean it)"""
        if self.main.townhalls.closer_than(15, unit):
            self.retreat_units.remove(unit.tag)

    def delegate_idle_unit(self, unit):
        """
        Control the idle units, by gathering then or telling then to attack
        Parameters
        ----------
        unit: Unit from the attacking force

        Returns
        -------
        True and the action(attack starting enemy location or retreat) if it meets the conditions
        """
        if (
            self.main.townhalls
            and not self.main.counter_attack_vs_flying
            and self.gathering_force_value(1, 2, 4) < 42
            and self.retreat_units
        ):
            self.move_to_rallying_point(self.targets, unit)
            return True
        if not self.main.close_enemy_production or self.main.time >= 480:
            if self.main.townhalls:
                self.attack_closest_building(unit)
            return self.attack_start_location(unit)
        return False

    def keep_attacking(self, unit):
        """
        It keeps the attack going if it meets the requirements no matter what
        Parameters
        ----------
        unit: Unit from the attacking force

        Returns
        -------
        True and the action(just attack the closest structure or closest enemy) if it meets the conditions
        """
        if not self.retreat_units or self.main.close_enemies_to_base:
            if self.main.enemy_structures:
                self.main.add_action(unit.attack(self.main.enemy_structures.closest_to(unit.position)))
                return True
            if self.targets:
                self.main.add_action(unit.attack(self.targets.closest_to(unit.position)))
                return True
            return False
        return False

    def set_unit_groups(self):
        """Set the targets and atk_force, separating then by type"""
        if self.main.enemies:
            excluded_units = {
                UnitTypeId.ADEPTPHASESHIFT,
                UnitTypeId.DISRUPTORPHASED,
                UnitTypeId.EGG,
                UnitTypeId.LARVA,
                UnitTypeId.INFESTEDTERRANSEGG,
                UnitTypeId.INFESTEDTERRAN,
            }
            filtered_enemies = self.main.enemies.not_structure.exclude_type(excluded_units)
            enemy_base_on_construction = self.main.enemy_structures.filter(
                lambda base: base.type_id in {UnitTypeId.NEXUS, UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY}
                and 0 < base.build_progress < 1
            )
            static_defence = self.main.enemy_structures.of_type(
                {UnitTypeId.SPINECRAWLER, UnitTypeId.PHOTONCANNON, UnitTypeId.BUNKER, UnitTypeId.PLANETARYFORTRESS}
            )
            self.targets = static_defence | filtered_enemies.not_flying | enemy_base_on_construction
            self.hydra_targets = (
                static_defence | filtered_enemies.filter(lambda unit: not unit.is_snapshot) | enemy_base_on_construction
            )
        self.atk_force = self.main.units.of_type(self.army_types)
        if self.main.floated_buildings_bm and self.main.supply_used >= 199:
            self.atk_force = self.atk_force | self.main.queens

    def target_buildings(self, unit):
        """
        Target close buildings if no other target is available
        Parameters
        ----------
        unit: Unit from the attacking force

        Returns
        -------
        True and the action(just attack closer structures) if it meets the conditions
        """
        if self.main.enemy_structures.closer_than(30, unit.position):
            self.main.add_action(unit.attack(self.main.enemy_structures.closest_to(unit.position)))
            return True
        return False
