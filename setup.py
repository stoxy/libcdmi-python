from setuptools import setup, find_packages


setup(
    name="libcdmi-python",
    version='1.0alpha',
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
