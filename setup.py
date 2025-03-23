from setuptools import setup, find_packages

setup(
    name='quantra',
    author='Ufuk Altan',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas>=1.5.3,<2.1',
        'numpy>=1.23.5,<1.24.0',
        'pyarrow==19.0.1',
        'ta==0.10.2', 
        'statsmodels',
        'scikit-learn',
        'imbalanced-learn',
        'groq',
        'aiohttp'
    ],
    setup_requires=['setuptools>=49.6.0'],
)
