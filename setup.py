from setuptools import setup, find_packages

setup(
    name='moveonmeter',
    version='0.0.0',
    packages=find_packages(),
    url='https://github.com/foolswood/boredom_voter',
    include_package_data=True,
    license='GPLv3',
    author='David Honour',
    author_email='david@foolswood.co.uk',
    description='Cheezy "bored now" talk counter',
    install_requires=[
        'aiohttp'
    ],
    entry_points={
        'console_scripts': [
        ]
    }
)
