from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'DNA Compiler uses constrain programming to facilitate genetic design.'
LONG_DESCRIPTION = 'Gather your library, define your genetic design constrains and requirements and DNA Compiler will create the sequence for you.'

setup(
  name="dnacompiler", 
  version=VERSION,
  author="Isaac Guerreiro",
  author_email="<isaacguerreirocom@gmail.com>",
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  packages=find_packages(),
  install_requires=[], 
  keywords=['python'],
  classifiers= []
)
