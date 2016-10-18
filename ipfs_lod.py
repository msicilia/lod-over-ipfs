# -*- coding: utf-8 -*-
"""Publishes LOD datasets over IPFS based on their W3C VoID descriptions.

Assumptions (maybe not completely reasonable)
=============================================
- Datasets are described in VoID documents.
- Versioning can be discovered by looking at the dcterms:modified property.
- Actual data can be accessed via void:dataDump properties.
- Both the VoID description and the dataset are sent to IPFS.
- The VoID description is modified to include the addresses of the dumps over IPFS.
"""

import ipfsapi
import logging
from lodataset import LODatasetDescription
import os
import wget
import shutil

class IPFSLODPublisher(object):

    def __init__(self, dataset, client='127.0.0.1', port = 5001):
        """ Build the publisher from a LODataset.
        """
        self.dataset = dataset
        self.dataset_id = dataset.id
        self.last_modified = dataset["modified"]
        self.api = ipfsapi.connect(client, port)
        self.was_updated = True
        logging.getLogger().setLevel(logging.INFO)
        logging.info("Dataset " + dataset.id)
        logging.info("Last modified " +
                     self.last_modified.toPython().strftime("%Y-%m-%d %H:%M:%S"))

    def update(self):
        """ Reload the dataset and its description.
        If it was modified since last update, flags it for next publish.
        """
        lod = LODatasetDescription(self.dataset.desc.uri,
                                   self.dataset.desc.well_known)
        self.dataset = lod[self.dataset_id]
        newtime = self.dataset["modified"].toPython()
        # Check if the new last modification is more recent:
        if newtime > self.last_modified.toPython():
            self.was_updated = True
            logging.info("Dataset updated.")
        else:
            logging.info("Dataset remains the same.")
        self.last_modified = self.dataset["modified"]


    def publish(self, style="folder"):
        """Publish the Dataset to IPFS.
        Styles
        ======
        "folder" : the VOID file and dump files go in a common folder.
        "ipfsld" : a VOID file is augmented with IPFSLD links (not implemented)
        """
        if self.was_updated:
            self.was_updated = False
            if style=="folder":
                # Create the folder:
                folder = self.dataset.id.replace("/", "_")
                folder = folder + self.last_modified.toPython().strftime("%Y_%m_%d_%H:%M:%S")
                print(folder)
                if not os.path.exists(folder):
                    os.mkdir(folder)
                os.chdir(folder)
                # Serialize the VOID:
                #TODO: Include only the descriptions of the dataset, not all of them.
                self.dataset.desc.g.serialize(destination='void.ttl', format='turtle')
                # Get the dumps:
                dumps = self.dataset["dataDump"]
                # check if it is single dump:
                if not isinstance(dumps, list):
                    dumps = [dumps]
                for dump in dumps:
                    wget.download(dump)
                os.chdir("..")
                # Add to IPFS:
                res = self.api.add(folder, recursive=False)
                for r in res:
                    if r["Name"] == folder:
                        self.ipfs_addr = r["Hash"]
                logging.info(res)

                # cleanup
                shutil.rmtree(folder)
            else:
                raise ValueError("Publishing style " + style + "not supported." )
