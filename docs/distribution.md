See https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/#creating-a-python-package

## Initial setup

Start a virtual environment

    python3 -m venv venv
    . venv/bin/activate

To create a PyPi distibution you need these packages

    pip install setuptools
    pip install twine

## New version

to create a new source distribution (version), update the version number in `setup.py` and run

    python3 setup.py sdist

test on testpypi (change the version number)

    twine upload --repository-url https://test.pypi.org/legacy/ dist/richard-0.1.0.tar.gz
    pip install -i https://test.pypi.org/simple/ richard==0.1.0

upload to pypi

    twine upload dist/richard-0.1.0.tar.gz

