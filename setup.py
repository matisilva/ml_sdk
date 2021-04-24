from setuptools import setup
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()

setup(
    name='ml_sdk',
    version='1.2.0',
    description='An SDK to deploy your ML models in a common API made with FastAPI',
    long_description=long_description,
    url='https://pypi.python.org/pypi/mlsdk',
    author='Matias',
    author_email='matias.gaston.silva@mi.unc.edu.ar',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: General public',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='machine learning models api framework',
    packages=[
        'ml_sdk',
        'ml_sdk.io',
        'ml_sdk.service',
        'ml_sdk.communication',
        'ml_sdk.database',
        'ml_sdk.api',
    ],
    package_dir = {'ml_sdk':'.'},
    install_requires=requirements
)
