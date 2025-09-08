from setuptools import setup, find_packages

setup(
    name="namae-py",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "namae": ["data/particles.txt"],
    },
    python_requires=">=3.7",
)