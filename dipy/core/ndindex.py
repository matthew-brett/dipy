import numpy as np
from numpy.lib.stride_tricks import as_strided

def ndindex(shape):
    """
    An N-dimensional iterator object to index arrays.

    Given the shape of an array, an `ndindex` instance iterates over
    the N-dimensional index of the array. At each iteration a tuple
    of indices is returned; the last dimension is iterated over first.

    Parameters
    ----------
    shape : tuple of ints
      The dimensions of the array.

    Examples
    --------
    >>> from dipy.core.ndindex import ndindex
    >>> shape = (3, 2, 1)
    >>> for index in ndindex(shape):
    ...     print index
    (0, 0, 0)
    (0, 1, 0)
    (1, 0, 0)
    (1, 1, 0)
    (2, 0, 0)
    (2, 1, 0)
    """
    if len(shape) == 0:
        yield ()
        return
    try: # np.nditer present from numpy 1.6.0
        np.nditer
    except AttributeError:
        for ix in np.ndindex(*shape):
            yield ix
    else: # nditer version much faster
        x = as_strided(np.zeros(1), shape=shape, strides=np.zeros_like(shape))
        ndi = np.nditer(x, flags=['multi_index', 'zerosize_ok'], order='C')
        for e in ndi:
            yield ndi.multi_index
