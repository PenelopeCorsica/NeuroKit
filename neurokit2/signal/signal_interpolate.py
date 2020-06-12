# -*- coding: utf-8 -*-
import numpy as np
import scipy.interpolate


def signal_interpolate(x_values, y_values, x_new=None, method="quadratic"):
    """Interpolate a signal.

    Interpolate a signal using different methods.

    Parameters
    ----------
    x_values : list, array or Series
        The samples corresponding to the values to be interpolated.
    y_values : list, array or Series
        The values to be interpolated.
    x_new : list, array Series or int
        The samples at which to interpolate the y_values. Samples before the first value in x_values
        or after the last value in x_values will be extrapolated.
        If an integer is passed, nex_x will be considered as the desired length of the interpolated
        signal between the first and the last values of x_values. No extrapolation will be done for values
        before or after the first and the last valus of x_values.
    method : str
        Method of interpolation. Can be 'linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
        'previous', 'next' or 'monotone_cubic'.  'zero', 'slinear', 'quadratic' and 'cubic' refer to
        a spline interpolation of zeroth, first, second or third order; 'previous' and 'next' simply
        return the previous or next value of the point) or as an integer specifying the order of the
        spline interpolator to use.
        See https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html
        for details on the 'monotone_cubic' method.

    Returns
    -------
    array
        Vector of interpolated samples.

    Examples
    --------
    >>> import numpy as np
    >>> import neurokit2 as nk
    >>> import matplotlib.pyplot as plt
    >>>
    >>> # Generate points
    >>> signal = nk.signal_simulate(duration=1, sampling_rate=10)
    >>>
    >>> # List all interpolation methods and interpolation parameters
    >>> interpolation_methods = ["zero", "linear", "quadratic", "cubic", 5, "nearest", "monotone_cubic"]
    >>> x_values = np.linspace(0, 1, num=10)
    >>> x_new = np.linspace(0, 1, num=1000)
    >>>
    >>> # Visualize all interpolations
    >>> fig, ax = plt.subplots() #doctest: +SKIP
    >>> ax.scatter(x_values, signal, label="original datapoints", zorder=3) #doctest: +SKIP
    >>> for im in interpolation_methods:
    ...     signal_interpolated = nk.signal_interpolate(x_values, signal, x_new=x_new, method=im)
    ...     ax.plot(x_new, signal_interpolated, label=im) #doctest: +SKIP
    >>> ax.legend(loc="upper left") #doctest: +SKIP

    """
    # Sanity checks
    if len(x_values) != len(y_values):
        raise ValueError("NeuroKit error: signal_interpolate(): x_values and y_values must be of the same length.")

    if isinstance(x_new, int):
        if len(x_values) == x_new:
            return y_values
    else:
        if len(x_values) == len(x_new):
            return y_values

    # Create interpolation function
    if isinstance(method, str) and method.lower() == "monotone_cubic":
        interpolation_function = scipy.interpolate.PchipInterpolator(x_values, y_values, extrapolate=True)
    else:
        interpolation_function = scipy.interpolate.interp1d(
            x_values, y_values, kind=method, bounds_error=False, fill_value=([y_values[0]], [y_values[-1]])
        )

    if isinstance(x_new, int):
        x_new = np.linspace(x_values[0], x_values[-1], x_new)

    interpolated = interpolation_function(x_new)

    return interpolated
