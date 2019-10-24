# elixir_proteomics_QC
[![Nextflow version](https://img.shields.io/badge/nextflow-%E2%89%A50.31.0-brightgreen.svg)](https://www.nextflow.io/)
[![Docker Build Status](https://img.shields.io/docker/automated/biocorecrg/qcloud.svg)](https://cloud.docker.com/u/biocorecrg/repository/docker/biocorecrg/qcloud/builds)

gitter chat is https://gitter.im/elixir_proteomics_QC/community

## Installation instructions: 

* Install Singularity and Nextflow.
* Git clone pipeline: 

```
git clone https://github.com/elixir-cloud-proteomics-workflows/elixir_proteomics_QC.git
```

* Configure Nextflow: params.config 

```
zipfiles         = "$baseDir/path_to/*.zip"
```

Now input files must be zipped RAW files with this format: 

```
{QC01|QC02}_{checksum}.raw.zip 
```

where {QC01|QC02} is the sample type, QC01 for BSA and QC01 for HeLa (Human). 

For instance: 

QC01_93d2a97b9d0b35c9668663223bdef998.raw.zip

* Configure Nextflow: nextflow.config 

```
queue='name_of_cluster_queue'
```
and leave as it is: 

```
process.container = 'biocorecrg/qcloud:2.2'
container = 'biocorecrg/thermorawparser:0.1'
```

This will download the Docker image from Dockerhub for the knime part (1.3GB aprox) and ThermoFileRawParse part (375MB). 

* Run the pipeline: 

```
nextflow run elixir_proteomics_QC.nf -bg
```
Last, but not least: 

* Copy zipped RAWs to the `"$baseDir/path_to/*.zip` folder. 
