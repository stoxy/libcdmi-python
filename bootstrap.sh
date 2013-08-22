#!/bin/bash

virtualenv pyenv
source pyenv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
nosetests test/
