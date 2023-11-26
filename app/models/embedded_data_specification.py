from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.data_specification_iec_61360 import DataSpecificationIec61360
from app.models.rdfiable import RDFiable
from app.models.reference import Reference


class EmbeddedDataSpecification(BaseModel, RDFiable):
    dataSpecification: Reference
    dataSpecificationContent: Union[DataSpecificationIec61360]

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
        graph.add((node, rdflib.RDF.type, AASNameSpace.AAS["EmbeddedDataSpecification"]))
        _, created_data_specification_node = self.dataSpecification.to_rdf(graph=graph, parent_node=node)
        graph.add(
            (node, AASNameSpace.AAS["EmbeddedDataSpecification/dataSpecification"], created_data_specification_node)
        )

        _, created_content_node = self.dataSpecificationContent.to_rdf(graph=graph, parent_node=node)
        graph.add(
            (
                node,
                AASNameSpace.AAS["EmbeddedDataSpecification/dataSpecificationContent"],
                created_content_node,
            )
        )

        return graph, node

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        # TODO: use type as discriminator

        data_specification_ref: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["EmbeddedDataSpecification/dataSpecification"]),
            None,
        )
        data_specification = Reference.from_rdf(graph, data_specification_ref)
        content = None
        content_ref: rdflib.URIRef = next(
            graph.objects(
                subject=subject, predicate=AASNameSpace.AAS["EmbeddedDataSpecification/dataSpecificationContent"]
            ),
            None,
        )
        content_ref_type: rdflib.URIRef = next(
            graph.objects(subject=content_ref, predicate=rdflib.RDF.type),
            None,
        )
        if content_ref_type == AASNameSpace.AAS["DataSpecificationIec61360"]:
            content = DataSpecificationIec61360.from_rdf(graph, content_ref)
        return EmbeddedDataSpecification(dataSpecification=data_specification, dataSpecificationContent=content)
