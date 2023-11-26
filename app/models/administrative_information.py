from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.has_data_specification import HasDataSpecification
from app.models.reference import Reference


class AdministrativeInformation(HasDataSpecification):
    version: Optional[constr(min_length=1, max_length=4, pattern=r"^(0|[1-9][0-9]*)$")] = None
    revision: Optional[constr(min_length=1, max_length=4, pattern=r"^(0|[1-9][0-9]*)$")] = None
    creator: Optional[Reference] = None
    templateId: Optional[constr(min_length=1, max_length=2000)] = None

    @staticmethod
    def append_as_rdf(instance: "AdministrativeInformation", graph: rdflib.Graph, parent_node: rdflib.IdentifiedNode):
        node = rdflib.BNode()
        graph.add((node, rdflib.RDF.type, AASNameSpace.AAS["AdministrativeInformation"]))
        HasDataSpecification.append_as_rdf(instance, graph, node)
        if instance.version:
            graph.add((node, AASNameSpace.AAS["AdministrativeInformation/version"], rdflib.Literal(instance.version)))
        if instance.revision:
            graph.add((node, AASNameSpace.AAS["AdministrativeInformation/revision"], rdflib.Literal(instance.revision)))
        if instance.creator:
            _, created_creator_node = instance.creator.to_rdf(graph, node)
            graph.add((node, AASNameSpace.AAS["AdministrativeInformation/creator"], created_creator_node))

        if instance.templateId:
            graph.add(
                (node, AASNameSpace.AAS["AdministrativeInformation/templateId"], rdflib.Literal(instance.templateId))
            )

        graph.add((parent_node, AASNameSpace.AAS["Identifiable/administration"], node))

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        # HasDataSpecification
        hasDataSpecification = HasDataSpecification.from_rdf(graph, subject)

        version_value = None

        revision_value = None

        creator_value = None

        template_id_value = None
        return AdministrativeInformation(
            version=version_value,
            revision=revision_value,
            creator=creator_value,
            templateId=template_id_value,
            embeddedDataSpecifications=hasDataSpecification.embeddedDataSpecifications,
        )
