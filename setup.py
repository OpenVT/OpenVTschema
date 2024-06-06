from setuptools import setup, find_packages

setup(
    name="openvt-schema",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jsonschema"
    ],
    entry_points={
        'console_scripts': [
            'validate-instance=scripts.validate_instance:main',
        ],
    },
)
