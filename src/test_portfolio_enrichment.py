import pytest
import combine_sources


def test_name_normalization():
    variant_one = 'Tesla'
    variant_two = 'TESLA!'
    assert combine_sources.normalize_name(variant_one) == combine_sources.normalize_name(variant_two)
# Todo add tests
