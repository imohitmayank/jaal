# import
import codecs
import os.path
import setuptools

def read(rel_path):
    """Read a code file
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    """Fetch the version of package by parsing the __init__ file
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# fetch readme for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jaal",
    # version="0.0.6",
    version=get_version("jaal/__init__.py"),
    author="Mohit Mayank",
    author_email="mohitmayank1@gmail.com",
    description="jaal - your interactive network visualizer dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imohitmayank/jaal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={'': ['datasets/*', 'assest/logo.png', 'datasets/got/*']},
    include_package_data=True,
    install_requires=['dash>=1.19.0', 
                      'visdcc>=0.0.40', 
                      'pandas>=1.2.1', 
                      'dash_core_components>=1.15.0', 
                      'dash_html_components>=1.1.2', 
                      'dash_bootstrap_components>=0.11.1'],
)