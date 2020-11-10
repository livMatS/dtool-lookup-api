import os

from setuptools import setup
from setuptools_scm import get_version

url = "https://github.com/IMTEK-Simulation/dtool-lookup-api"
readme = open('README.rst').read()
version = get_version(root='.', relative_to=__file__)


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="dtool-lookup-api",
    packages=["dtool_lookup_api"],
    description="""This package offers both synchronous and asynchronous
                   implementations of a standardized Python API to communicate
                   with the dtool lookup server.""",
    long_description=readme,
    include_package_data=True,
    author="Johannes Laurin Hoermann, Lars Pastewka",
    author_email="johannes.hoermann@imtek.uni-freiburg.de",
    use_scm_version={
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join("dtool_lookup_api", "version.py"),
        "local_scheme": local_scheme},
    url=url,
    setup_requires=['setuptools_scm'],
    tests_require=['pytest', 'pytest-cov'],
    install_requires=[
        "asgiref",
        "aiohttp",
        "dtoolcore>=3.9.0",
        "dtool_config>=0.1.1",
        "pygments",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
