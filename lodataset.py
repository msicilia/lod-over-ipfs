# -*- coding: utf-8 -*-
"""Builds a representation of a LOD dataset from a W3C VoID description.
See: https://www.w3.org/TR/void/
"""
import requests
import rdflib as rdf
from rdflib import Namespace
from rdflib.namespace import RDF
import os

class LODatasetDescription(object):
    def __init__(self, uri, well_known = True):
        """Builds a rdflib graph from a VoID description.
        Arguments
        ---------
        well_known: Use the IANA well-known URI convention.
                    See: https://www.w3.org/TR/void/#well-known
                    Else, you should provide a URI to the file.
        """
        self.g = rdf.Graph()
        self.datasets = None
        # IANA URI convention for VoID dataset descriptors.
        void_suffix = ".well-known/void"
        # Save the parameters used for updating:
        self.uri = uri
        self.well_known = well_known

        if well_known:
            # 'Accept' header required, to avoid defaulting to other formats.
            # TODO: Accept more formats rdflib can handle.
            r = requests.get(uri + void_suffix, headers = {"Accept": "text/turtle"})
            with open("void.ttl", "w") as file:
                file.write(r.text)
            result = self.g.parse("void.ttl", format="turtle")
            file.close()
            os.remove("void.ttl")
        else:
            result = self.g.get(uri)

    def __getitem__(self, key):
        """ Gets the dataset with the given resource id
        """
        filter = [d for d in self.get_datasets() if d.id == key]
        if len(filter)==1:
            return filter[0]
        else:
            return None


    def get_datasets(self):
        """A dataset description may have more than one void:Dataset description.
        This parses and gets the list of datasets described.
        """
        if self.datasets is None:
            self.datasets = []
            void_ns = Namespace("http://rdfs.org/ns/void#")
            for s,p,o in self.g.triples( (None, RDF.type, void_ns.Dataset) ):
                d = LODataset(s, self)
                self.datasets.append(d)

        return self.datasets

class LODataset(object):

    # Constants for VoID predicates.
    VOID = Namespace("http://rdfs.org/ns/void#")
    DCTERMS = Namespace("http://purl.org/dc/terms/")


    def __init__(self, resource, desc):
        """ Represents a single void:Dataset.
        """
        self.resource = resource
        self.desc = desc


    def __getitem__(self, key):
        """ Access descriptions based on dict item get.
        key: A String with one of the VoID predicates.
        """
        #TODO: Add support for all VoID predicates not in void namespace.
        dcterm_preds = ["title", "description", "creator", "publisher",
                         "contributor", "source", "date", "created",
                         "issued", "modified"]
        items = []
        if key in dcterm_preds:
            ns = self.DCTERMS
        else:
            ns = self.VOID
        for s,p,o in self.desc.g.triples( (self.resource, ns[key], None) ):
            # TODO: Check the different cases: URIRef, Literal, BNode.
            items.append(o)


        # Return None, single value or list:
        if items == []:
            return None
        elif len(items)==1:
            return items[0]
        else:
            return items

    @property
    def id(self):
        return self.resource.strip()
