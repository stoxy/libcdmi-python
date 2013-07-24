#!/bin/bash

virtualenv pyenv
source pyenv/bin/activate
pip install -r 'requirements-test'
nosetests test/
