from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.rdfiable import RDFiable
from app.models.reference import Reference


class HasSemantics(BaseModel):
    semanticId: Optional[Reference] = None
    supplementalSemanticIds: Optional[List[Reference]] = Field(None, min_items=1)

    @staticmethod
    def append_as_rdf(instance: "HasSemantics", graph: rdflib.Graph, parent_node: rdflib.IdentifiedNode):
        if instance.semanticId:
            _, created_node_semantic_id = instance.semanticId.to_rdf(graph=graph, parent_node=parent_node)
            graph.add((parent_node, AASNameSpace.AAS["HasSemantics/semanticId"], created_node_semantic_id))
        if instance.supplementalSemanticIds and len(instance.supplementalSemanticIds) > 0:
            for idx, supplementalSemanticId in enumerate(instance.supplementalSemanticIds):
                _, created_node = supplementalSemanticId.to_rdf(graph=graph, parent_node=parent_node)
                graph.add((created_node, AASNameSpace.AAS["index"], rdflib.Literal(idx)))
                graph.add((parent_node, AASNameSpace.AAS["HasSemantics/supplementalSemanticIds"], created_node))

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode) -> "HasSemantics":
        semantic_id_ref: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["HasSemantics/semanticId"]),
            None,
        )

        semantic_id = None
        if semantic_id_ref:
            semantic_id = Reference.from_rdf(graph, semantic_id_ref)

        supplementalSemanticIds = []
        for supp_semantic_id in graph.objects(
            subject=subject, predicate=AASNameSpace.AAS["HasSemantics/supplementalSemanticIds"]
        ):
            supplementalSemanticIds.append(Reference.from_rdf(graph, supp_semantic_id))

        if len(supplementalSemanticIds) == 0:
            supplementalSemanticIds = None

        return HasSemantics(semanticId=semantic_id, supplementalSemanticIds=supplementalSemanticIds)
