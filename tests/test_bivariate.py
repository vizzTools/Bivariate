#!/usr/bin/env python

"""Tests for `bivariate` package."""

import pytest
from bivariate import bivariate

COLORS_9 = ["#e8e8e8", "#a6d9d9", "#5ac8c8", "#d3a7cb", "#a6a7cb", "#5aa7c8", "#be64ac", "#a664ac", "#5a64ac"]


class TestBivariateColorMap:
    def test_only_takes_square_number_of_colors(self):
        bad_length_colors = COLORS_9 + ["#ffffff"]  # 10 colors is not a square number
        with pytest.raises(ValueError) as exc:
            bivariate.BivariateColorMap(bad_length_colors)
        assert "The number of colors must be a square." in str(exc.value)

    def test_make_labels(self):
        bivar = bivariate.BivariateColorMap(COLORS_9)

        assert bivar.n_rows == 3
        assert bivar.label_letters == ["A", "B", "C"]
        assert bivar.label_numbers == ["1", "2", "3"]
        assert bivar.labels == "A1 A2 A3 B1 B2 B3 C1 C2 C3".split()

    def test_labels_sorted(self):
        bivar = bivariate.BivariateColorMap(COLORS_9)
        assert bivar._sorted_labels() == "A3 B3 C3 A2 B2 C2 A1 B1 C1".split()

    def test_cmap(self):
        bivar = bivariate.BivariateColorMap(COLORS_9)
        expected_cmap = {
            "A1": "#e8e8e8",
            "B1": "#a6d9d9",
            "C1": "#5ac8c8",
            "A2": "#d3a7cb",
            "B2": "#a6a7cb",
            "C2": "#5aa7c8",
            "A3": "#be64ac",
            "B3": "#a664ac",
            "C3": "#5a64ac",
        }
        assert bivar.cmap() == expected_cmap
