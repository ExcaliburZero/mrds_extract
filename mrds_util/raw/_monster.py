from typing import Annotated

import dataclasses_struct as dcs

from mrds_util.raw._util import BinaryReadWriteable


@dcs.dataclass_struct(size="std", byteorder="little")
class Monster(BinaryReadWriteable):
    name: Annotated[bytes, 12]  # TODO: figure out correct number
    unknown_a: Annotated[bytes, 28]
    power: dcs.U16
    intelligence: dcs.U16
    skill: dcs.U16
    speed: dcs.U16
    defense: dcs.U16
    life: dcs.U16
    unknown: Annotated[bytes, 368]
