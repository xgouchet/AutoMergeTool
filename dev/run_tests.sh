#!/bin/bash


# make sure we run from the root
WD=`pwd`
LOCAL_ROOT=`git rev-parse --show-toplevel`

cd $LOCAL_ROOT

# run tests
coverage run -m nose2.__main__ && coverage report && coverage html

cd $WD
