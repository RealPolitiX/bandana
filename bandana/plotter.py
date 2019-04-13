#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: R. Patrick Xian, Christopher Sutton
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go


def bandplot3d(bands, selector, indaxis=0, title='', fname='', **kwargs):
    """ Make 3D band structure (a number of electronic bands) surface plot.

    :Parameters:
        bands : 2D/3D matrix
            Electronic band structure ordered by band index.
        selector : iterable
            Index selector for the bands to visualize.
        indaxis : int | 0
            Axis of the band index.
        title : str | ''
            Title to appear on the plot.
        fname : str | ''
            User-defined filename for the plotted figure.
        **kwargs : keyword arguments
            Additional keyword arguments for `plotly.graph_objs.Layout()`.
            :width, height: numeric
                Width and height of the plotted figure.
            :plot_margin: dictionary
                Margins of the figure upon initialization, such as dict(l=65, r=50, b=65, t=90).
            :labelsize: int
                Size of the axes label.
            :aspect: list/tuple
                Aspect ratio of the x, y and z directions.
    """

    nb = bands.ndim

    if nb == 2: # Amend an axis in case only one band is used as the input
        bands = bands[None, :, :]

    elif nb == 3:

        bands = np.moveaxis(bands, indaxis, 0)
        # Retrieve figure attributes
        plotmargin = kwargs.pop('plot_margin', dict(l=65, r=50, b=65, t=90))
        width = kwargs.pop('width', 600)
        height = kwargs.pop('height', 600)
        labelsize = kwargs.pop('labelsize', 30)
        asp = kwargs.pop('aspect', [1, 1, 1])

        data = [go.Surface(z=bands[i,:,:], showscale=False) for i in selector]

        layout = go.Layout(
            scene=dict(xaxis=dict(ticks='', showticklabels=False, title='kx',
                                    linewidth=3, titlefont=dict(size=labelsize)),
                       aspectratio=dict(x=asp[0], y=asp[1], z=asp[2]),
            yaxis=dict(ticks='', showticklabels=False, title='ky', linewidth=3,
                        titlefont=dict(size=labelsize)),
            zaxis=dict(ticks='', showticklabels=False, title='Energy', linewidth=3,
                        titlefont=dict(size=labelsize))),
            title=title,
            autosize=False,
            width=width, height=height,
            margin=plotmargin, **kwargs)

        f = go.Figure(data=data, layout=layout)
        plot = py.iplot(f, filename=fname)

        return plot
