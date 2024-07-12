from setuptools import setup, find_packages

setup(
    name='visual_eda',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for visual exploratory data analysis',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas>=1.0.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.10.0',
        'tabulate>=0.8.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)