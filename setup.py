import os
from setuptools import setup, find_packages

setup(
    name='bbnotify',
    version='0.1',
    description='Tray notification for BuildBot',
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
    packages=find_packages(exclude=['tests']),
    scripts = ['bbnotify.py'],
    include_package_data=True,
)

