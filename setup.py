import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clearpasspy",
    version="1.1.1",
    author="zemerick1",
    author_email="zemerick@emerickcc.com",
    description="ClearPass API Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zemerick1/clearpasspy",
    packages=setuptools.find_packages(),
    py_modules=['clearpasspy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
)
