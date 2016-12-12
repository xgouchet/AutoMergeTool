#!/bin/bash

WD=`pwd`
LOCAL_ROOT=`git rev-parse --show-toplevel`

cd $LOCAL_ROOT
cp dev/hooks/* .git/hooks
cd $WD
