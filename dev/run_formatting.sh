#!/bin/bash


# make sure we run from the root
WD=`pwd`
LOCAL_ROOT=`git rev-parse --show-toplevel`

cd $LOCAL_ROOT

# Formatting the python files
yapf -i -r --style='{based_on_style:pep8, COLUMN_LIMIT=100}' .

cd $WD
