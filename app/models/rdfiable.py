from abc import ABC, abstractmethod

import rdflib


class RDFiable(ABC):
    @abstractmethod
    def to_rdf(
        self,
        graph: rdflib.Graph = None,
        parent_node: rdflib.IdentifiedNode = None,
        prefix_uri: str = "",
        base_uri: str = "",
    ) -> (rdflib.Graph, rdflib.IdentifiedNode):
        pass

    @staticmethod
    @abstractmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        pass
