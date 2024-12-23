#!/bin/bash

basedir=ngrams
languages=(
    fin
)

for lang in ${languages[@]}
do
    for fd in bigram_fd trigram_fd wildcard_fd word_fd
    do
        jsonfile="$basedir/$lang/$fd.json"
        zipfile="$basedir/$lang/$fd.zip"
        
        if [[ -f $zipfile ]] && ! [[ -f $jsonfile ]]
        then
            unzip $zipfile -d $basedir/$lang
        fi
    done
done
