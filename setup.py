import dblite

setup_args = {
    'name': 'scrapy-dblite',
    'version': dblite.__version__,
    'url': 'https://github.com/ownport/scrapy-dblite',
    'description': 'Simple library for storing Scrapy Items in sqlite database',
    'long_description': open('README.md').read(),
    'author': dblite.__author__,
    'maintainer': dblite.__author__,
    'maintainer_email': dblite.__author__,
    'license': 'BSD',
    'packages': 'dblite',
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Database',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**setup_args)
