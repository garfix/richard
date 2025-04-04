from setuptools import setup, find_namespace_packages

setup(
    name='richard',
    version='0.4.0',
    description='A Natural Language Understanding and Execution library',
    long_description='This library turns a question, statement or command from a ordinary human language text directly into Python executable code. It is completely rule-based and you as a developer define the code that is to be executed. The executable code can be any Python code, and there is specially suited for database access.',
    url='https://github.com/garfix/richard',
    author='Patrick van Bergen',
    author_email='patrick.vanbergen@gmail.com',
    license='MIT',
    package_dir={"": "richard"},
    packages=find_namespace_packages(where='richard'),

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
