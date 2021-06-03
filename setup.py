from setuptools import setup, find_packages
from dash_dict_callback.__version__ import __version__

setup(
    name="dash_dict_callback",
    version=__version__,
    description="Dictionary Based Callback Plugin and Decorator for Dash",
    url="https://github.com/WestHealth/dash-dict-callback",
    author='Haw-minn Lu',
    author_email="hlu@westhealth.org",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dash>=1.20.0",
    ]
)
