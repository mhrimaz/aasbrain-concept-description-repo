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

from .aas_namespace import AASNameSpace
from .data_element import DataElement
from .data_type_def_xsd import DataTypeDefXsd
from .lang_string_text_type import LangStringTextType
from .model_type import ModelType
from .reference import Reference
from .submodel_element import SubmodelElement
import base64


# TODO: check content type
class Blob(DataElement):
    value: Optional[str] = None
    contentType: str
    modelType: Literal["Blob"] = ModelType.Blob.value

    def to_rdf(
        self,
        graph: rdflib.Graph = None,
        parent_node: rdflib.IdentifiedNode = None,
        prefix_uri: str = "",
        base_uri: str = "",
        id_strategy: str = "",
    ) -> (rdflib.Graph, rdflib.IdentifiedNode):
        created_graph, created_node = super().to_rdf(graph, parent_node, prefix_uri, base_uri, id_strategy)
        created_graph.add((created_node, RDF.type, AASNameSpace.AAS["Blob"]))
        if self.value != None:
            created_graph.add(
                (
                    created_node,
                    AASNameSpace.AAS["Blob/value"],
                    rdflib.Literal(self.value, datatype=rdflib.XSD.base64Binary),
                )
            )
        created_graph.add(
            (
                created_node,
                AASNameSpace.AAS["Blob/contentType"],
                rdflib.Literal(self.contentType),
            )
        )
        return created_graph, created_node

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode) -> "Blob":
        value_value = None
        value_ref: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Blob/value"]),
            None,
        )
        if value_ref:
            value_value = value_ref
        content_type_value = None
        content_type_ref: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["Blob/contentType"]),
            None,
        )
        if content_type_ref:
            content_type_value = content_type_ref.value
        submodel_element = SubmodelElement.from_rdf(graph, subject)
        return Blob(
            value=value_value,
            contentType=content_type_value,
            qualifiers=submodel_element.qualifiers,
            category=submodel_element.category,
            idShort=submodel_element.idShort,
            displayName=submodel_element.displayName,
            description=submodel_element.description,
            extensions=submodel_element.extensions,
            semanticId=submodel_element.semanticId,
            supplementalSemanticIds=submodel_element.supplementalSemanticIds,
            embeddedDataSpecifications=submodel_element.embeddedDataSpecifications,
        )