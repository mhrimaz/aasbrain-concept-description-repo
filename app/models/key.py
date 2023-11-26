from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.key_types import KeyTypes
from app.models.rdfiable import RDFiable


class Key(BaseModel, RDFiable):
    type: KeyTypes
    value: constr(min_length=1, max_length=2000)
    # TODO: Add Pattern for Key

    def to_rdf(
        self,
        graph: rdflib.Graph = None,
        parent_node: rdflib.IdentifiedNode = None,
        prefix_uri: str = "",
        base_uri: str = "",
    ) -> (rdflib.Graph, rdflib.IdentifiedNode):
        if graph == None:
            graph = rdflib.Graph()
            graph.bind("aas", AASNameSpace.AAS)
        node = rdflib.BNode()
        rdflib.namespace
        graph.add((node, rdflib.RDF.type, AASNameSpace.AAS["Key"]))
        graph.add(
            (
                node,
                AASNameSpace.AAS["Key/type"],
                AASNameSpace.AAS[f"KeyTypes/{self.type.value}"],
            )
        )
        graph.add(
            (
                node,
                AASNameSpace.AAS["Key/value"],
                rdflib.Literal(self.value),
            )
        )
        return graph, node

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        payload = {}
        key_type: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Key/type"]),
            None,
        )
        value: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Key/value"]),
            None,
        )
        payload["type"] = key_type[key_type.rfind("/") + 1 :]
        payload["value"] = value.value
        return Key(**payload)
