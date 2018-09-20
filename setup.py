from setuptools import setup

setup(
    name='drb-python',
    version='0.1',
    packages=['', 'api', 'http', 'subnets_api'],
    package_dir={'': 'drb-python'},
    url='https://github.com/cablelabs/drb-python.git',
    license='Apache 2.0',
    author='Dan Schrimpsher',
    author_email='d.schrimpsher@cablelabs.com',
    description='Python Module to Support Digital Rebar API',
    install_requires=[
        'certifi',
        'chardet',
        'enum',
        'idna',
        'requests',
        'urllib3'
    ]
)
