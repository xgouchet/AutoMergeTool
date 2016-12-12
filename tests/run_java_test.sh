#!/bin/bash

cp tests/java/merged.java tmp_merged.java

./ArachneMergeTool.py -b tests/java/base.java -l tests/java/local.java -r tests/java/remote.java -m tmp_merged.java
