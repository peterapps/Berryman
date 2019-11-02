#!/bin/bash

echo 'Extracting names from HSDB'
grep -oP '(?<=\<NameOfSubstance\>).*?(?=\<)' data/hsdb.xml > data/hsdb_names.txt
echo '  Done.'

echo 'Extracting names from ChemIDplus'
grep -oP '(?<=\<NameOfSubstance\>).*?(?=\<)' data/chemid.xml > data/chemid_names.txt
echo '  Done.'
