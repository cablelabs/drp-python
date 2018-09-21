from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


def license():
    with open('LICENSE') as f:
        return f.read()


setup(
    name='drb_python',
    version='0.1',
    packages=['drb_python'],
    url='https://github.com/cablelabs/drb_python',
    license='Apache 2.0',
    author='Dan Schrimpsher',
    author_email='d.schrimpsher@cablelabs.com',
    description='Python Module to Support Digital Rebar API',
    long_description='Really, the funniest around.',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: Apache Software License 2.0 (Apache-2.0)'
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
    ],
    keywords='network boot, digital rebar, installation, NFV',
    install_requires=[
        'certifi',
        'chardet',
        'enum',
        'idna',
        'requests',
        'urllib3'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
