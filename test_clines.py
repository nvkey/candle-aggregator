import pytest

from cline_converter import (
    Candle,
    CandleAggregator,
    TemporaryCandle,
    agg_volume_candles,
)


# @pytest.mark.skip()
@pytest.mark.parametrize(
    ("test_candles, volume, expected_len, expected_volume, expected_bool"),
    [
        (
            Candle(1000, 1100, 1500, 1450, 1400, 1500, 150),
            100,
            2,
            50,
            True,
        ),
        (
            Candle(1000, 1100, 1500, 1450, 1400, 1500, 155),
            50,
            4,
            5,
            True,
        ),
        (
            Candle(1000, 1100, 1500, 1450, 1400, 1500, 150),
            50,
            3,
            50,
            False,
        ),
    ],
)
def test_split_candle(test_candles, volume, expected_len, expected_volume, expected_bool):
    result = CandleAggregator.split_candle(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool


# @pytest.mark.skip()
@pytest.mark.parametrize(
    ("test_candles, volume, expected_len, expected_volume, expected_bool"),
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
        ),
        (
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 99),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 99),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 2),
            ],
            100,
            2,
            100,
            False,
        ),
        (
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
                Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
                Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
                Candle(1500, 1600, 1370, 1480, 1350, 1500, 10),
            ],
            100,
            1,
            70,
            True,
        ),
    ],
)
def test_combine_candles(test_candles, volume, expected_len, expected_volume, expected_bool):
    result = CandleAggregator.combine_candles(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool


# @pytest.mark.skip()
@pytest.mark.parametrize(
    ("name_case, test_candles, volume, expected_len, expected_volume, expected_bool"),
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
        ),
        (
            "test_candles_1",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 100)],
            100,
            1,
            100,
            False,
        ),
        (
            "test_candles_2",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 150)],
            100,
            2,
            50,
            True,
        ),
        (
            "test_candles_3",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 300)],
            100,
            3,
            100,
            False,
        ),
        (
            "test_candles_4",
            [Candle(1000, 1100, 1500, 1450, 1400, 1500, 333)],
            100,
            4,
            33,
            True,
        ),
        (
            "test_candles_5",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 200),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 650),
            ],
            100,
            9,
            50,
            True,
        ),
        (
            "test_candles_6",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 200),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 650),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 100),
                Candle(1300, 1400, 1400, 1350, 1340, 1410, 100),
                Candle(1400, 1500, 1350, 1370, 1345, 1350, 100),
                Candle(1500, 1600, 1370, 1480, 1350, 1500, 300),
            ],
            100,
            15,
            50,
            True,
        ),
        (
            "test_candles_7",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
                Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
                Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
                Candle(1500, 1600, 1370, 1480, 1350, 1500, 10),
            ],
            100,
            1,
            70,
            True,
        ),
        (
            "test_candles_8",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
                Candle(1100, 1200, 1450, 1350, 1250, 1460, 20),
                Candle(1200, 1300, 1350, 1400, 1330, 1410, 10),
                Candle(1300, 1400, 1400, 1350, 1340, 1410, 15),
                Candle(1400, 1500, 1350, 1370, 1345, 1350, 5),
                Candle(1500, 1600, 1370, 1480, 1350, 1500, 40),
            ],
            100,
            1,
            100,
            False,
        ),
        (
            "test_candles_9",
            [
                Candle(1000, 1100, 1500, 1450, 1400, 1500, 10),
                Candle(1100, 1200, 1450, 1500, 1400, 1500, 10),
                Candle(1200, 1300, 1500, 1450, 1000, 2000, 10),
                Candle(1300, 1400, 1450, 1500, 1400, 1500, 10),
                Candle(1400, 1500, 1500, 1450, 1400, 1500, 10),
            ],
            19,
            3,
            12,
            True,
        ),
    ],
)
def test_agg_volume_candles(name_case, test_candles, volume, expected_len, expected_volume, expected_bool):
    result = agg_volume_candles(test_candles, volume)
    assert len(result) == expected_len
    assert result[-1].volume == expected_volume
    assert isinstance(result[-1], TemporaryCandle) == expected_bool
