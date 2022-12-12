from setuptools import setup, find_namespace_packages
setup(name='contact_book',
      version='1',
      description='Very useful code',
      url='http://github.com/dummy_user/useful',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['start_1 = contact_book.sorter:work']})
