
import os
import nose
from nose.tools import nottest
import common


@nottest
def test():
    """
    Run all the doctests available
    """
    path = os.path.split(__file__)[0]
    print "Path: {0}".format(path)
    nose.main(argv=['-w', path, '--with-doctest'])


def get_version():
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version

__version__ = get_version()

__all__ = ['__version__',
           'test'
           ]