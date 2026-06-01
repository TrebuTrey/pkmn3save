import enum
import struct
import sys
from pkmn3save.mapping import BinaryChunk
from pkmn3save.data_types.strings import to_ascii
import typing
if typing.TYPE_CHECKING:
    from . import GameSave

SECTION_ID = 0
NAME       = BinaryChunk(0x0, 7)
GENDER     = BinaryChunk(0x8, 1)
GAME_CODE  = BinaryChunk(0x00AC, 4)

# struct "L" (unsigned long) is 4 bytes on Windows but 8 bytes on macOS/Linux,
# which causes "unpack requires a buffer of 8 bytes" on non-Windows platforms.
# "<I" is always 4 bytes little-endian on every platform and produces the same
# numeric result as "L" on Windows, so it is the correct portable format.
_GAME_CODE_FMT = "L" if sys.platform == "win32" else "<I"


class GameCode(enum.Enum):
    RUBY_SAPPHIRE      = 0x00000000
    FIRERED_LEAFGREEN  = 0x00000001
    EMERALD            = None


class Gender(enum.Enum):
    BOY  = 0x00
    GIRL = 0x01


class TrainerInfo:
    def __init__(self, data: bytes):
        self.data = data

    @classmethod
    def from_game_save(cls, save: 'GameSave'):
        return cls(save.sections[SECTION_ID])

    @property
    def name(self) -> str:
        return to_ascii(NAME(self.data))

    @property
    def gender(self) -> Gender:
        return Gender(GENDER(self.data)[0])

    @property
    def game_code(self) -> GameCode:
        data = GAME_CODE(self.data)
        num = struct.unpack(_GAME_CODE_FMT, data)
        try:
            return GameCode(num)
        except ValueError:
            return GameCode.EMERALD

    def __str__(self):
        return (f"TrainerInfo(name={self.name}, gender={self.gender}, "
                f"game_code={self.game_code})")
