"""Hourly footfall aggregation for retail entrance analytics"""
from datetime import datetime
from collections import OrderedDict

from logger import logger


class HourlyAggregator:
    """
    Buckets in/out counts into hourly windows keyed by hour-start timestamp.
    Consumes cumulative counts from LineCounter and computes per-hour deltas,
    since LineCounter tracks running totals, not per-window counts.
    """

    def __init__(self):
        self._hourly_data: "OrderedDict[str, dict]" = OrderedDict()
        self._last_in_total = 0
        self._last_out_total = 0
        logger.info("HourlyAggregator initialized")

    @staticmethod
    def _hour_key(ts: datetime) -> str:
        return ts.strftime("%Y-%m-%d %H:00")

    def update(self, counts: dict, timestamp: datetime = None) -> dict:
        try:
            timestamp = timestamp or datetime.now()
            hour_key = self._hour_key(timestamp)

            in_total = counts.get("in_count", 0)
            out_total = counts.get("out_count", 0)

            in_delta = in_total - self._last_in_total
            out_delta = out_total - self._last_out_total

            self._last_in_total = in_total
            self._last_out_total = out_total

            if hour_key not in self._hourly_data:
                self._hourly_data[hour_key] = {"in": 0, "out": 0}
                logger.info("New hour bucket started: {}", hour_key)

            self._hourly_data[hour_key]["in"] += in_delta
            self._hourly_data[hour_key]["out"] += out_delta

            return self._hourly_data[hour_key]
        except Exception:
            logger.exception("Error updating hourly aggregator")
            raise

    def get_report(self) -> list[dict]:
        """Returns hourly rows with peak/off-peak classification for completed hours."""
        rows = []
        totals = [(h, d["in"] + d["out"]) for h, d in self._hourly_data.items()]

        if not totals:
            return rows

        counts_only = sorted(t[1] for t in totals)
        n = len(counts_only)
        low_cutoff = counts_only[int(n * 0.25)] if n >= 4 else counts_only[0]
        high_cutoff = counts_only[int(n * 0.75)] if n >= 4 else counts_only[-1]

        for hour, data in self._hourly_data.items():
            total = data["in"] + data["out"]
            if total >= high_cutoff and total > 0:
                level = "PEAK"
            elif total <= low_cutoff:
                level = "LOW"
            else:
                level = "MODERATE"

            rows.append({
                "hour": hour,
                "in_count": data["in"],
                "out_count": data["out"],
                "total": total,
                "traffic_level": level,
            })

        return rows

    def export_csv(self, path: str = "footfall_report.csv"):
        import csv

        report = self.get_report()
        if not report:
            logger.warning("No data to export")
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["hour", "in_count", "out_count", "total", "traffic_level"])
                writer.writeheader()
                writer.writerows(report)
            logger.info("Exported hourly report to {}", path)
        except Exception:
            logger.exception("Failed to export CSV to {}", path)
            raise