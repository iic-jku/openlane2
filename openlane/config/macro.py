from decimal import Decimal
from dataclasses import dataclass, field
from typing import Dict, Literal, Optional, Tuple, List, Union

from ..state import Path, DesignFormat


@dataclass
class Instance:
    """
    Location information for an instance of a Macro.

    :param location: The physical co-ordinates of the Macro's origin.
    :param orientation: Whether the Macro is facing North or South.
    """

    location: Tuple[Decimal, Decimal]
    orientation: Union[Literal["N"], Literal["S"]]


@dataclass
class Macro:
    """
    A data structure for storing definitions of Macros.

    As it is typically stored in a dictionary in its superclass, the module name
    is not stored in any of these fields.

    You will note most fields correspond to a :class:`openlane.state.DesignFormat`
    entry IDs. This is not coincidental.

    :param gds: A list of GDSII files representing the design. At least one is required.
    :param lef: A list of LEF files representing the design. At least one is required.
    :param instances: A dictionary of :class:`Instance` objects representing the
        instances of said macro.

        The keys for the dictionaries are the names of the instances.
    :param nl: A list of netlists constituting the design.

        The netlists must be valid Verilog netlists readable by tools such as
        OpenSTA.

        Can be empty, however SPEF-based hierarchical static timing analysis
        will be unavailable.
    :param spef: A dictionary of parasitics annotations for the various netlists of the
        Macro.

        The keys are wildcards for timing corners supported by a certain SPEF file.

        Can be empty, however SPEF-based hierarchical static timing analysis
        will be unavailable.
    :param lib: A dictionary of timing library files.

        The keys are wildcards for timing corners supported by a certain LIB file.

        If both SPEF and LIB views are empty, the design may be black-boxed
        during STA.
    :param spice: A list of SPICE netlists constituting the design. May be
        useful in some flows.
    :param sdf: A dictionary of standard delay format files. May be useful in some flows.

        The keys are wildcards for timing corners supported by a certain SPEF file.
    :param json_h: A JSON file as generated by Yosys. Helpful in some flows.
    """

    gds: List[Path]
    lef: List[Path]
    instances: Dict[str, Instance] = field(default_factory=lambda: {})

    nl: List[Path] = field(default_factory=lambda: [])
    spef: Dict[str, List[Path]] = field(default_factory=lambda: {})
    lib: Dict[str, List[Path]] = field(default_factory=lambda: {})
    spice: List[Path] = field(default_factory=lambda: [])
    sdf: Dict[str, List[Path]] = field(default_factory=lambda: {})

    json_h: Optional[Path] = None

    def view_by_df(
        self, df: DesignFormat
    ) -> Union[None, Path, List[Path], Dict[str, List[Path]]]:
        return getattr(self, df.value.id)

    def __post_init__(self):
        if len(self.gds) < 1:
            raise ValueError(
                "Invalid Macro definition- at least one GDSII file must be specified."
            )
        if len(self.lef) < 1:
            raise ValueError(
                "Invalid Macro definition- at least one LEF file must be specified."
            )
