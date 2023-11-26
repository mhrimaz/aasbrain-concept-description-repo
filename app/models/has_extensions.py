from enum import Enum
from typing import Any, List, Optional, Union, Literal

import rdflib
from pydantic import BaseModel, Field, constr
from rdflib import RDF

from app.models.aas_namespace import AASNameSpace
from app.models.extension import Extension


class HasExtensions(BaseModel):
    extensions: Optional[List[Extension]] = Field(None, min_length=1)

    # TODO: instead of list Set might be better see Constraint AASd-077

    @staticmethod
    def append_as_rdf(instance: "HasExtensions", graph: rdflib.Graph, parent_node: rdflib.IdentifiedNode):
        if instance.extensions and len(instance.extensions) > 0:
            for idx, extension in enumerate(instance.extensions):
                _, created_node = extension.to_rdf(graph, parent_node)
                graph.add((created_node, AASNameSpace.AAS["index"], rdflib.Literal(idx)))
                graph.add((parent_node, AASNameSpace.AAS["HasExtensions/extensions"], created_node))

    @staticmethod
    def from_rdf(graph: rdflib.Graph, subject: rdflib.IdentifiedNode):
        extensions = []

        for extension_ref in graph.objects(subject=subject, predicate=AASNameSpace.AAS["HasExtensions/extensions"]):
            extensions.append(Extension.from_rdf(graph, extension_ref))

        if len(extensions) == 0:
            extensions = None
        return HasExtensions(extensions=extensions)
