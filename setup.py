import setuptools

with (open('README.md', 'r') as fh:
      long_description = fh.read()

setuptools.setup(
    name='Galapagos_Mapper_hamishgibbs',
    version ='0.0.1',
    author='Hamish Gibbs',
    description='Package for plotting data in the Galapagos Islands'
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hamishgibbs/Galapagos_Mapper',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
