# Another exception, using third party lib for Part 2.
import os
import re

from typing import Iterator, NamedTuple

from shapely import Polygon
from shapely.ops import unary_union, clip_by_rect


__here__ = os.path.dirname(__file__)

with open(os.path.join(__here__, 'test_data.txt'), 'r') as fp:
    TEST_DATA = fp.read()


class Pt(NamedTuple):
    x: int
    y: int

    def distance_to(self, other: 'Pt') -> int:
        # returns manhattan distance from self to other.
        a = self
        b = other
        return abs(a.x - b.x) + abs(a.y - b.y)


class RegionSpan(NamedTuple):
    xmin: int
    xmax: int
    ymin: int
    ymax: int


class Region(NamedTuple):
    origin: Pt
    radius: int

    @property
    def span(self) -> RegionSpan:
        o = self.origin
        r = self.radius

        return RegionSpan(
            xmin=o.x - r,
            xmax=o.x + r,
            ymin=o.y - r,
            ymax=o.y + r,
        )

    def y_coverage(self, y: int) -> set[Pt]:
        # generates points covered by the region at given y coordinate.
        span = self.span
        if not span.ymin <= y <= span.ymax:
            # given y is outside the region.
            return set()

        points = set()
        for x in range(span.xmin, span.xmax + 1):
            # Collect all points that are within the region.
            # This can probably be done analytically, but is left as an excercise ;)
            p = Pt(x, y)
            if self.origin.distance_to(p) <= self.radius:
                points.add(p)

        return points

    @property
    def polygon(self):
        s = self.span
        o = self.origin
        return Polygon([
            (o.x, s.ymin),
            (s.xmax, o.y),
            (o.x, s.ymax),
            (s.xmin, o.y),
        ])


def parse_input(data: str) -> Iterator[tuple[Pt, Pt]]:
    pattern = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'

    for line in data.splitlines():
        s_x, s_y, b_x, b_y = map(int, re.match(pattern, line).groups())
        yield Pt(s_x, s_y), Pt(b_x, b_y)


def beacon_sensor(data: str, y: int):
    regions = []
    beacons = []

    for sensor, beacon in parse_input(data):
        radius = sensor.distance_to(beacon)
        regions.append(Region(origin=sensor, radius=radius))
        beacons.append(beacon)

    # Find the "coverage" of the regions are given y position. This is for Part
    # 1 and may be made performant by using shapely here as well. However the
    # original solution runs in <30s (haha), and it is verbatim so I kept it.
    coverage = set()

    print('Enumerating lots of points. It will take some time...')

    for r in regions:
        coverage |= r.y_coverage(y)

    # Converage also includes the points where beacons may be located.
    # We now remove the beacon positions
    coverage -= set(beacons)

    yield len(coverage)

    # Part 2 cannot be realistically solved with this method. We are using
    # shapely (based on suggestions on reddit) to skip iterating all the points
    # and instead use the geometrical approach. All diamond shaped regions are
    # merged together to form a planar region. This region then is intersected
    # with a bounding box. Within this region, we will have hole corresponding
    # to the beacon not received by other sensors.
    rmax = 4_000_000

    all_regions = unary_union([r.polygon for r in regions])
    interior = clip_by_rect(all_regions, 0, 0, rmax, rmax).interiors[0]
    distress_beacon = interior.centroid.coords[:][0]
    x, y = map(round, distress_beacon)

    yield x * rmax + y


if __name__ == '__main__':
    test_case = beacon_sensor(TEST_DATA, y=10)
    assert next(test_case) == 26
    assert next(test_case) == 56000011

    with open(os.path.join(__here__, 'input.txt'), 'r') as fp:
        data = fp.read()

    answers = beacon_sensor(data, y=2_000_000)
    print(f'answer_1={next(answers)}')
    print(f'answer_2={next(answers)}')
