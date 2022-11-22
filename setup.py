from setuptools import find_packages
from setuptools import setup

DEPENDENCIES = [
    "gcsfs==2022.2.0",
    "google-api-python-client==2.65.0",
    "scikit-learn==0.24.2",
    "tensorflow==2.6",
    "keras==2.6.0",
]
EXTRA_DEPENDENCIES = []

description = "An end-to-end example on how to train on GCP's AI-Platform"
setup(
    name="SampleTrainer",
    version="0.1",
    description=description,
    author="Sagar Mishra",
    install_requires=DEPENDENCIES,
    extra_require=EXTRA_DEPENDENCIES,
    python_reqiures="=3.7",
    packages=find_packages(),
    include_package_data=True,
)
