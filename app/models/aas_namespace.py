import rdflib
from rdflib.namespace import DefinedNamespace, Namespace


class AASNameSpace:
    AAS = Namespace("https://admin-shell.io/aas/3/0/")
    CD_TYPE = rdflib.URIRef(AAS["ConceptDescription"])
    ID = rdflib.URIRef(AAS["Identifiable/id"])
