"""Everything related to the expansion logic goes here"""
from sc2.constants import HATCHERY


class BuildExpansion:
    """Ok for now"""

    def __init__(self, ai):
        self.ai = ai
        self.worker_to_first_base = False

    async def should_handle(self, iteration):
        """Good for now, maybe the 7th or more hatchery can be postponed
         for when extra mining patches or production are needed """
        local_controller = self.ai
        base = local_controller.townhalls
        base_amount = len(base)
        game_time = local_controller.time
        if not self.worker_to_first_base and base_amount == 1 and local_controller.minerals > 225:
            self.worker_to_first_base = True
            return True

        if (
            base
            and local_controller.can_afford(HATCHERY)
            and not local_controller.close_enemies_to_base
            and (not local_controller.close_enemy_production or game_time > 690)
        ):
            if not local_controller.already_pending(HATCHERY):
                if not (
                    local_controller.enemy_structures.closer_than(50, local_controller.start_location)
                    and game_time < 300
                ):
                    if base_amount <= 5:
                        return len(local_controller.zerglings) > 19 or game_time >= 285 if base_amount == 2 else True
                    return local_controller.caverns
                return False
            return False
        return False

    async def handle(self, iteration):
        """Expands to the nearest expansion location using the nearest drone to it"""
        local_controller = self.ai
        action = local_controller.add_action
        if self.worker_to_first_base:
            action(await self.send_worker_to_next_expansion())
            self.worker_to_first_base = False
            return True
        for expansion in local_controller.ordered_expansions:
            if await local_controller.can_place(HATCHERY, expansion):
                if local_controller.workers:
                    drone = local_controller.workers.closest_to(expansion)
                    action(drone.build(HATCHERY, expansion))
                    return True
        return False

    async def send_worker_to_next_expansion(self):
        """Send the worker to the first expansion so its placed faster"""
        local_controller = self.ai
        worker = local_controller.workers.gathering.first
        return worker.move(await local_controller.get_next_expansion())
