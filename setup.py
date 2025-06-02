from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="digital_marketplace",
    version="0.1.0",
    author="DigitalMarketplace Team",
    author_email="info@example.com",
    description="A digital marketplace smart contract implementation for Algorand",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/digital_marketplace",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "py-algorand-sdk>=1.13.0",
        "requests>=2.25.1",
    ],
)