# lod-over-ipfs

A toy implementation of a migration tool of LOD datasets to IPFS.

**NOTE: this is a just a proof-of-concept example, not a final proposal**

## Overview

IPFS ([the InterPlanetary File System](https://github.com/ipfs)) is a distributed file system that seeks to connect all computing devices with the same system of files, using content-based addresses.

[Linked Data](https://en.wikipedia.org/wiki/Linked_data) is a set of methods for publishing structured data so that it can be interlinked and become more useful through semantic queries. Linked Open Data (LOD) is linked data that is open content.

Linked Data is currently published and maintained by a variety of organizations (Universties, public bodies, companies, communities, etc.) or even individuals.
As Linked Data is aimed at building applications on its top, lack of availability, scalability or even dataset removal make applications unusable or faulty. Migrating Linked Data datasets to IPFS is a solution to provide scalable and permanent access.

However, there are many ways of doing that migration still to be proposed and tested. Here we present a simplistic, straightforward approach that works with datasets described using the [Vocabulary of Interlinked Datasets (VoID)](https://www.w3.org/TR/void/). It simply uses VoID descriptions to get updates and moves the dumps of the data together with the VoID descriptions to IPFS with a set of minimal conventions.

## Setup

Uses ```rdflib``` to parse dataset descriptions and ```ipfsapi``` to interface with IPFS. You must have both installed.

You need to have access to an IPFS client. The current implementation has been tested with IPFS 0.4.3

## Example

The example migrates the [UK Ordnance Survey 50K Gazetteer dataset](http://data.ordnancesurvey.co.uk/datasets/50k-gazetteer). You can try with other similarly described datasets by changing the ```uk-gazetteer2ipfs.py
``` script, and changing other options by modifying the example code (command line options to come maybe in the future).

For example, you can customize the dataset by changing the following lines:

```py
# Data server location:
dataset_uri = "http://data.ordnancesurvey.co.uk/"
# Dataset identifier:
dataset_id = "http://data.ordnancesurvey.co.uk/id/data/50k-gazetteer"
```
