#!/bin/bash

cp tests/java/merged.java tmp_merged.java

python ArachneMergeTool.py -b tests/java/base.java -l tests/java/local.java -r tests/java/remote.java -m tmp_merged.java -c tests/java/amt_java.config

echo "Merged : "
cat tmp_merged.java
