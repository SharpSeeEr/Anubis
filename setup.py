"""Packaging settings."""

from os.path import abspath, dirname, join
from subprocess import run, CalledProcessError

from anubis import __version__
from setuptools import Command, find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        try:
            result = run(['pytest', '--cov=anubis', '--cov-report=term-missing'], check=True)
            raise SystemExit(result.returncode)
        except CalledProcessError as e:
            raise SystemExit(e.returncode)


with open(join(this_dir, 'requirements.txt'), encoding='utf-8') as file:
    reqs = [line.strip() for line in file if line.strip() and not line.startswith('#')]

setup(
    name='anubis-netsec-refactored',
    version=__version__,
    description='Modern and efficient subdomain enumeration and information gathering tool, overhall 2024 by rikdan cybersecurity research',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RikDan-CyberSecurity-Research/Anubis',
    author='JonLuca DeCaro',
    author_email='jonluca.decaro@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    python_requires='>=3.6',
    install_requires=reqs,
    extras_require={'test': ['coverage', 'pytest', 'pytest-cov']},
    entry_points={'console_scripts': ['anubis=anubis.cli:main']},
    cmdclass={'test': RunTests},
)
