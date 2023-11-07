#!/bin/bash

set -e

for path in $(find /fred/oz005/search -type f -name "obs.header"); do
    if [ $path == "/fred/oz005/search/J1630-4733/2019-03-15-04:20:04/2/1070/obs.header" ]; then
        continue
    fi
    IFS="/"
    # Split the path into an array
    read -ra directories <<< "$path"
    beam=${directories[-3]}
    utc=${directories[-4]}
    jname=${directories[-5]}
    IFS=" "
    if [ -e "${path%%obs.header}/meertime.json" ]; then
        echo "Skipping $path"
    else
        echo "Making meetime.json for $path"
        EXIT_CODE=0
        generate_meerkat_json $path $beam -o ${path%%obs.header} || EXIT_CODE=$?
        if [ "$EXIT_CODE" -ne 42 ]; then
            if [ -e "meertime.json" ]; then
                ingest_obs "${path%%obs.header}/meertime.json"
            else
                echo "meertime.json does not exist."
            fi
        fi
    fi
done