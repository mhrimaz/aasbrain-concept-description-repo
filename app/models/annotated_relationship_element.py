#  MIT License
#
#  Copyright (c) 2023. Mohammad Hossein Rimaz
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the “Software”), to deal in
#  the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr
from rdflib import RDF

from app.models.aas_namespace import AASNameSpace
from app.models.has_data_specification import HasDataSpecification
from app.models.model_type import ModelType
from app.models.multi_language_property import MultiLanguageProperty
from app.models.property import Property
from app.models.reference import Reference
from app.models.relationship_element_abstract import RelationshipElementAbstract


class AnnotatedRelationshipElement(RelationshipElementAbstract):
    # TODO: workaround
    annotations: List[Union[Property, MultiLanguageProperty]] = Field(None, min_length=0, discriminator="modelType")
    modelType: Literal["AnnotatedRelationshipElement"] = ModelType.AnnotatedRelationshipElement.value

    def to_rdf(
        self,
        graph: rdflib.Graph = None,
        parent_node: rdflib.IdentifiedNode = None,
        prefix_uri: str = "",
        base_uri: str = "",
    ) -> (rdflib.Graph, rdflib.IdentifiedNode):
        created_graph, created_node = super().to_rdf(graph, parent_node, prefix_uri, base_uri)

        created_graph.add((created_node, RDF.type, AASNameSpace.AAS["AnnotatedRelationshipElement"]))
        return created_graph, created_node

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode) -> "AnnotatedRelationshipElement":
        relation_element_abstract = RelationshipElementAbstract.from_rdf(graph, subject)
        return AnnotatedRelationshipElement(
            first=relation_element_abstract.first,
            second=relation_element_abstract.second,
            qualifiers=relation_element_abstract.qualifiers,
            category=relation_element_abstract.category,
            idShort=relation_element_abstract.idShort,
            displayName=relation_element_abstract.displayName,
            description=relation_element_abstract.description,
            extensions=relation_element_abstract.extensions,
            semanticId=relation_element_abstract.semanticId,
            supplementalSemanticIds=relation_element_abstract.supplementalSemanticIds,
            embeddedDataSpecifications=relation_element_abstract.embeddedDataSpecifications,
        )
