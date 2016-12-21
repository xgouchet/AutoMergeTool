#!/bin/bash

WD=`pwd`
LOCAL_ROOT=`git rev-parse --show-toplevel`

cd $LOCAL_ROOT

dev/hooks/pre-commit

cd $WD
