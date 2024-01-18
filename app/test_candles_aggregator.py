import pytest
from candles_aggregator import Candle, TemporaryCandle, agg_volume_candles


@pytest.mark.parametrize(
    ("name_case, test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles"),
    [
        (
            "test_candles_0",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 100),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 150),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 100),
            ],
            100,
            4,
            50,
            True,
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 100),
                Candle(1100, 1166.67, 1450, 1350, 1250, 1460, 100),
                Candle(1166.67, 1255.56, 1450, 1400, 1250, 1460, 100),
                TemporaryCandle(1255.56, 1300, 1450, 1400, 1250, 1460, 50),
            ],
        ),
        (
            "test_candles_1",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 100)],
            100,
            1,
            100,
            False,
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 100)],
        ),
        (
            "test_candles_2",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 150)],
            100,
            2,
            50,
            True,
            [
                Candle(1000, 1066.67, 1500, 1450, 1400, 1500, 100),
                TemporaryCandle(1066.67, 1100.00, 1500, 1450, 1400, 1500, 50),
            ],
        ),
    ],
)
def test_agg_volume_candles(
    name_case, test_candles, volume, expected_len, expected_volume, expected_bool, excepted_candles
):
    result = agg_volume_candles(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool
    assert result == excepted_candles
