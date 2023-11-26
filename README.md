# AAS Brain Concept Description Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Docker Pulls](https://img.shields.io/docker/pulls/mhrimaz/aas-brain-concept-description-repo?logo=docker)](https://hub.docker.com/r/mhrimaz/aas-brain-concept-description-repo)
 [![Maturity badge - level 1](https://img.shields.io/badge/Maturity-Level%201%20--%20New%20Project-yellow.svg)](https://github.com/tophat/getting-started/blob/master/scorecard.md) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mhrimaz_aasbrain-concept-description-repo&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mhrimaz_aasbrain-concept-description-repo) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mhrimaz_aasbrain-concept-description-repo&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mhrimaz_aasbrain-concept-description-repo) 


AAS Brain features solutions and tries to overcome existing limitations and propose alternative approaches to deal with Asset Administration Shell. An attempt to make the AAS interaction better. 

**AAS is great, but let's make it even better**

- You need to create a lot of Concept Descriptions at the same time? Use the Bulk API

- Do you need to get multiple Concept Descriptions in one call? Use the Bulk API

- REST API interaction doesn't fit for your client side that only needs the unit symbol? Simply avoid overfetching and underfetching by using GraphQL. Use GraphQL endpoint.

- What is the relationship between concepts? Can I have a cluster view? Can I use my industrial Ontology? Our semantic backend is just for that, contact us!

- I don't need an API, I need a user interface. Do you have something like that? We have, contact us!

**Which backend is the best?**

Which backend is the best? The answer is obvious! It depends :)

- Semantic workloads: AAS Brain is the only repository that offers RDF and a semantic backend using Ontotext GraphDB (Free/Enterprise). By leveraging RDF model, which is part of the specification, you will not only have AAS in a knowledge graph, but you can further utilize SPARQL as a query language, SHACL for data quality assurance, and offer semantic reasoning. AAS Brain full profile offers such capabilities. If you are interested to know about its semantic capabilities, feel free to contact.

- Fastest retrival by ID: Redis is mostly suitable for fast retrival use cases when you already know the ID of Concept Description and you don't want to actually query the content of Concept Description.
In this type of workload Redis is the fastest. Unlike other in-memory alternatives, we don't use runtime environment heap space which is only suitable for testing purposes. Redis offers a horizontally scalable in-memory solution.

- Huge read/write: MongoDB is a scalable solution for heavy read and write applications. Similar to Eclipse BaSyx, we also have MongoDB backend. It is mostly suitable for a general workloads.

- GraphQL optimized with search capability: Thanks to the AAS-Connect master schema, and Neo4j GraphQL library, a graphql endpoint is at its most optimum way. Moreover, Neo4j automatically generates query parameters so you have much more flexibility here. So if you want to have GraphQL consider to use Neo4j backend.

- Hybrid: Thanks to our Redis-based in-memory solution, in future, you can leverage Redis as a caching layer for frequently accessed resources. This is a future plan.

## Usage

Docker commands and documentations will be provided.

## Licence

You are allowed to do whatever you want, just make the AAS great!

## Contributions

Any feedback, discussion, issue, ... are welcomed.


Code Quality provided by SonarCloud:

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=mhrimaz_aasbrain-concept-description-repo) 
