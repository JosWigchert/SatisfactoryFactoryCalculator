from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Item:
    name: str
    id: Optional[int] = None


@dataclass
class Machine:
    name: str
    id: Optional[int] = None


@dataclass
class Recipe:
    item: Item
    output_amount: int
    machine: Machine
    inputs: Dict[Item, int]
    id: Optional[int] = None
