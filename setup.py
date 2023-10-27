from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fr:
    required_packages = [pkg.strip() for pkg in fr.readlines()]

setup(
    name="applibot",
    version="0.1.0",
    author="Supriyo Paul",
    author_email="paul.supriyo.paul@example.com",
    description="A tool to simplify the job application process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supriyopaul/applibot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=required_packages,
)
