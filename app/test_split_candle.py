import pytest
from candles_aggregator import Candle, CandleAggregator, TemporaryCandle

# class Candle:
#     ts_open: float
#     ts_close: float
#     open: float
#     close: float
#     low: float
#     high: float
#     volume: float


# @pytest.mark.skip()
@pytest.mark.parametrize(
    ("test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles"),
    [
        (
            Candle(1000, 1100, 1500, 1450, 1400, 1500, 150),
            100,
            2,
            50,
            True,
            [
                Candle(1000, 1066.67, 1500, 1450, 1400, 1500, 100),
                TemporaryCandle(1066.67, 1100.00, 1500, 1450, 1400, 1500, 50),
            ],
        ),
        (
            Candle(1000, 1150, 1500, 1450, 1400, 1500, 150),
            100,
            2,
            50,
            True,
            [
                Candle(1000, 1100.0, 1500, 1450, 1400, 1500, 100),
                TemporaryCandle(1100.0, 1150.0, 1500, 1450, 1400, 1500, 50),
            ],
        ),
        (
            Candle(1000, 1100, 1500, 1450, 1400, 1500, 300),
            100,
            3,
            100,
            False,
            [
                Candle(1000, 1033.33, 1500, 1450, 1400, 1500, 100),
                Candle(1033.33, 1066.66, 1500, 1450, 1400, 1500, 100),
                Candle(1066.66, 1099.99, 1500, 1450, 1400, 1500, 100),
            ],
        ),
    ],
)
def test_split_candle(test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles):
    result = CandleAggregator.split_candle(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool
    assert result == excepted_candles
