See https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/#creating-a-python-package

setup.py

    pip install setuptools
    python setup.py check

create a source distribution

    python setup.py check

test on testpypi

    pip install twine

upload to testpypi

    twine upload --repository-url https://test.pypi.org/legacy/ dist/richard-0.1.0.tar.gz

token pypi: my_token
