import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "WxConnector",
    version = "0.0.1",
    author = "david reid",
    author_email = "zathrasorama@gmail.com",
    description = ("Weather Station data collector."),
    license = "Apache License 2.0",
    keywords = "weather network serial",
    url = "http://www.david-reid.com/projects/wxconnector.html",
    packages=['wxconnector'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    test_suite='tests'
)
