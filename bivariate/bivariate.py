import math
import string
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mapclassify import NaturalBreaks
from matplotlib.colors import to_rgba_array


class BivariateColorMap:
    def __init__(self, colors: list[str]):
        if not self._is_square(len(colors)):
            raise ValueError("The number of colors must be a square.")
        self.colors = colors
        self.n_rows = math.isqrt(len(colors))
        self.label_letters, self.label_numbers, self.labels = self._make_labels()

    @staticmethod
    def _is_square(n: int) -> bool:
        return n == math.isqrt(n) ** 2

    def _make_labels(self) -> tuple[list[str], list[str], list[str]]:
        """Makes a list of labels for the bivariate color map of length n_rows**2.
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
        """Sorted labels by number

        Used to match the order of the colors produced by
        https://observablehq.com/@benjaminadk/bivariate-choropleth-color-generator"
        like: `["A3", "B3", "C3", "A2", "B2" ...]`
        """
        return sorted(self.labels, key=lambda x: x[1], reverse=reverse)

    def plot_color_square(self, show_labels=True) -> plt.Axes:
        """Plots the square of colors with the corresponding labels.

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

    def cmap(self) -> dict[str:str]:
        """Returns a map of labels to colors."""
        return dict(zip(self._sorted_labels(reverse=False), self.colors))

    def classify(self, var1: pd.Series, var2: pd.Series) -> pd.Series:
        """Classifies the data using the bivariate color map."""
        cls_var1 = pd.Series(NaturalBreaks(var1, self.n_rows).yb).map({k: v for k, v in enumerate(self.label_letters)})
        cls_var2 = pd.Series(NaturalBreaks(var2, self.n_rows).yb).map({k: v for k, v in enumerate(self.label_numbers)})
        return cls_var1 + cls_var2
