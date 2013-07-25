from setuptools import setup, find_packages
from version import get_git_version


setup(
    name="libcdmi-python",
    version=get_git_version(),
    description="""CDMI client library""",
    author="Ilja Livenson and Co",
    author_email="ilja.livenson@gmail.com",
    packages=find_packages(),
    namespace_packages=['stoxy'],
    zip_safe=False,  # martian grok scan is incompatible with zipped eggs
    install_requires=[
        "setuptools",  # Redundant but removes a warning
        ],
)
