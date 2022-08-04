"""Installer for the plone_code_analysis package."""
from setuptools import setup


setup(
    name="plone_code_analysis",
    version="0.0.0",
    description="Plone Code Analysis.",
    author="Plone Community",
    author_email="dev@plone.org",
    url="https://github.com/plone/code-quality",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Framework :: Zope :: 5",
        "Framework :: Zope",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
    ],
    keywords="plone python code-quality",
    packages=["plone_code_analysis"],
    package_dir={"plone_code_analysis": "plone_code_analysis"},
    include_package_data=True,
    python_requires=">=3.7",
    zip_safe=False,
    install_requires=[],
)
