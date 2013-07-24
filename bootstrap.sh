#!/bin/bash

virtualenv pyenv
source pyenv/bin/activate
pip install nose
pip install mock
pip install requests
nosetests tests/
