import os

from setuptools import setup
from setuptools_scm import get_version

url = "https://github.com/livMatS/dtool-lookup-api"
readme = open('README.rst').read()
version = get_version(root='.', relative_to=__file__)


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="dtool-lookup-api",
    packages=["dtool_lookup_api"],
    description="This package offers both synchronous and asynchronous implementations of a standardized Python API "
                "to communicate with dserver.",
    long_description=readme,
    include_package_data=True,
    author="Johannes Laurin Hoermann",
    author_email="johannes.hoermann@imtek.uni-freiburg.de",
    use_scm_version={
        "root": '.',
        "relative_to": __file__,
        "write_to": os.path.join("dtool_lookup_api", "version.py"),
        "local_scheme": local_scheme},
    url=url,
    setup_requires=['setuptools_scm'],
    install_requires=[
        "asgiref",
        "aiohttp",
        "dtoolcore>=3.9.0",
        "PyYAML",
    ],
    extras_require={
        'testing': ['pytest', 'pytest-cov', 'pytest-ordering'],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
