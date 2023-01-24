import os
from setuptools import (
    find_packages,
    setup
)


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'requirements.txt')) as requirements_file:
    REQUIRES = []
    LINKS = None

    for requirement in requirements_file.read().split('\n'):
        if requirement.startswith('--find-links'):
            (_, LINKS) = requirement.split(' ')
            continue
        REQUIRES.append(requirement)

setup(
    name='TodoList',
    version='0.1',
    description='A TodoList build with pyramid.',
    author='Benjamin Reiter',
    author_email='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    dependency_lins=[
        LINKS
    ],
    entry_points={
        'paste.app_factory': [
            'main = todolist:main',
        ],
        'console_scripts': [
            'initdb = todolist.scripts.initializedb:main',
        ]
    }
)
