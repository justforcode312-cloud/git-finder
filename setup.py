"""Setup script for git-finder package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="git-finder",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Show today's commits from all Git projects in a directory tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/git-finder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "git-finder=git_finder.cli:main",
            "gf=git_finder.cli:main",
        ],
    },
    keywords="git commits finder projects repository",
)
