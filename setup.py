import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jaal",
    version="0.0.1",
    author="Mohit Mayank",
    author_email="mohitmayank1@gmail.com",
    description="jaal - your interactive network visualizer dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imohitmayank/jaal",
    packages=setuptools.find_packages(),
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)