from setuptools import setup

setup(
    name='imgx',
    description='A image processing framework built on top of numpy.',
    version='1.2.0',
    license='GPLv3',
    author='Eduardo Fillipe da Silva Reis',
    author_email='eduardo556@live.com',
    url='https://github.com/eduardo-fillipe/imgx-framework',
    packages=['imgx'],
    python_requires='>=3.9',
    install_requires=['numpy', 'matplotlib', 'seaborn']
)
