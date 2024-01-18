"""
https://codebunk.com/b/5581100639615/

# Основное задание

# Задача: по входным свечкам построить свечи объемов.

# Свеча: ts_open, ts_close, open, close, low, high, volume - в тест кейсах

"""


from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from utils import division, pop_last_if_exists


def print_result(res: Iterable[Any]) -> None:
    for candle in res:
        print(candle)


@dataclass(slots=True)
class Candle:
    ts_open: float
    ts_close: float
    open: float
    close: float
    low: float
    high: float
    volume: float


@dataclass(slots=True)
class TemporaryCandle(Candle):
    ...


@dataclass(slots=True)
class CandleAggregator:
    candles: Sequence[Candle]
    volume: float

    @staticmethod
    def distribute_identical_candles(
        candle: Candle, candle_whole_ts_close: float, candle_whole_duration: float, candle_count: int, volume: float
    ) -> list[Candle]:
        lst = [
            Candle(
                ts_open=candle.ts_open,
                ts_close=round(candle_whole_ts_close, 2),
                open=candle.open,
                close=candle.close,
                low=candle.low,
                high=candle.high,
                volume=volume,
            )
        ]
        for count in range(1, candle_count):
            candle_whole_ts_close += candle_whole_duration
            candle_whole_ts_open = lst[-1].ts_close
            lst += [
                Candle(
                    ts_open=round(candle_whole_ts_open, 2),
                    ts_close=round(candle_whole_ts_close, 2),
                    open=candle.open,
                    close=candle.close,
                    low=candle.low,
                    high=candle.high,
                    volume=volume,
                )
            ]
        return lst

    @classmethod
    def split_candle(cls, candle: Candle, volume: float) -> Sequence[Candle | TemporaryCandle]:
        candle_count, remaind = division(candle.volume, volume)
        candle_duration = candle.ts_close - candle.ts_open
        percent_duration = candle_duration / candle.volume
        if remaind:
            candle_temp_ts_open = round(candle.ts_close - (percent_duration * remaind), 2)
            temp_candle = TemporaryCandle(
                ts_open=candle_temp_ts_open,
                ts_close=candle.ts_close,
                open=candle.open,
                close=candle.close,
                low=candle.low,
                high=candle.high,
                volume=remaind,
            )
            candle_whole_duration = (candle_temp_ts_open - candle.ts_open) / candle_count
            candle_whole_ts_close = candle.ts_open + candle_whole_duration
            lst = cls.distribute_identical_candles(
                candle=candle,
                candle_whole_ts_close=candle_whole_ts_close,
                candle_whole_duration=candle_whole_duration,
                candle_count=candle_count,
                volume=volume,
            )
            lst += [temp_candle]
            return lst

        candle_whole_duration = candle_duration / candle_count
        candle_whole_ts_close = candle.ts_open + candle_whole_duration
        lst = cls.distribute_identical_candles(
            candle=candle,
            candle_whole_ts_close=candle_whole_ts_close,
            candle_whole_duration=candle_whole_duration,
            candle_count=candle_count,
            volume=volume,
        )
        lst[-1].ts_close = candle.ts_close
        return lst

    @classmethod
    def combine_candles(
        cls, candles: Sequence[Candle | TemporaryCandle], volume: float
    ) -> Sequence[Candle | TemporaryCandle]:
        combine_volume = sum(candle.volume for candle in candles)
        ts_open = candles[0].ts_open
        ts_close = candles[-1].ts_close
        open = candles[0].open
        close = candles[-1].close
        low = min(candle.low for candle in candles)
        high = max(candle.high for candle in candles)

        if combine_volume == volume:
            volume_candle = Candle(
                ts_open=ts_open, ts_close=ts_close, open=open, close=close, low=low, high=high, volume=combine_volume
            )
            return [volume_candle]

        if combine_volume < volume:
            temp_candle = TemporaryCandle(
                ts_open=ts_open, ts_close=ts_close, open=open, close=close, low=low, high=high, volume=combine_volume
            )
            return [temp_candle]

        if combine_volume > volume:
            candle = Candle(
                ts_open=ts_open, ts_close=ts_close, open=open, close=close, low=low, high=high, volume=combine_volume
            )
            return cls.split_candle(candle, volume)

        return candles

    @staticmethod
    def check_last_candle_is_not_temp(candles: Sequence[Any]) -> bool:
        if isinstance(candles[-1], TemporaryCandle):
            return False
        return True

    @property
    def volume_candles(self) -> Sequence[Candle | TemporaryCandle]:
        volume_candles_lst: list[Candle | TemporaryCandle] = []
        temp_candles_lst: list[Candle | TemporaryCandle] = []

        for candle in self.candles:
            if len(temp_candles_lst) > 0:
                temp_candles_lst += [candle]
                combine_candles_lst = self.combine_candles(temp_candles_lst, self.volume)
                pop_last_if_exists(volume_candles_lst)
                volume_candles_lst += combine_candles_lst
                if self.check_last_candle_is_not_temp(volume_candles_lst):
                    continue
                candle = volume_candles_lst[-1]

            if candle.volume == self.volume:
                volume_candles_lst += [candle]

            if candle.volume > self.volume:
                split_candles_lst = self.split_candle(candle, self.volume)
                volume_candles_lst += split_candles_lst
                temp_candles_lst += [volume_candles_lst[-1]]

            if candle.volume < self.volume:
                temp_candles_lst = [candle]

        return volume_candles_lst


def agg_volume_candles(candles: Sequence[Candle], volume: float) -> Sequence[Candle | TemporaryCandle]:
    return CandleAggregator(candles, volume).volume_candles


print("test_candles_1")
test_candles_1 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 100),
]
result = agg_volume_candles(test_candles_1, 100)
assert len(result) == 1
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_2")
test_candles_2 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 150),
]
result = agg_volume_candles(test_candles_2, 100)
assert len(result) == 2
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_3")
test_candles_3 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 300),
]
result = agg_volume_candles(test_candles_3, 100)
assert len(result) == 3
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_4")
test_candles_4 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 333),
]
result = agg_volume_candles(test_candles_4, 100)
assert len(result) == 4
assert result[-1].volume == 33
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_5")
test_candles_5 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 200),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 650),
]
result = agg_volume_candles(test_candles_5, 100)
assert len(result) == 9
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_6")
test_candles_6 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 200),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 650),
    Candle(1200, 1300, 1350, 1400, 1330, 1410, 100),
    Candle(1300, 1400, 1400, 1350, 1340, 1410, 100),
    Candle(1400, 1500, 1350, 1370, 1345, 1350, 100),
    Candle(1500, 1600, 1370, 1480, 1350, 1500, 300),
]
result = agg_volume_candles(test_candles_6, 100)
assert len(result) == 15
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_7")
test_candles_7 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
    Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
    Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
    Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
    Candle(1500, 1600, 1370, 1480, 1350, 1500, 10),
]
result = agg_volume_candles(test_candles_7, 100)
assert len(result) == 1
assert result[-1].volume == 70
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_8")
test_candles_8 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
    Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
    Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
    Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
    Candle(1500, 1600, 1370, 1480, 1350, 1500, 40),
]
result = agg_volume_candles(test_candles_8, 100)
assert len(result) == 1
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_9")
test_candles_9 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
    Candle(1100, 1200, 1450, 1500, 1400, 1500, 10),
    Candle(1200, 1300, 1500, 1450, 1000, 2000, 10),
    Candle(1300, 1400, 1450, 1500, 1400, 1500, 10),
    Candle(1400, 1500, 1500, 1450, 1400, 1500, 10),
]
result = agg_volume_candles(test_candles_9, 19)
assert len(result) == 3
assert result[-1].volume == 12
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


print("test_candles_add_1")
test_candles_add_1 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 99),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 99),
    Candle(1200, 1300, 1450, 1350, 1250, 1460, 2),
]
result = agg_volume_candles(test_candles_add_1, 100)
assert len(result) == 2
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)

print("test_candles_add_2")
test_candles_add_2 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 100),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 150),
    Candle(1200, 1300, 1350, 1400, 1330, 1410, 100),
]

result = agg_volume_candles(test_candles_add_2, 100)
assert len(result) == 4
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)
