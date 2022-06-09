import math
import string
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mapclassify import NaturalBreaks
from matplotlib.colors import to_rgba_array


class BivariateColorMap:
    """Create a bivariate color map from a list of colors.

    Attributes
    ----------
    colors: list
        list of colors to use for the bivariate color map
    n_rows: int
        number of rows in the bivariate color map or the size of the square of colors
    label_letters: list
        letter codes for first variable. The length of this list is n_rows.
    label_numbers: list
        numeric codes for second variable. The length of this list is n_rows.
    labels: list
        labels used in the classification of the data. The length of this list is n_rows**2.
    """

    def __init__(self, colors: list[str]):
        """Initialize the bivariate color map.

        To create a list of valid colors, use the following tool to make your own list of colors:
        https://observablehq.com/@benjaminadk/bivariate-choropleth-color-generator

        Parameters
        ----------
        colors: list
            List of colors to use for the bivariate color map
        """
        if not self._is_square(len(colors)):
            raise ValueError("The length of colors must be a square number like 9 (3*3), 16 (4*4)...")
        self.colors = colors
        self.n_rows = math.isqrt(len(colors))
        self.label_letters, self.label_numbers, self.labels = self._make_labels()

    @property
    def cmap(self) -> dict[str:str]:
        """Map of labels to colors."""
        return dict(zip(self._sorted_labels(reverse=False), self.colors))

    @staticmethod
    def _is_square(n: int) -> bool:
        """Check if n is a square number."""
        return n == math.isqrt(n) ** 2

    def _make_labels(self) -> tuple[list[str], list[str], list[str]]:
        """Make a list of labels for the bivariate color map of length n_rows**2.

        The labels are a combination of the letters A-Z and the numbers 1-9.

        Returns
        -------
        letters: list
            Letter codes for first variable
        numbers: list
            Numeric codes for second variable
        labels: list
            result of cartesian product between letters and numbers
        """
        letters = list(string.ascii_uppercase[: self.n_rows])
        numbers = [str(n) for n in range(1, self.n_rows + 1)]
        return (
            letters,
            numbers,
            ["".join([*pair]) for pair in product(letters, numbers)],
        )

    def _sorted_labels(self, reverse: bool = True) -> list[str]:
        """Sort labels by number.

        Used to match the order of the colors produced by
        https://observablehq.com/@benjaminadk/bivariate-choropleth-color-generator"

        Parameters
        ----------
        reverse: bool
            Reverse the order of the labels by number like: `["A3", "B3", "C3", "A2", "B2" ...]`
        """
        return sorted(self.labels, key=lambda x: x[1], reverse=reverse)

    def plot_color_square(self, show_labels=True) -> plt.Axes:
        """Plot the square of colors with the corresponding labels.

        Parameters
        ----------
        show_labels: bool
            Show category labels on each color
        """
        labels = np.array(self._sorted_labels()).reshape(self.n_rows, self.n_rows)
        # color array must be rotated so the lighter color is at the lower left corner
        rgba_colors = np.rot90(to_rgba_array(self.colors).reshape(self.n_rows, self.n_rows, 4))

        _, ax = plt.subplots()
        ax.imshow(rgba_colors)
        if show_labels:
            for ij, label in np.ndenumerate(labels):
                ax.text(ij[1], ij[0], label, ha="center", va="center", color="w")
        return ax

    def classify(self, var1: pd.Series, var2: pd.Series) -> pd.Series:
        """Classifies the data using the bivariate color map.

        Parameters
        ----------
        var1: pd.Series
            First variable to classify
        var2: pd.Series
            Second variable to classify

        Returns
        -------
        pd.Series
            Series of labels for the bivariate color map
        """
        cls_var1 = pd.Series(NaturalBreaks(var1, self.n_rows).yb).map({k: v for k, v in enumerate(self.label_letters)})
        cls_var2 = pd.Series(NaturalBreaks(var2, self.n_rows).yb).map({k: v for k, v in enumerate(self.label_numbers)})
        return cls_var1 + cls_var2
