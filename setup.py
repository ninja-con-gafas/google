from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name="google",
    version="0.10.2", 
    packages=find_packages(),
    install_requires=read_requirements(),
    author="ninja-con-gafas",
    description="The repository features a collection of modules to interact with Google products and services.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ninja-con-gafas/google",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
