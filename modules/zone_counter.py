"""Line-crossing counter for footfall analytics"""
from logger import logger


class LineCounter:
    """
    Counts unique track crossings over a line segment defined by two points.

    Crossing direction is determined via the sign of the cross product between
    the line vector and the vector from line_start to the object's centroid.
    Each track id is counted once per crossing event (not per frame), and once
    counted is not re-counted unless reset_track() is called — this avoids
    jitter near the line inflating counts on a single crossing.
    """

    def __init__(self, line_start: tuple, line_end: tuple):
        self.line_start = line_start
        self.line_end = line_end

        self._track_sides: dict[int, int] = {}
        self._counted_ids: set[int] = set()

        self.in_count = 0
        self.out_count = 0

        logger.info("LineCounter initialized with line {} -> {}", line_start, line_end)

    def _side_of_line(self, point: tuple) -> int:
        x1, y1 = self.line_start
        x2, y2 = self.line_end
        px, py = point

        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)

        if cross > 0:
            return 1
        if cross < 0:
            return -1
        return 0

    @staticmethod
    def _centroid(box: tuple) -> tuple:
        x1, y1, x2, y2 = box
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def update(self, tracked_objects) -> dict:
        try:
            for obj in tracked_objects:
                x1, y1, x2, y2, track_id = map(int, obj[:5])
                centroid = self._centroid((x1, y1, x2, y2))
                current_side = self._side_of_line(centroid)

                previous_side = self._track_sides.get(track_id)

                if (
                    previous_side is not None
                    and current_side != 0
                    and previous_side != current_side
                    and track_id not in self._counted_ids
                ):
                    if previous_side == -1 and current_side == 1:
                        self.in_count += 1
                        logger.debug("Track {} crossed IN. Total in={}", track_id, self.in_count)
                    elif previous_side == 1 and current_side == -1:
                        self.out_count += 1
                        logger.debug("Track {} crossed OUT. Total out={}", track_id, self.out_count)

                    self._counted_ids.add(track_id)

                if current_side != 0:
                    self._track_sides[track_id] = current_side

            return {
                "in_count": self.in_count,
                "out_count": self.out_count,
                "total": self.in_count + self.out_count,
            }
        except Exception:
            logger.exception("Error updating line counter")
            raise

    def reset_track(self, track_id: int):
        """Allow a track id to be counted again (e.g. after long absence / id reuse)."""
        self._track_sides.pop(track_id, None)
        self._counted_ids.discard(track_id)