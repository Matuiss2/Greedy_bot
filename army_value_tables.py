from sc2.constants import (
    COLUSSUS,
    ADEPT,
    ARCHON,
    STALKER,
    DARKTEMPLAR,
    PHOTONCANNON,
    ZEALOT,
    SENTRY,
    PROBE,
    HIGHTEMPLAR,
    PHOENIX,
    ORACLE,
    MOTHERSHIP,
    IMMORTAL,
    DISRUPTOR,
    CARRIER,
    TEMPEST,
    VOIDRAY,
)


class EnemyArmyValue:
    def __init__(self):
        self.massive_counter = 4
        self.counter = 3
        self.advantage = 2
        self.normal = 1
        self.countered = 0.5
        self.massive_countered = 0.25

    def general_calculation(self, table):
        total = 0
        for enemy in self.enemies:
            total += table[enemy.type_id]
        return total

    def protoss_value_for_zergling(self):
        protoss_as_zergling_table = {
            COLUSSUS: self.massive_counter,
            ADEPT: self.counter,
            ARCHON: self.counter,
            STALKER: self.normal,
            DARKTEMPLAR: self.normal,
            PHOTONCANNON: self.counter,
            ZEALOT: self.advantage,
            SENTRY: self.countered,
            PROBE: 0.1,
            HIGHTEMPLAR: self.countered,
            DISRUPTOR: self.counter,
            IMMORTAL: self.advantage,
        }
        return self.general_calculation(protoss_as_zergling_table)

    def protoss_value_for_hydralisks(self):
        protoss_as_hydralisks_table = {
            PHOENIX: self.countered,
            ORACLE: self.normal,
            COLUSSUS: self.counter,
            ADEPT: self.advantage,
            ARCHON: self.advantage,
            STALKER: self.normal,
            DARKTEMPLAR: self.countered,
            PHOTONCANNON: self.counter,
            ZEALOT: self.normal,
            SENTRY: self.massive_countered,
            PROBE: 0.1,
            HIGHTEMPLAR: self.countered,
            CARRIER: self.counter,
            DISRUPTOR: self.advantage,
            IMMORTAL: self.counter,
            TEMPEST: self.advantage,
            VOIDRAY: self.normal,
        }
        return self.general_calculation(protoss_as_hydralisks_table)
