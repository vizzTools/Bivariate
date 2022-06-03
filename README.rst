=========
bivariate
=========


.. image:: https://img.shields.io/pypi/v/bivariate.svg
        :target: https://pypi.python.org/pypi/bivariate

.. image:: https://img.shields.io/travis/bielstela/bivariate.svg
        :target: https://travis-ci.com/bielstela/bivariate

.. image:: https://readthedocs.org/projects/bivariate/badge/?version=latest
        :target: https://bivariate.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

Straighforward tool to help you in your bivariate maps journey


* Free software: MIT license
* Documentation: https://bivariate.readthedocs.io. (Not yet)

Usage
-----

Simply select your prefered color palette from `bivariate palette generator`_, copy the color list and::
        from bivariate import BivariateColorMap

        palette = ["#e8e8e8", "#d9a4a4", "#c85a5a", "#a7cad3", "#a7a4a4", "#a75a5a", "#64acbe", "#64a4a4", "#645a5a"]
        bivar = BivariateColorMap(palette)
        bivar.plot_color_square()

Then, if you are using a DataFrame or GeoDataFrame, to compute the the classes simply do::
        classes = bivar.classify(data.var1, data.var2)

And, with geopandas, plot the resulting bivariate map with::
        data.plot(color=classes.map(bivar.cmap()), categorical=True, figsize=(14, 14))
        bivar.plot_color_square(show_labels=False)
        plt.plot()

TODO
----

* Add classifier for raster data