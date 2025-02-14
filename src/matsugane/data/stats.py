from statistics import mean, median, mode, pstdev
from typing import List

from attrs import define


@define
class Stats:
    items: List[int]

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def average(self) -> float:
        if self.total == 0:
            return 0.0
        return mean(self.items)

    @property
    def median(self) -> float:
        if self.total == 0:
            return 0.0
        return median(self.items)

    @property
    def mode(self) -> int:
        if self.total == 0:
            return 0
        return mode(self.items)

    @property
    def stddev(self) -> float:
        if self.total == 0:
            return 0.0
        return pstdev(self.items)

    @property
    def lower_limit(self) -> float:
        if self.total == 0:
            return 0.0

        result = self.average - (2 * self.stddev)
        if result <= 1.0:
            return 1.0
        return result

    @property
    def upper_limit(self) -> float:
        if self.total == 0:
            return 0.0

        return self.average + (2 * self.stddev)

    @property
    def items_exceeding_upper_limit(self) -> int:
        if self.items == 0:
            return 0

        return len([item for item in self.items if item > self.upper_limit])
