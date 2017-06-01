from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='student_bsu_by',

    version='0.0.1',

    description='Module for getting infromation from student.bsu.by',
    long_description=long_description,
    url='https://github.com/teryokhin/student_bsu_by',

    author='Maxim Teryokhin',
    author_email='max.teryokhin@gmail.com',

    license='MIT',

    packages=['student_bsu_by'],

    install_requires=['requests', 'pillow'],
)