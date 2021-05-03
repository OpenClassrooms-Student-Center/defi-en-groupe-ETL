from .mufflins import mufflins
from .chi_gra import chichigneux_grapencourt

def extract():
    data = mufflins()

    return data

__all__ = ["extract"]
