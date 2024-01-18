import pytest
from candles_aggregator import Candle, CandleAggregator, TemporaryCandle


@pytest.mark.parametrize(
    ("test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles"),
    [
        (
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 99),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 1),
            ],
            100,
            1,
            100,
            False,
            [
                Candle(1000, 1200, 1500, 1350, 1250, 1500, 100),
            ],
        ),
        (
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 99),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 2),
            ],
            100,
            2,
            1,
            True,
            [
                Candle(1000, 1198.02, 1500, 1350, 1250, 1500, 100),
                TemporaryCandle(1198.02, 1200.0, 1500, 1350, 1250, 1500, 1),
            ],
        ),
        (
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
                Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
                Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
                Candle(1500, 1600, 1370, 1481, 1350, 1500, 10),
            ],
            100,
            1,
            70,
            True,
            [
                TemporaryCandle(1000, 1600, 1500, 1481, 1250, 1500, 70),
            ],
        ),
    ],
)
def test_combine_candles(test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles):
    result = CandleAggregator.combine_candles(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool
    assert result == excepted_candles
