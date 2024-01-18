def division(dividend: float, divisor: float) -> tuple[int, float]:
    whole_part = dividend // divisor
    remainder = dividend % divisor
    return int(whole_part), remainder


def pop_last_if_exists(volume_candles_lst: list) -> None:
    if len(volume_candles_lst) > 0:
        volume_candles_lst.pop()
