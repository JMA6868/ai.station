import pytest

from src.exploratory_dual_threshold import is_anomaly


@pytest.mark.parametrize(
    "rms,cf,expected",
    [
        (0.05, 3.0, False),
        (0.09, 3.0, True),
        (0.05, 4.5, True),
        (0.09, 4.5, True),
        (0.08, 4.0, False),
    ],
)
def test_dual_threshold_or_rule(rms, cf, expected):
    result = is_anomaly(
        rms=rms,
        crest_factor=cf,
        rms_threshold=0.08,
        cf_threshold=4.0,
    )

    assert result is expected


def test_dual_threshold_rejects_negative_threshold():
    with pytest.raises(ValueError):
        is_anomaly(
            rms=0.05,
            crest_factor=3.0,
            rms_threshold=-0.01,
            cf_threshold=4.0,
        )
