from setuptools import find_packages
from setuptools import setup

DEPENDENCIES = [
    "google-api-python-client",
    "scikit-learn==0.24.2",
    "tensorflow==2.6",
    "keras==2.6.0",
    "transparentpath==1.1.32",
]
EXTRA_DEPENDENCIES = []

setup(
    name="SampleTrainer",
    version="0.1",
    description="A small example of how to train on gcp",
    author="Sagar Mishra",
    install_requires=DEPENDENCIES,
    extra_require=EXTRA_DEPENDENCIES,
    python_reqiures="=3.7",
    packages=find_packages(),
    include_package_data=True,
)
