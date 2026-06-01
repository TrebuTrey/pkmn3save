import struct
import sys
from functools import cached_property
from pkmn3save.mapping import BinaryChunk, DataMapping
from pkmn3save.data_types.pokemon import Pokemon
import typing
if typing.TYPE_CHECKING:
    from . import GameSave

SECTION_ID = 1

# struct "L" (unsigned long) is 4 bytes on Windows but 8 bytes on macOS/Linux,
# which causes "unpack requires a buffer of 8 bytes" on non-Windows platforms.
# "<I" is always 4 bytes little-endian on every platform and produces the same
# numeric result as "L" on Windows, so it is the correct portable format.
_TEAM_SIZE_FMT = "L" if sys.platform == "win32" else "<I"


class TeamItems(DataMapping):
    _TEAM_SIZE    = BinaryChunk(0x0234, 4)
    _POKEMON_LIST = BinaryChunk(0x0238, 600)

    @classmethod
    def from_game_save(cls, save: 'GameSave'):
        return cls(save.sections[SECTION_ID])

    @cached_property
    def team_size(self) -> int:
        data = self._TEAM_SIZE(self.data)
        num = struct.unpack(_TEAM_SIZE_FMT, data)
        return num[0]

    @cached_property
    def team(self) -> list[Pokemon]:
        team_data = self._POKEMON_LIST(self.data)
        team = []
        for i in range(self.team_size):
            start = 100 * i
            end   = start + 100
            team.append(Pokemon(team_data[start:end]))
        return team


class TeamItemsLGFR(TeamItems):
    _TEAM_SIZE    = BinaryChunk(0x0034, 4)
    _POKEMON_LIST = BinaryChunk(0x0038, 600)
