"""
Setup script for TED Transcript Extractor.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ted-transcript-extractor",
    version="1.0.0",
    author="Xintong120",
    author_email="lxt2002120@gmail.com",
    description="A Python library for extracting transcripts from TED talks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xintong120/ted-transcript-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Education",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "ted-extractor=ted_extractor.cli:main",
        ],
    },
    keywords="ted, transcript, extraction, nlp, text-processing, education",
    project_urls={
        "Bug Reports": "https://github.com/Xintong120/ted-transcript-extractor/issues",
        "Source": "https://github.com/Xintong120/ted-transcript-extractor",
        "Documentation": "https://github.com/Xintong120/ted-transcript-extractor#readme",
    },
)
