from setuptools import setup, find_packages

setup(
    name='tree_lab',
    version='0.1.0',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        # List your dependencies here
        'numpy',
        'pandas',
        'polars',
        # Add other dependencies as needed
    ],
)
