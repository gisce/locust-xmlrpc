from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='locust-xmlrpc',
    version='0.2.0',
    description='XML-RPC Transport for Locust',
    long_description=readme,
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    url='https://github.com/gisce/locust-xmlrpc',
    packages=find_packages(),
    install_requires=[
        'locustio',
        'six'
    ],
    license='MIT',    
)
