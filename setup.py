import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='django-oscar-tinkoff',
    version='0.0001',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='Django oscar tinkoff payment support',
    long_description=README,
    url='https://github.com/initflow/django-oscar-tinkoff',
    author='Pavel Pantiukhov',
    author_email='pantyukhov.p@gmail.com',
    install_requires=install_requires
)

