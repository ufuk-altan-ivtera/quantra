from setuptools import setup, find_packages

setup(
    name='quantra',
    author='Ufuk Altan',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
        'yfinance==0.2.26',
        'pandas>=1.5.3,<2.1',
        'numpy>=1.24.3',
        'ta==0.10.2', 
        'statsmodels==0.13.5',
        'scikit-learn==1.2.2',
        'imbalanced-learn==0.11.0',
        'groq==0.5.0'
    ],
    setup_requires=['setuptools>=49.6.0'],
)
