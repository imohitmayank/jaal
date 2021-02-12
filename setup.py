import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jaal",
    version="0.0.6",
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