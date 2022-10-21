from setuptools import find_packages
from setuptools import setup

DEPENDENCIES = [
    "google-api-python-client",
    "numpy==1.23.4",
    "protobuf==3.20.2",         # some weird tf errors for 4.x versions
    "scikit-learn==1.0.2",
    "tensorflow==2.8.0",
]
EXTRA_DEPENDENCIES = []

setup(
    name="SampleTrainer",
    version="0.1",
    description="A small example of how to train on gcp",
    author="Sagar Mishra",
    install_requires=DEPENDENCIES,
    extra_require=EXTRA_DEPENDENCIES,
    python_reqiures=">3.6",
    packages=find_packages(),
    include_package_data=True,
)
