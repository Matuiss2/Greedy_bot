# 167 army - and (not self.close_enemy_production or self.time > 300)
# Spore placement

self.enemy_natural_expansion = False
if base_amount <= 4:
    if (base_amount == 2 and self.enemy_natural_expansion) or self.time > 400:
        if self.spines or self.time > 330:
            await self.expand_now()


if (len(self.spines) + self.already_pending(SPINECRAWLER) < 2 <= len(base.ready)
    and self.time <= 360
    or (self.close_enemy_production
        and self.time <= 300
        and len(self.spines) + self.already_pending(SPINECRAWLER)
        < len(self.known_enemy_structures.of_type({BARRACKS, GATEWAY}).closer_than(50, self.start_location)))
or (len(self.spines) + self.already_pending(SPINECRAWLER) < 5 and not self.enemy_natural_expansion)):
                await self.build(
                    SPINECRAWLER,
                    near=self.townhalls.closest_to(self._game_info.map_center).position.towards(
                        self._game_info.map_center, 9
                    ),
                )






