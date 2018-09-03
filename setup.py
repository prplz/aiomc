from setuptools import setup

setup(
    name='aiomc',
    version='0.0.1',
    packages=['aiomc'],
    url='https://github.com/prplz/aiomc',
    license='MIT',
    author='prplz',
    author_email='mhiming@gmail.com',
    description='Ping Minecraft servers',
    install_requires=[
        'dnspython>=1.15.0'
    ],
    entry_points={
        'console_scripts': [
            'aiomc=aiomc.command:aiomc'
        ]
    }
)
