from setuptools import setup

setup(
    name='ls2sql',
    description='Application to dump xml Lightspeed data into SQL',
    version='1.0.0',
    author='Andrew Hall',
    author_email='ahall@sunsetnovelties.com',
    packages=['ls2sql'],
    include_package_data=True,
    license='LICENSE.txt',
    install_requires=['pymssql','requests']
)