#!/usr/bin/env bash

# Edit: 
#JSON_MERGED_OUTPUT=/home/rolivella/mydata/toy_dataset/190219_Q_QC02_01_01_100ng_6583a564-93dd-4500-a101-b2fe56496b25_QC02_3f98581e6291b298c2a11a4410d7198e/json_subset
#JSON_FILENAME_OUTPUT="6583a564-93dd-4500-a101-b2fe56496b25_QC02_3f98581e6291b298c2a11a4410d7198e.json"

JSON_MERGED_OUTPUT=$1
JSON_FILENAME_OUTPUT=$2

# Remove any output merged file previously generated:
if [[ -f "$JSON_MERGED_OUTPUT/$JSON_FILENAME_OUTPUT" ]];
then
    rm ${JSON_MERGED_OUTPUT}/${JSON_FILENAME_OUTPUT}
fi

# Remove json files with size 0: 
for file in "$JSON_MERGED_OUTPUT"/*.json
do
    if [[ ! -s $file ]]; then 
        rm $file 
    fi
done

# Filter anly json files: 
JSON_TO_MERGE=(${JSON_MERGED_OUTPUT}/*.json)

counter=0
num_files=$((${#JSON_TO_MERGE[@]}-1))

JSON_MERGED='{"file" : {"checksum" : '

for json_file in "${JSON_TO_MERGE[@]}"; do

    if [[ -f $json_file ]] && [[ ! -s $json_file ]]; then
        echo "Skipping file $json_file because is empty." ;
    else
        if [[ "$counter" -eq 0 ]]; then
            JSON_MERGED=${JSON_MERGED}$(jq '.file.checksum' $json_file)' }, "data" : [ '$(jq -r '.["data"][]' $json_file)','
        elif [[ "$counter" -eq  "$num_files" ]]; then
            JSON_MERGED=${JSON_MERGED}$(jq -r '.["data"][]' $json_file)
        else 
            JSON_MERGED=${JSON_MERGED}$(jq -r '.["data"][]' $json_file)','
        fi 
        counter=$((counter+1))
    fi
done

JSON_MERGED=${JSON_MERGED}' ] }'

echo ${JSON_MERGED} | jq . > ${JSON_MERGED_OUTPUT}/${JSON_FILENAME_OUTPUT}
