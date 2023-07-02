import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ciboulette-pkg-SGCMarkus", # Replace with your own username
    version="0.1.0",
    author="Touzan Dominique",
    author_email="markusornik@gmail.com",
    description="Ciboulette package for astronomy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SGCMarkus/ciboulette",
    package_dir = {#"ciboulette": ".",
                   "ciboulette.aavso": "aavso",
                   "ciboulette.base": "base",
                   "ciboulette.filtering": "filtering",
                   "ciboulette.indiclient": "indiclient",
                   "ciboulette.phd2client": "phd2client",
                   "ciboulette.spectrum": "spectrum",
                   "ciboulette.utils": "utils",
                   "ciboulette.sector": "sector"},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
