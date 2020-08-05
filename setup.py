from setuptools import setup, find_packages

setup(
    name='Grand Travels',
    description='An app to track our travels via our motorhomes GPS enabled router.',
    version='1.2',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask']
)