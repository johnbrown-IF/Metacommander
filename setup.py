from setuptools import setup

setup(
    name='Metacommander',
    version='1.2',
    packages=['metacommander'],
    author='Alexey Galkin',
    license='MIT',
    description='A Python wrapper (preparser) for terminal-based Interactive Fiction interpreters and text adventures.',
    entry_points={
        'console_scripts': [
            'mc = metacommander.mc:main',
        ]
    }
)
