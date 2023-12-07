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
import json
import urllib
from typing import Union
from itertools import zip_longest

import rdflib

from app.models.concept_description import ConceptDescription
from app.models.response import (
    GetConceptDescriptionsResult,
    Result,
    ConceptNotFoundException,
    DuplicateConceptException,
    UpdatePayloadIDMismatchException,
)
from app.repository import ConceptDescriptionRepository
from datetime import datetime, timezone
import requests
from app.models import (
    base_64_url_encode,
    base_64_url_decode,
)
from urllib.parse import quote, unquote


def sanitize_for_turtle(input_str: str) -> str:
    return input_str.replace('"', '\\"')


class GraphDBConceptDescriptionRepository(ConceptDescriptionRepository):
    graphdb_endpoint = "http://127.0.0.1:7200"  # GraphDB endpoint
    repository_name = "aas"  # GraphDB repository name
    base_url = f"{graphdb_endpoint}/repositories/{repository_name}/statements"
    base_prefix = "https://aasbrain"

    def if_exist(self, cd_identifier: str) -> bool:
        url = f"{self.base_url}?pred=%3Chttps%3A%2F%2Fadmin-shell.io%2Faas%2F3%2F0%2FIdentifiable%2Fid%3E&obj=%22{quote(cd_identifier,safe='')}%22"
        response = requests.get(url, headers={"Accept": "text/turtle"})
        g = rdflib.Graph().parse(response.content)
        return len(g) != 0

    def get_concept_description_from_triplestore(self, cd_identifier_base64url: str) -> ConceptDescription:
        uri = f"{self.base_prefix}/{cd_identifier_base64url}"
        url = f"{self.base_url}?subj=%3C{quote(uri,safe='')}%3E"
        response = requests.get(url, headers={"Accept": "text/turtle"})
        response.raise_for_status()
        g = rdflib.Graph().parse(response.content)
        if len(g) == 0:
            raise ConceptNotFoundException()
        concept = ConceptDescription.from_rdf(g, rdflib.URIRef(uri))
        return concept

    def delete_concept_description_from_triplestore(self, cd_identifier_base64url: str):
        uri = f"{self.base_prefix}/{cd_identifier_base64url}"
        url = f"{self.base_url}?subj=%3C{quote(uri,safe='')}%3E"
        response = requests.delete(url, headers={"Accept": "text/turtle"})
        response.raise_for_status()

    def insert_rdf_into_triplestore(self, concept_description: ConceptDescription):
        if self.if_exist(concept_description.id):
            raise DuplicateConceptException()

        graph, _ = concept_description.to_rdf()
        rdf_data = graph.serialize(format="turtle_custom", base=self.base_prefix, encoding="utf-8")
        print(rdf_data)
        headers = {
            "Content-Type": "application/x-turtle",
        }

        try:
            response = requests.post(self.base_url, data=rdf_data, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
            print("RDF data inserted successfully.")
        except:
            print(f"HTTP Error:", graph.serialize(format="turtle_custom"))
            print(response.text)

    async def connect_to_database(self, db_setting: dict):
        pass

    async def close_database_connection(self):
        pass

    async def get_concept_descriptions(self, query: dict, cursor=None, limit=100) -> GetConceptDescriptionsResult:
        pass

    async def get_concept_description(self, cd_id_base64url_encoded: str) -> ConceptDescription:
        result = self.get_concept_description_from_triplestore(cd_id_base64url_encoded)
        return result

    async def add_concept_description(self, concept_description: ConceptDescription) -> ConceptDescription:
        self.insert_rdf_into_triplestore(concept_description)
        return concept_description

    async def update_concept_description(
        self, cd_id_base64url_encoded: str, concept_description: ConceptDescription
    ) -> bool:
        pass

    async def delete_concept_description(self, cd_id_base64url_encoded: str) -> bool:
        pass

    async def get_concept_description_history(
        self, cd_id_base64url_encoded: str, cursor=None, limit=100
    ) -> GetConceptDescriptionsResult:
        pass
