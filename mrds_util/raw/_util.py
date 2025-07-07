import abc
from collections.abc import Callable
from typing import IO, Optional, Protocol, Self, cast


class BinaryRwNotDataclassStructError(TypeError):
    def __init__(self, cls: type):
        super().__init__(
            f"Binary read/writeable class must be a dataclass-struct, but is not: {cls.__name__}"
        )


class DataclassStructProtocol(Protocol):
    size: int


class BinaryReadWriteable(abc.ABC):  # noqa: B024
    """
    Abstract class that adds write_bin and from_bin methods to a dataclass struct.

    The implementations use getattr to fail with an exception if misused and also keep the
    typechecker happy.
    """

    def write_bin(self, output_stream: IO[bytes]) -> None:
        """
        Writes the data as binary to the given output stream.
        """
        pack = cast("Optional[Callable[[], bytes]]", getattr(self, "pack", lambda: None))
        if pack is None:
            raise BinaryRwNotDataclassStructError(self.__class__)

        output_stream.write(pack())

    @classmethod
    def from_bin(cls, input_stream: IO[bytes]) -> Self:
        """
        Reads the data from the given binary input stream.
        """
        from_packed = cast(
            "Optional[Callable[[bytes], Self]]", getattr(cls, "from_packed", lambda: None)
        )
        if from_packed is None:
            raise BinaryRwNotDataclassStructError(cls)

        struct_info = cast(
            "Optional[DataclassStructProtocol]", getattr(cls, "__dataclass_struct__", lambda: None)
        )
        if struct_info is None:
            raise BinaryRwNotDataclassStructError(cls)

        return from_packed(input_stream.read(struct_info.size))
