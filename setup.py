from setuptools import setup

setup(name='cartographer',
      version='0.1',
      description='Cartographer command line client',
      url='https://cartographer.io',
      author='Dave Gurnell',
      author_email='dave@cartographer.io',
      license='Apache 2',
      packages=['cartographer'],
      install_requires=[
          'click',
          'click_config_file',
          'requests',
          'semver'
      ],
      scripts=[
          'bin/cartographer'
      ],
      zip_safe=False)
