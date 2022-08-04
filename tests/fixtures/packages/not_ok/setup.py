"""Installer for the foo package."""
from setuptools import setup



setup(
    name="bar",
    version="1.0.0",
    description="A package to be used to test code quality tool",
    long_description="",
    long_description_content_type="text/markdown",
    keywords="plone python code-quality",
    packages=["bar"],
    package_dir={"bar": "bar"},
    include_package_data=True,
    python_requires=">=3.7",
    zip_safe=False,
    install_requires=[],
)
