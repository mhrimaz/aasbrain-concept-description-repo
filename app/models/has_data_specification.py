from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.embedded_data_specification import EmbeddedDataSpecification


class HasDataSpecification(BaseModel):
    embeddedDataSpecifications: Optional[List[EmbeddedDataSpecification]] = Field(None, min_items=1)

    @staticmethod
    def append_as_rdf(instance: "HasDataSpecification", graph: rdflib.Graph, parent_node: rdflib.IdentifiedNode):
        if instance.embeddedDataSpecifications and len(instance.embeddedDataSpecifications) > 0:
            for idx, data_specification in enumerate(instance.embeddedDataSpecifications):
                _, created_node = data_specification.to_rdf(
                    graph,
                )
                graph.add((created_node, AASNameSpace.AAS["index"], rdflib.Literal(idx)))
                graph.add(
                    (parent_node, AASNameSpace.AAS["HasDataSpecification/embeddedDataSpecifications"], created_node)
                )

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        embeddedDataSpecifications = []
        for embedded_ref in graph.objects(
            subject=subject, predicate=AASNameSpace.AAS["HasDataSpecification/embeddedDataSpecifications"]
        ):
            embeddedDataSpecifications.append(EmbeddedDataSpecification.from_rdf(graph, embedded_ref))

        if len(embeddedDataSpecifications) == 0:
            embeddedDataSpecifications = None

        return HasDataSpecification(embeddedDataSpecifications=embeddedDataSpecifications)
