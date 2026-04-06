"""
    Gene co-occurence graph
        tracking which genes appear together
"""

import re
import networkx as nx

EXCLUDED = {"DNA", "RNA", "PCR", "USA", "WHO", "CI", "OR", "HR", "SD"}
#excluding some of the non gene symbols that are cummon and can match the pattern of gene symboles

def extract_genes(text: str) -> list[str]:#extracting every mentionned gene in a text
    pattern = r'\b[A-Z][A-Z0-9]{1,5}\b'#r'' raw str, \b word boundry it won't gene like patterns that are part of a longer word
                                        #[A-Z][A-Z0-9]{1,5} starts with uppercase followed by an uppercase or a digit repeated 1 to 5 times
    matches = re.findall(pattern, text)
    return list(set(m for m in matches if m not in EXCLUDED))

def update_graph(graph: nx.Graph, abstract: str) -> nx.Graph:
    genes = extract_genes(abstract)

    for gene in genes:# creating the first node
        if not graph.has_node(gene):
            graph.add_node(gene)

    for i in range(len(genes)):
        for j in range(i + 1, len(genes)): 
            gene_a = genes[i]
            gene_b = genes[j]
            if graph.has_edge(gene_a,gene_b):  # checking if there is already an edge between these two genes
                graph[gene_a][gene_b]["weight"] += 1 # if there is we add +1 to it's weight
            else:
                graph.add_edge(gene_a,gene_b, weight =1)# else we create an adge between these two
    
    return graph
