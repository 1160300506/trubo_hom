# trubo_hom
Taming Subgraph Isomorphism for RDF Query Processing.

according to Type-aware Transformation，RDF is transformed into a graph. The advantage of this graph is that it omits the object entity nodes corresponding to predicates of type and subclass, and it can directly transform them into labels corresponding to subject entity nodes.
By building a storage structure suitable for query, it can better support this type of label Graph query.
The algorithm also transforms the query statement into the corresponding graph in a similar way, and transforms it into a query tree, and uses the query tree to lock the candidate region. In this process, how to select the first query node and the matching order of query nodes are optimized.
