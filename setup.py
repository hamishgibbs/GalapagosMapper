import setuptools

setuptools.setup(
    name='GalapagosMapper',
    version ='0.0.1',
    author='Hamish Gibbs',
    description='Package for matplotlib compatible plotting in the Galapagos Islands',
    url='https://github.com/hamishgibbs/Galapagos_Mapper',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'numpy',
        'geopandas',
        'shapely'
    ],
    zip_safe=False
    )
