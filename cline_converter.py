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
class VolumeCandle:
    ts_open: float
    ts_close: float
    volume: float


@dataclass(slots=True)
class TemporaryCandle(VolumeCandle):
    ...


@dataclass(slots=True)
class CandleAggregator:
    candles: Sequence[Candle | VolumeCandle]
    volume: float

    @classmethod
    def split_candle(cls, candle: Candle | VolumeCandle, volume: float) -> Sequence[VolumeCandle | TemporaryCandle]:
        candle_count, remaind = division(candle.volume, volume)
        volume_candle = VolumeCandle(ts_open=0, ts_close=0, volume=volume)
        lst = [volume_candle] * candle_count
        if remaind:
            temp_candle = TemporaryCandle(
                ts_open=volume_candle.ts_open,
                ts_close=volume_candle.ts_close,
                volume=volume_candle.volume,
            )
            temp_candle.volume = remaind
            lst += [temp_candle]
        return lst

    @classmethod
    def combine_candles(
        cls, candles: Sequence[VolumeCandle | TemporaryCandle], volume: float
    ) -> Sequence[VolumeCandle | TemporaryCandle]:
        combine_volume = sum(candle.volume for candle in candles)
        ts_open = candles[0].ts_open
        ts_close = candles[-1].ts_close
        if combine_volume == volume:
            volume_candle = VolumeCandle(
                ts_open=ts_open,
                ts_close=ts_close,
                volume=combine_volume,
            )
            return [volume_candle]

        if combine_volume < volume:
            temp_candle = TemporaryCandle(
                ts_open=ts_open,
                ts_close=ts_close,
                volume=combine_volume,
            )
            return [temp_candle]

        if combine_volume > volume:
            candle = VolumeCandle(
                ts_open=ts_open,
                ts_close=ts_close,
                volume=combine_volume,
            )
            return cls.split_candle(candle, volume)

        return [VolumeCandle(ts_open=ts_open, ts_close=ts_close, volume=combine_volume)]

    @staticmethod
    def check_last_candle_is_not_temp(candels: Sequence[Any]) -> bool:
        if isinstance(candels[-1], TemporaryCandle):
            return False
        return True

    @property
    def volume_candles_lst(self) -> Sequence[VolumeCandle | TemporaryCandle]:
        volume_candles_lst: list[VolumeCandle | TemporaryCandle] = []
        temp_candles_lst: list[VolumeCandle | TemporaryCandle] = []

        for candle in self.candles:
            if len(temp_candles_lst) > 0:
                temp_candles_lst += [
                    VolumeCandle(ts_open=candle.ts_open, ts_close=candle.ts_close, volume=candle.volume)
                ]
                combine_candles_lst = self.combine_candles(temp_candles_lst, self.volume)
                pop_last_if_exists(volume_candles_lst)
                volume_candles_lst += combine_candles_lst
                if self.check_last_candle_is_not_temp(volume_candles_lst):
                    continue
                candle = volume_candles_lst[-1]

            if candle.volume == self.volume:
                volume_candles_lst += [
                    VolumeCandle(ts_close=candle.ts_close, ts_open=candle.ts_open, volume=candle.volume)
                ]

            if candle.volume > self.volume:
                split_candles_lst = self.split_candle(candle, self.volume)
                volume_candles_lst += split_candles_lst
                if self.check_last_candle_is_not_temp(volume_candles_lst):
                    continue
                temp_candles_lst += [volume_candles_lst[-1]]

            if candle.volume < self.volume:
                temp_candles_lst = [
                    VolumeCandle(ts_open=candle.ts_open, ts_close=candle.ts_close, volume=candle.volume)
                ]

        return volume_candles_lst


def agg_volume_candles(candles: Sequence[Candle], volume: float) -> Sequence[VolumeCandle | TemporaryCandle]:
    return CandleAggregator(candles, volume).volume_candles_lst


test_candles_1 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 100),
]
result = agg_volume_candles(test_candles_1, 100)
assert len(result) == 1
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)

test_candles_2 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 150),
]
result = agg_volume_candles(test_candles_2, 100)
assert len(result) == 2
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)

test_candles_3 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 300),
]
result = agg_volume_candles(test_candles_3, 100)
assert len(result) == 3
assert result[-1].volume == 100
assert not isinstance(result[-1], TemporaryCandle)
print_result(result)


test_candles_4 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 333),
]
result = agg_volume_candles(test_candles_4, 100)
assert len(result) == 4
assert result[-1].volume == 33
assert isinstance(result[-1], TemporaryCandle)
print_result(result)


test_candles_5 = [
    Candle(1000, 1100, 1500, 1450, 1400, 1500, 200),
    Candle(1100, 1200, 1450, 1350, 1250, 1460, 650),
]
result = agg_volume_candles(test_candles_5, 100)
assert len(result) == 9
assert result[-1].volume == 50
assert isinstance(result[-1], TemporaryCandle)
print_result(result)

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
