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
from rdflib.namespace import FOAF, RDF, Namespace
import pydantic
import rdflib
from pydantic import BaseModel, Field, constr
from rdflib import Graph, XSD
from rdflib.plugins.serializers.turtle import TurtleSerializer

import pydantic
from pydantic import BaseModel, Field, constr

from app.models.aas_namespace import AASNameSpace
from app.models.asset_kind import AssetKind
from app.models.resource import Resource
from app.models.specific_asset_id import SpecificAssetId


class AssetInformation(BaseModel):
    assetKind: AssetKind
    globalAssetId: Optional[
        constr(
            min_length=1,
            max_length=2000,
        )
    ] = None
    specificAssetIds: Optional[List[SpecificAssetId]] = Field(None, min_length=1)
    assetType: Optional[
        constr(
            min_length=1,
            max_length=2000,
        )
    ] = None
    defaultThumbnail: Optional[Resource] = None

    def to_rdf(self, graph=None, parent_uri="", blank_node=False):
        if graph == None:
            graph = Graph()
            graph.bind("aas", AASNameSpace.AAS)

        node = rdflib.URIRef("test")
        if blank_node:
            node = rdflib.BNode()
        graph.add((node, RDF.type, rdflib.URIRef(AASNameSpace.AAS["AssetInformation"])))
        graph.add(
            (
                node,
                rdflib.URIRef(AASNameSpace.AAS["AssetInformation/assetKind"]),
                rdflib.URIRef(AASNameSpace.AAS[f"AssetKind/{self.assetKind.value}"]),
            )
        )
        graph.add(
            (
                node,
                rdflib.URIRef(AASNameSpace.AAS["AssetInformation/globalAssetId"]),
                rdflib.Literal(self.globalAssetId),
            )
        )
        graph.add(
            (
                node,
                rdflib.URIRef(AASNameSpace.AAS["AssetInformation/assetType"]),
                rdflib.Literal(self.assetType),
            )
        )
        thumbnail = rdflib.BNode()
        # TODO: specificAssetIds, defaultThumbnail

        return node, graph

    @staticmethod
    def from_rdf(graph: Graph, subject):
        payload = {}
        asset_kind_uriref: rdflib.URIRef = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["AssetInformation/assetKind"]), None
        )
        if asset_kind_uriref:
            payload["assetKind"] = asset_kind_uriref[asset_kind_uriref.rfind("/") + 1 :]
        asset_type_uriref: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["AssetInformation/assetType"]),
            None,
        )
        if asset_type_uriref:
            payload["assetType"] = asset_type_uriref

        global_asset_id_uriref: rdflib.Literal = next(
            graph.objects(subject=subject, predicate=AASNameSpace.AAS["AssetInformation/globalAssetId"]),
            None,
        )
        if global_asset_id_uriref:
            payload["globalAssetId"] = global_asset_id_uriref

        return AssetInformation(**payload)
