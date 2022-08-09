from dataclasses import dataclass


@dataclass
class Intervals:
    values: list
    status: bool


def d_percent_to_float(percentage: str) -> float:
    """
    31.3% -> 31.3 type float
    """
    percentage = percentage.replace("%", "")
    percentage = float(percentage)
    return percentage


def equal_status_interval(d_percent_str: str, intervals: Intervals):
    d_percent_float = d_percent_to_float(d_percent_str)

    start_len = len(intervals.values)
    intervals.values = [x for x in intervals.values if x > d_percent_float]
    after_len = len(intervals.values)
    if start_len == after_len:
        intervals.status = False
    else:
        intervals.status = True
    return intervals


if __name__ == "__main__":
    intervals = Intervals(list(range(0, 105, 5)), False)
    print(type(intervals))

    intervals = equal_status_interval("20%", intervals)

    print(intervals, type(intervals))

    intervals = equal_status_interval("30%", intervals)

    print(intervals, type(intervals))

    intervals = equal_status_interval("32%", intervals)

    print(intervals, type(intervals))

    intervals = equal_status_interval("50%", intervals)

    print(intervals, type(intervals))
