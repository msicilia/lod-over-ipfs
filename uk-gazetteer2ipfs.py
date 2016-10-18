#!/usr/bin/env python
"""An example of uploading the UK Gazettter LOD dataset to IPFS.
"""

import lodataset
from ipfs_lod import IPFSLODPublisher
import time


def main():
    """ Load the VoID description of the dataset and
    polls recursively sending updates to IPFS.
    """
    # Data server location:
    dataset_uri = "http://data.ordnancesurvey.co.uk/"
    # Dataset identifier:
    dataset_id = "http://data.ordnancesurvey.co.uk/id/data/50k-gazetteer"

    desc = lodataset.LODatasetDescription(dataset_uri)

    # Prints the datasets described in the file:
    for d in desc.get_datasets():
        print("-----------------")
        print("Dataset id: ", d.id)
        if d["dataDump"] is None:
            print("Dumps not available.")
        else:
            print("Dumps available at: ", d["dataDump"])
        print("-----------------")

    # Get reference to the dataset we look for:
    gz = desc[dataset_id]

    # Instantiate a IPFS publisher on default location:
    ipfs = IPFSLODPublisher(gz)

    # Loop forever updating and publishing:
    try:
        while True:
            ipfs.publish()
            time.sleep(60*60) # Suspend for an hour
            ipfs.update()
    except KeyboardInterrupt:
        print("\n")
        print("Last IPFS hash for the folder of the dataset:" + ipfs.ipfs_addr)
        print("To retrieve the contents use: $ipfs ls <hash>")


if __name__ == "__main__":
    main()
