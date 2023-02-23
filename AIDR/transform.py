import numpy as np


def base_transform(pos, basis):
    """ Do base transformation on points set

        Parameters: pos((n,dimension) float) - coordinates of points set
                    basis((3,3) or (2,2) float) - new basis
        Returns:
    """
    return np.dot(pos, basis)

