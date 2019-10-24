import logging

from s2clientprotocol import sc2api_pb2 as sc_pb

from .player import Computer
from .protocol import Protocol

LOGGER = logging.getLogger(__name__)


class Controller(Protocol):
    def __init__(self, ws, process):
        super().__init__(ws)
        self.__process = process

    @property
    def running(self):
        return self.__process._process is not None

    async def create_game(self, game_map, players, realtime, random_seed=None):
        if not isinstance(realtime, bool):
            raise AssertionError()
        req = sc_pb.RequestCreateGame(local_map=sc_pb.LocalMap(map_path=str(game_map.relative_path)), realtime=realtime)
        if random_seed is not None:
            req.random_seed = random_seed

        for player in players:
            player_setup = req.player_setup.add()
            player_setup.type = player.type.value
            if isinstance(player, Computer):
                player_setup.race = player.race.value
                player_setup.difficulty = player.difficulty.value
                player_setup.ai_build = player.ai_build.value

        LOGGER.info("Creating new game")
        LOGGER.info(f"Map:     {game_map.name}")
        LOGGER.info(f"Players: {', '.join(str(p) for p in players)}")
        result = await self._execute(create_game=req)
        return result
