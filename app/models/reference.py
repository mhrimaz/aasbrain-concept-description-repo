from typing import Any, List, Optional, Union, Literal

import pydantic
import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.key import Key
from app.models.rdfiable import RDFiable
from app.models.reference_types import ReferenceTypes


class Reference(BaseModel, RDFiable):
    type: ReferenceTypes
    keys: List[Key] = Field(..., min_length=1)
    # this is not a mistake, since it is a recursive structure, we need to define it in this way.
    referredSemanticId: "Reference" = None

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
        graph.add((node, rdflib.RDF.type, AASNameSpace.AAS["Reference"]))

        graph.add((node, AASNameSpace.AAS["Reference/type"], AASNameSpace.AAS[f"ReferenceTypes/{self.type.value}"]))
        for idx, key in enumerate(self.keys):
            sub_graph, created_key_node = key.to_rdf(graph=graph, parent_node=node)
            graph.add((created_key_node, AASNameSpace.AAS["index"], rdflib.Literal(idx)))
            graph.add((node, AASNameSpace.AAS["Reference/keys"], created_key_node))
        if self.referredSemanticId:
            sub_graph, created_reference_node = self.referredSemanticId.to_rdf(graph=graph, parent_node=node)
            graph.add((node, AASNameSpace.AAS["Reference/referredSemanticId"], created_reference_node))
        return graph, node

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        payload = {}
        key_type: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Reference/type"]),
            None,
        )
        payload["type"] = key_type[key_type.rfind("/") + 1 :]
        keys = []
        for key in graph.objects(subject=subject, predicate=AASNameSpace.AAS["Reference/keys"]):
            created_key: Key = Key.from_rdf(graph, key)
            keys.append(created_key)
            # TODO: make sure about the order
        referred_semantic_id: rdflib.IdentifiedNode = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Reference/referredSemanticId"]),
            None,
        )
        referred_semantic_id_created = None
        if referred_semantic_id:
            referred_semantic_id_created = Reference.from_rdf(graph, referred_semantic_id)
        payload["keys"] = keys
        return Reference.model_construct(
            type=ReferenceTypes(payload["type"]), keys=keys, referredSemanticId=referred_semantic_id_created
        )
