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
mzmlfiles         = "$baseDir/path_to/*.mzML"
```

* Configure Nextflow: nextflow.config 

```
queue='name_of_cluster_queue'
```
and leave as it is: 

```
process.container = 'biocorecrg/qcloud:2.0'
```

This will download the Docker image from Dockerhub (1.7GB aprox). 

* Run thbe pipeline: 

```
nextflow run elixir_proteomics_QC.nf -bg
```
Last, but not least: 

* Copy mzMLs to the `"$baseDir/path_to/*.mzML` folder. 
* mzMLs notation, for instance: 
```
1af64022-7dcd-4f5e-8322-ffd893558c8a_QC02_3f98581e6291b298c2a11a4410d7198e.mzML 
```
where: 
* 1af64022-7dcd-4f5e-8322-ffd893558c8a: a uuid, leave it as it is. 
* QC02 is the sample type. In this case a HeLa. QC01 is for BSA. Leave this code as it is.
* 3f98581e6291b298c2a11a4410d7198e: is the checksum of the original raw file. This must be modified everytime for each file.

There are two mzML file samples here: https://www.dropbox.com/sh/8kf3dplmbuhldie/AABE_dSep2kgTKjSCooWInrwa?dl=0

* mzMLs generated by msconvert with this options: 
```
--32 --mzML --zlib --filter "peakPicking true 1-"
```
