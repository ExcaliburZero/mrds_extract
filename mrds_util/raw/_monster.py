from typing import Annotated

import dataclasses_struct as dcs

from mrds_util.raw._util import BinaryReadWriteable


@dcs.dataclass_struct(size="std", byteorder="little")
class Monster(BinaryReadWriteable):
    name: Annotated[bytes, 10]  # TODO: figure out correct number
    unknown: Annotated[bytes, 410]
