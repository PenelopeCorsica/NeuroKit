# -*- coding: utf-8 -*-
from .signal_period import signal_period


def signal_rate(peaks, sampling_rate=1000, desired_length=None, interpolation_method="monotone_cubic"):
    """Calculate signal rate from a series of peaks.

    This function can also be called either via ``ecg_rate()``, ```ppg_rate()`` or ``rsp_rate()``
    (aliases provided for consistency).

    Parameters
    ----------
    peaks : Union[list, np.array, pd.DataFrame, pd.Series, dict]
        The samples at which the peaks occur. If an array is passed in, it is assumed that it was obtained
        with `signal_findpeaks()`. If a DataFrame is passed in, it is assumed it is of the same length
        as the input signal in which occurrences of R-peaks are marked as "1", with such containers
        obtained with e.g., ecg_findpeaks() or rsp_findpeaks().
    sampling_rate : int
        The sampling frequency of the signal that contains peaks (in Hz, i.e., samples/second). Defaults to 1000.
    desired_length : int
        If None, the `desired_length` is set to length of peaks. The returned signal period will
        have the same number of elements as peaks (non-interpolated between peaks). If set to the
        length of signal, the returned signal period will be interpolated over `desired_length` samples
        (interpolated between peaks) and will have the same number of elements as signal. Default to None.
    interpolation_method : str
        Method used to interpolate the rate between peaks. See `signal_interpolate()`. 'monotone_cubic' is chosen
        as the default interpolation method since it ensures monotone interpolation between data points
        (i.e., it prevents physiologically implausible "overshoots" or "undershoots" in the y-direction).
        In contrast, the widely used cubic spline interpolation does not ensure monotonicity.

    Returns
    -------
    array
        A vector containing the rate.

    See Also
    --------
    signal_findpeaks, signal_fixpeaks, signal_plot

    Examples
    --------
    >>> import neurokit2 as nk
    >>>
    >>> signal = nk.signal_simulate(duration=10, sampling_rate=1000, frequency=1)
    >>> info = nk.signal_findpeaks(signal)
    >>>
    >>> rate = nk.signal_rate(peaks=info["Peaks"], desired_length=len(signal))
    >>> fig = nk.signal_plot(rate)
    >>> fig #doctest: +SKIP

    """
    period = signal_period(peaks, sampling_rate, desired_length, interpolation_method)
    rate = 60 / period

    return rate
