import json
import os
import re
from typing import Union

import rdflib
import requests

from app.models.asset_administraion_shell import AssetAdministrationShell
from app.models.concept_description import ConceptDescription
from app.models.response import ConceptNotFoundException, DuplicateConceptException
from app.models.submodel import Submodel
import requests
from app.models import (
    base_64_url_encode,
    base_64_url_decode,
)
from urllib.parse import quote, unquote
import json
import uuid

graphdb_endpoint = "http://127.0.0.1:7200"  # GraphDB endpoint
repository_name = "aas"  # GraphDB repository name
base_url = f"{graphdb_endpoint}/repositories/{repository_name}/statements"
base_prefix = "https://aasbrain"
jena_base_url = f"http://127.0.0.1:3030/{repository_name}/update"


def gen_nested_submodel_collections(nesting_level=5):
    submodel_collection = {"idShort": f"root", "modelType": "SubmodelElementCollection"}
    current = submodel_collection
    for i in range(nesting_level):
        new_collection = {"idShort": f"child_{i}", "modelType": "SubmodelElementCollection"}
        current["value"] = [new_collection]
        current = new_collection
    return submodel_collection


def maximum_depth():
    for nesting_level in range(50, 200):
        print(nesting_level)
        nested_submodel_collections = gen_nested_submodel_collections(nesting_level=nesting_level)
        nested_submodel = {
            "id": f"NestedSubmodel_{str(uuid.uuid4())}",
            "kind": "Instance",
            "submodelElements": [nested_submodel_collections],
            "modelType": "Submodel",
        }
        basyx_root = "https://cloudrepo.h2894164.stratoserver.net"
        submodel_repo = f"{basyx_root}/submodels"
        payload = json.dumps(nested_submodel)
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", submodel_repo, headers=headers, data=payload)
        response.raise_for_status()


def if_exist(identifier: str) -> bool:
    url = f"{base_url}?pred=%3Chttps%3A%2F%2Fadmin-shell.io%2Faas%2F3%2F0%2FIdentifiable%2Fid%3E&obj=%22{quote(identifier,safe='')}%22"
    response = requests.get(url, headers={"Accept": "text/turtle"})
    g = rdflib.Graph().parse(response.content)
    return len(g) != 0


def get_concept_description_from_triplestore(cd_identifier_base64url: str) -> ConceptDescription:
    uri = f"{base_prefix}/{cd_identifier_base64url}"
    url = f"{base_url}?subj=%3C{quote(uri,safe='')}%3E"
    response = requests.get(url, headers={"Accept": "text/turtle"})
    response.raise_for_status()
    g = rdflib.Graph().parse(response.content)
    if len(g) == 0:
        raise ConceptNotFoundException()
    concept = ConceptDescription.from_rdf(g, rdflib.URIRef(uri))
    return concept


def delete_identifier_from_triplestore(identifier_base64url: str):
    uri = f"{base_prefix}/{identifier_base64url}"
    url = f"{base_url}?subj=%3C{quote(uri,safe='')}%3E"
    response = requests.delete(url, headers={"Accept": "text/turtle"})
    response.raise_for_status()


def insert_rdf_into_triplestore(element: Union[ConceptDescription, Submodel, AssetAdministrationShell]):
    if if_exist(element.id):
        raise DuplicateConceptException()

    graph, _ = element.to_rdf()
    rdf_data = graph.serialize(format="turtle_custom", base=base_prefix, encoding="utf-8")
    headers = {
        "Content-Type": "application/x-turtle",
    }

    try:
        response = requests.post(base_url, data=rdf_data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
        # print("RDF data inserted successfully.")
    except:
        print(f"HTTP Error:", graph.serialize(format="turtle_custom"))
        print(response.text)

    try:
        # INSERT IN JENA
        rdf_data = graph.serialize(format="turtle_custom")
        rdf_data_no_prefix = re.sub(r"@prefix.+> \.", "", str(rdf_data))
        rdf_data_no_prefix = re.sub(r"@base.+> \.", "", str(rdf_data_no_prefix))

        payload = f"prefix aas: <https://admin-shell.io/aas/3/0/>\nprefix xsd: <http://www.w3.org/2001/XMLSchema#>  \nINSERT DATA \n{{\n {rdf_data_no_prefix}\n }}"

        headers = {
            "Content-Type": "application/sparql-update",
        }
        jena_response = requests.request("POST", jena_base_url, headers=headers, data=payload)
        jena_response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
        # print("RDF data inserted successfully.")
    except Exception as ex:
        print(ex)
        print(f"HTTP Error:", rdf_data_no_prefix)
        print(response.text)


if __name__ == "__main__":
    basyx = "http://127.0.0.1:8085"
    size = 30
    submodels_file = f"C:/Users/Rimaz/OneDrive - Technologie-Initiative Smartfactory KL e.V/ReCircE intern/HosseinMasterarbeit/Presentations/Reasoner Demo/data/new data 11.2023/dataset2_json/submodels_{size}.json"
    url = f"{basyx}/submodels/"
    print("Adding Submodels")

    graph = rdflib.Graph()
    with open(submodels_file, encoding="utf-8") as f:
        submodels = json.load(f)
        for submodel in submodels:
            try:
                submodel_object = Submodel(**submodel)
                g, _ = submodel_object.to_rdf()
                # graph = graph + g
                insert_rdf_into_triplestore(submodel_object)
                payload = json.dumps(submodel)
                headers = {"Content-Type": "application/json"}
                response = requests.request("POST", url, headers=headers, data=payload)
            except Exception as ex:
                print("FAILED" + submodel_object.id)

    concepts_file = f"C:/Users/Rimaz/OneDrive - Technologie-Initiative Smartfactory KL e.V/ReCircE intern/HosseinMasterarbeit/Presentations/Reasoner Demo/data/new data 11.2023/dataset2_json/concepts_{size}.json"
    url = f"{basyx}/concept-descriptions/"
    print("Adding Concepts")
    with open(concepts_file, encoding="utf-8") as f:
        concepts = json.load(f)
        for concept in concepts:
            try:
                concept_object = ConceptDescription(**concept)
                g, _ = concept_object.to_rdf()
                # graph = graph + g
                insert_rdf_into_triplestore(concept_object)
                payload = json.dumps(concept)
                headers = {"Content-Type": "application/json"}
                response = requests.request("POST", url, headers=headers, data=payload)
            except:
                print("FAILED" + concept_object.id)

    shells_file = f"C:/Users/Rimaz/OneDrive - Technologie-Initiative Smartfactory KL e.V/ReCircE intern/HosseinMasterarbeit/Presentations/Reasoner Demo/data/new data 11.2023/dataset2_json/shells_{size}.json"
    url = f"{basyx}/shells/"
    print("Adding Shells")
    with open(shells_file, encoding="utf-8") as f:
        shells = json.load(f)
        for shell in shells:
            try:
                shell_object = AssetAdministrationShell(**shell)
                g, _ = shell_object.to_rdf()
                # graph = graph + g
                insert_rdf_into_triplestore(shell_object)
                payload = json.dumps(shell)
                headers = {"Content-Type": "application/json"}
                response = requests.request("POST", url, headers=headers, data=payload)
            except:
                print("FAILED" + shell_object.id)

    with open(f"merged_{size}.ttl", "w") as text_file:
        print("Total Statements: ", len(graph))
        text_file.write(graph.serialize(format="turtle_custom"))
