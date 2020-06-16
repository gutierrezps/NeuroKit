from timeit import default_timer as timer

from wfdb.processing import compare_annotations


def benchmark_record(record, sampling_rate, annotation, tolerance, detector):
    """Obtain detector performance for an annotated record.

    Parameters
    ----------
    record : array
        The raw physiological record.
    sampling_rate: int
        The sampling rate of the record in Hertz.
    annotation : array
        The manual extrema annotations.
    tolerance : int
        Maximum difference in millisecond that is permitted between the manual
        annotation and the annotation generated by the detector.
    detector : function
        A function that takes a physiological record as first positional
        argument as well as a `sampling_rate` keyword argument.

    Returns
    -------
    precision : float
        The detectors precision on the record given the tolerance.
    sensitivity : float
        The detectors sensitivity on the record given the tolerance.

    """
    detector_annotation = detector(record, sampling_rate=sampling_rate)

    comparitor = compare_annotations(detector_annotation, annotation, tolerance)
    tp = comparitor.tp
    fp = comparitor.fp
    fn = comparitor.fn

    sensitivity = tp / (tp + fn)
    precision = tp / (tp + fp)

    return precision, sensitivity


def time_record(record, sampling_rate, detector, n_runs):
    """Obtain the average run time of a detector on a record over N runs.

    Parameters
    ----------
    record : array
        The raw physiological record.
    sampling_rate : int
        The sampling rate of the record in Hertz-
    detector : function
        A function that takes a physiological record as first positional
        argument as well as a `sampling_rate` keyword argument.
    n_runs : int
        The number of runs.

    Returns
    -------
    avg_time
        The run time of the detector on the record averaged over n_runs. In
        milliseconds.

    """
    start = timer()
    for _ in range(n_runs):
        detector(record, sampling_rate=sampling_rate)
    end = timer()
    avg_time = (end - start) / n_runs * 1000

    return avg_time
