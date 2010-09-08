import os
from os import path
from setuptools import setup, find_packages

f = open(path.join(path.dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

setup(
    name='bbnotify',
    version='0.1',
    url = "http://github.com/aleszoulek/bbnotify",
    description='Tray notification for BuildBot',
    long_description=long_description,
    author='Ales Zoulek',
    author_email='ales.zoulek@gmail.com',
    license='BSD',
    keywords='buildbot tray notification'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'bbnotify = bbnotify:main',
        ],
    },
    include_package_data=True,
    zip_safe = False,
)

