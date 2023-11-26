from enum import Enum
from typing import Any, List, Optional, Union, Literal

import pydantic
import rdflib
from pydantic import BaseModel, Field, constr
from rdflib import Graph

from app.models.aas_namespace import AASNameSpace
from app.models.administrative_information import AdministrativeInformation
from app.models.rdfiable import RDFiable
from app.models.referable import Referable


class Identifiable(Referable):
    id: constr(min_length=1, max_length=2000)
    administration: Optional[AdministrativeInformation] = None

    @staticmethod
    def append_as_rdf(instance: "Identifiable", graph: rdflib.Graph, parent_node: rdflib.IdentifiedNode):
        graph.add((parent_node, AASNameSpace.AAS["Identifiable/id"], rdflib.Literal(instance.id)))

        if instance.administration:
            AdministrativeInformation.append_as_rdf(instance.administration, graph, parent_node)

        # Referable
        Referable.append_as_rdf(instance, graph, parent_node)

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode) -> "Identifiable":
        # Referable
        referable = Referable.from_rdf(graph, subject)

        id_value = None
        id_ref: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Identifiable/id"]),
            None,
        )
        id_value = id_ref.value

        administration_ref: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Identifiable/administration"]),
            None,
        )
        administration_value = None
        if administration_ref:
            administration_value = AdministrativeInformation.from_rdf(graph, administration_ref)

        return Identifiable(
            id=id_value,
            administration=administration_value,
            category=referable.category,
            idShort=referable.idShort,
            displayName=referable.displayName,
            description=referable.description,
            extensions=referable.extensions,
        )
