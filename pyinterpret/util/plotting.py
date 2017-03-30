from matplotlib import colors, cm, patches, pyplot
import numpy as np
import math

COLORS = ['#328BD5', '#404B5A', '#3EB642', '#E04341', '#8665D0']


class ColorMap(object):
    """
    Maps arrays to colors
    """
    class LinearSegments(object):
        black_to_blue_dict = {
            'red': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),
            'blue': ((0.0, 0.0, 0.0),
                     (1.0, 1.0, 0.0)),
            'green': ((0.0, 0.0, 0.0),
                      (1.0, 0.0, 0.0))}

        black_to_green_dict = {
            'red': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),
            'blue': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),
            'green': ((0.0, 0.0, 0.0),
                      (1.0, 1.0, 0.0))}

        red_to_green_dict = {
                'red': ((0.0, 1.0, 1.0),
                         (1.0, 0.0, 0.0)),
                 'blue': ((0.0, 0.0, 0.0),
                          (1.0, 0.0, 0.0)),
                 'green': ((0.0, 0.0, 0.0),
                           (1.0, 1.0, 0.0))}

    red_to_green = colors.LinearSegmentedColormap('my_colormap', LinearSegments.red_to_green_dict, 100)
    black_to_blue = colors.LinearSegmentedColormap('my_colormap', LinearSegments.black_to_blue_dict, 100)
    black_to_green = colors.LinearSegmentedColormap('my_colormap', LinearSegments.black_to_green_dict, 100)


    def array_1d_to_color_scale(self,array_1d, colormap):
        mmin, mmax = min(array_1d), max(array_1d)
        norm = colors.Normalize(mmin, mmax)
        scalarMapx = cm.ScalarMappable(norm=norm, cmap=colormap)
        scalarMapx.set_array(array_1d)
        return scalarMapx.to_rgba(array_1d)



def coordinate_gradients_to_1d_colorscale(dx, dy, x_buffer=.5, y_buffer=.5, norm='separate'):
    """
    Map x and y gradients to single array of colors based on 2D color scale

    Parameters
    ----------
    dx: array type
        x component of gradient
    dy: array type
        y component of gradient
    x_buffer:
    y_buffer:
    norm: string
        whether to normalize colors based on differences in x and y scales.
        if separate, each component gets its own scaling (default)
        if global, will scale based on global extrema

    Returns
    ----------
    color_array, xmin, xmax, ymin, ymax
    """
    xmin, xmax = dx.min(), dx.max()
    ymin, ymax = dy.min(), dy.max()
    global_min = min(xmin, ymin)
    global_max = max(xmax, ymax)
    if norm == 'separate':
        normx = colors.Normalize(xmin-x_buffer, xmax+x_buffer)
        normy = colors.Normalize(ymin-y_buffer, ymax+y_buffer)
    elif norm == 'shared':
        normx = colors.Normalize(global_min-x_buffer, global_max+x_buffer)
        normy = colors.Normalize(global_min-x_buffer, global_max+x_buffer)
    else:
        raise KeyError("keyword norm must be in ('separate', 'shared')")

    scalarMapx = cm.ScalarMappable(norm=normx, cmap=ColorMap.black_to_blue)
    scalarMapy = cm.ScalarMappable(norm=normy, cmap=ColorMap.black_to_green)

    scalarMapx.set_array(dx)
    scalarMapy.set_array(dy)

    colorx = scalarMapx.to_rgba(dx)
    colory = scalarMapy.to_rgba(dy)

    color = np.array(colorx) + np.array(colory)
    color[:, :, 3] = 1.
    return color, xmin-x_buffer, xmax+x_buffer, ymin-y_buffer, ymax+y_buffer

def plot_2d_color_scale(x1_min, x1_max, x2_min, x2_max, resolution=10, ax=None):
    """
    Return a generic plot of a 2D color scale

    Parameters
    ----------
    x1_min: numeric
        how high x1 should extend the color scale
    x1_max:  numeric
        how high 2 should extend the color scale
    x2_min:  numeric
        how low x2 should extend the color scale
    x2_max: numeric
        how high x2 should extend the color scale
    resolution: int
        how fine grain to make the color scale
    ax: matplotlib.axes._subplots.AxesSubplot
        matplotlib axis to plot on. if none will generate a new one

    Returns
    ----------
    matplotlib.axes._subplots.AxesSubplot
    """
    ax.set_xlim(x1_min, x1_max)
    ax.set_ylim(x2_min, x2_max)
    x1 = np.linspace(x1_min, x1_max, resolution+1)
    x2 = np.linspace(x2_min, x2_max, resolution+1)
    x1_diff = x1[1] - x1[0]
    x2_diff = x2[1] - x2[0]
    x1, x2 = np.meshgrid(x1, x2)
    colors_for_scale, a, b, c, d = coordinate_gradients_to_1d_colorscale(x1, x2)

    if ax is None:
        f, ax = pyplot.subplots(1)
    for i in range(resolution):
        for j in range(resolution):
            xy = (x1[i,j], x2[i,j])
            color = colors_for_scale[i, j]
            rect = patches.Rectangle(
                xy, x1_diff, x2_diff,
                alpha=None, facecolor=color,
            )
            ax.add_patch(rect)
    return ax

def plot_2d_color_scale_dev(x1_min, x1_max, x2_min, x2_max, resolution=10, ax=None):
    """
    Return a generic plot of a 2D color scale

    Parameters
    ----------
    x1_min: numeric
        how high x1 should extend the color scale
    x1_max:  numeric
        how high 2 should extend the color scale
    x2_min:  numeric
        how low x2 should extend the color scale
    x2_max: numeric
        how high x2 should extend the color scale
    resolution: int
        how fine grain to make the color scale
    ax: matplotlib.axes._subplots.AxesSubplot
        matplotlib axis to plot on. if none will generate a new one

    Returns
    ----------
    matplotlib.axes._subplots.AxesSubplot
    """
    ax.set_xlim(x1_min, x1_max)
    ax.set_ylim(x2_min, x2_max)
    x1 = np.linspace(x1_min, x1_max, resolution+1)
    x2 = np.linspace(x2_min, x2_max, resolution+1)
    x1_diff = x1[1] - x1[0]
    x2_diff = x2[1] - x2[0]
    x1, x2 = np.meshgrid(x1, x2)
    colors_for_scale, a, b, c, d = coordinate_gradients_to_1d_colorscale(x1, x2)

    x1_labels = num_to_string()
    if ax is None:
        f, ax = pyplot.subplots(1)
    for i in range(resolution):
        for j in range(resolution):
            xy = (x1[i,j], x2[i,j])
            color = colors_for_scale[i, j]
            rect = patches.Rectangle(
                xy, x1_diff, x2_diff,
                alpha=None, facecolor=color,
            )
            ax.add_patch(rect)
    return ax




def order_of_magnitude(n):
    if n == 0:
        return 0
    else:
        return math.floor(math.log10(n))
def num_to_string(number, n_digits=0):
    formatter = numeric_string_formatter(n_digits)
    return formatter % number
def numeric_string_formatter(n_digits):
    return "%0.{}f".format(n_digits)
def magic_formatter(array):
    min_diff = abs(np.diff(array)).min()
    or_magnitude = order_of_magnitude(min_diff)
    if or_magnitude == 0:
        significant_figures = 0
    elif or_magnitude > 0:
        significant_figures = 1
    else:
        significant_figures = int(-1 * or_magnitude + 1)
    return map(lambda i: num_to_string(i, significant_figures), array)
