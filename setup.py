from setuptools import setup

setup(
    name='imgx',
    python_requires='>=3.9',
    license='GPLv3',
    version='1.0.0',
    description='A image processing framework built on top of numpy.',
    author='Eduardo Fillipe da Silva Reis',
    author_email='eduardo556@live.com',
    packages=['imgx'],
    install_requires=['numpy', 'matplotlib', 'seaborn']
)
