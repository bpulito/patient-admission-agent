# Assisted by watsonx Code Assistant
# watsonx Code Assistant did not check whether this code suggestion might be similar to third party code.

from setuptools import setup, find_packages

setup(
    name='reservation_tool_project',
    version='0.1',
    packages=find_packages(),
    install_requires=with open('requirements.txt') as f:
         install_requires = f.read().splitlines(),
)
