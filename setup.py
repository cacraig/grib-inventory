from setuptools import setup, find_packages

setup(name='GribInventory',
      version='0.0.2',
      description='Python Grib Subsetting Tool.',
      author='Colin Craig',
      author_email='wxflights@gmail.com',
      url='',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'bs4'
      ],
      # extras_require={
      #     'test': ['pytest'],
      # },
      scripts=['bin/gribinventory'],
      packages=['gribinventory', 'gribinventory.models'],
     )