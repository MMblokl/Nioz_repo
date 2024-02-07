#!bin/bash/
for d in ~/mock_references/* | egrep genomic
do
  echo $d | egrep "[A-Za-z]{0,}"
done
