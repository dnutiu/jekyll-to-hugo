import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jekyll-to-hugo",
    version="0.0.1",
    author="Denis Nutiu",
    author_email="nuculabs@outlook.com",
    description="Python library for converting jekyll md files to Hugo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="nuculabs.dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    scripts=["jekyll-to-hugo"],
    install_requires=[
        "beautifulsoup4==4.12.2",
        "PyYAML==6.0",
        "soupsieve==2.4.1",
        "pydantic==1.10.8",
    ],
    python_requires=">=3.10",
)
