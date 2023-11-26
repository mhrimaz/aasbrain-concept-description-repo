
HoRi 2023.09.06 - Supported DBs will be MongoDB, and Redis.

HoRi 2023.09.06 - The first approach was to use Graphene, as it is the most popular tool out there. However, graphene-pydantic supports version 1. So I moved to Strawberry. It is also the suggested approach by FastAPI.

HoRi 2023.09.07 - As Neo4j Offers nice integration with GraphQL, Neo4j would be available as 3rd backend.

HoRi 2023.09.07 - Both Graphene and Strawberry are code-first approaches. As a result, two type should be created in parallel. For this reason, I move to Ariadne.

HoRi 2023.11.05 - why modelType: Literal["Property"] and not modelType: ModeType? this is because of the pydantic. the descriminator should be literal.

HoRi 2023.11.12 - RDFlib automatically generate namespace for unknown path. there is no parameter to disable it. The `getQName` in `rdflib/plugins/serializers/turtle` should return None
```python
def getQName(self, uri, gen_prefix=True):
    return None   
```

HoRi 2023.11.12 - the rdf serialization and `RDFiable` interface for inheritence is obviously not a good idea. Especially for multiple inheritence. A visitor pattern might be easier/same effort. First we make it work, then refactor.

HoRi 2023.11.21 - redoc doesn't work. content negotation docuemantion is hard! See https://github.com/tiangolo/fastapi/issues/4712

HoRi 2023.11.22 - `/concept-descriptions` offers pagination. If we want to have turtle output out of it there is not any clean way to handle it.
Then, we back to the question that do we need a turtle output out of our rest api? it is true that this is the job of serializer. so if someone wants turtle, they can ask for json and they convert it on their side. We can justify this and say the client doesn't have a compatible serializer. Another example https://wiki.lyrasis.org/display/FEDORA5x/RESTful+HTTP+API. Furthermore, then why we have xml response? to somehow mimic legacy endpoints? so why not have turtle? turtle does not have any place in web communication? then why not jsonld? we don't have json ld examples? Not sure!
Also why exactly we need `/sereialize` endpoint in specification? `/seralize` endpoint should be even only for environment aka `full-profile`.

HoRi 2023.11.22 - why `append_as_rdf` does not simply return an rdf node? in general i am not a fan of function with sideeffect, hard to debug and test. the reason was that we might need to generate the id of node based on parrent and attribute of the object. graph is also needed because triple should add in a graph. but maybe after final job, I can focus on refactoring.

HoRi 2023.11.23 - Add semantic triplestore backend. Jena was the first condidate, but since it doesn't have commercial capability I will go with graphdb free version. then if somone wants commercial, then they can easily change. But anyway, it shouldn't be that much graphdb dependent.

HoRi 2023.11.23 - Bulk endpoints? path? should it be atomic? here they provide non atomic https://developer.adobe.com/commerce/webapi/rest/use-rest/bulk-endpoints/, here they discourage non atomic https://adidas.gitbook.io/api-guidelines/rest-api-guidelines/execution/batch-operations it is just about preference.
it can be /concept-descriptions/bulkOperations like https://docs.oracle.com/en/cloud/paas/content-cloud/rest-api-manage-content/api-items-bulk-operations.html , https://www.ibm.com/docs/en/bpm/8.5.6?topic=resources-process-instance-bulk-operations
or it can be /bulk/concept-descriptions like https://mailchimp.com/developer/marketing/guides/run-async-requests-batch-endpoint/