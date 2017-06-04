from setuptools import setup

setup(
    name='student_bsu_by',

    version='0.4.1',

    description='Tool for getting various student information from student.bsu.by website.',
    url='https://github.com/teryokhin/student_bsu_by',

    author='Maxim Teryokhin, Ilya Medyanikov',
    author_email='max.teryokhin@gmail.com',

    license='MIT',

    packages=['student_bsu_by'],

    install_requires=['requests'],
)
