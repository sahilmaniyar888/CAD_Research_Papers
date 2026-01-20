#!/usr/bin/env python3
"""
build_knowledge_graph.py
Build a research knowledge graph from enriched papers.
Graph structure: nodes (papers, authors, domains, techniques, representations)
and edges (relationships).
"""

import json
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict


def load_json(file_path: Path) -> List[Dict]:
    """Load JSON file."""
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, file_path: Path) -> None:
    """Save JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_node_id(node_type: str, value: str) -> str:
    """
    Create a unique node ID.

    Args:
        node_type: Type of node (paper, author, domain, etc.)
        value: Node value/name

    Returns:
        Unique node ID string
    """
    # Clean value for ID
    clean_value = value.replace(' ', '_').replace('/', '_')
    return f"{node_type}:{clean_value}"


def build_knowledge_graph(papers: List[Dict]) -> Dict:
    """
    Build knowledge graph from papers.

    Args:
        papers: List of enriched paper dictionaries

    Returns:
        Knowledge graph dictionary
    """
    # Initialize graph structure
    graph = {
        'nodes': [],
        'edges': [],
        'metadata': {
            'total_papers': 0,
            'total_authors': 0,
            'total_domains': 0,
            'total_techniques': 0,
            'total_representations': 0
        }
    }

    # Track unique nodes
    seen_nodes = set()

    # Track statistics
    author_paper_count = defaultdict(int)
    domain_paper_count = defaultdict(int)
    technique_paper_count = defaultdict(int)
    representation_paper_count = defaultdict(int)

    def add_node(node_id: str, node_type: str, properties: Dict) -> None:
        """Add node if not already present."""
        if node_id not in seen_nodes:
            graph['nodes'].append({
                'id': node_id,
                'type': node_type,
                'properties': properties
            })
            seen_nodes.add(node_id)

    def add_edge(source: str, target: str, edge_type: str, properties: Dict = None) -> None:
        """Add edge to graph."""
        graph['edges'].append({
            'source': source,
            'target': target,
            'type': edge_type,
            'properties': properties or {}
        })

    # Process each paper
    for paper in papers:
        paper_id = create_node_id('paper', paper['arxiv_id'])

        # Add paper node
        add_node(paper_id, 'paper', {
            'arxiv_id': paper['arxiv_id'],
            'title': paper['title'],
            'abstract': paper['abstract'],
            'published_date': paper['published_date'],
            'pdf_link': paper['pdf_link'],
            'citation_count': paper.get('citation_count', 0),
            'venue': paper.get('venue', 'arXiv'),
            'year': paper.get('year', paper['published_date'][:4])
        })

        # Add author nodes and edges
        for author in paper['authors']:
            author_id = create_node_id('author', author)

            add_node(author_id, 'author', {
                'name': author
            })

            add_edge(author_id, paper_id, 'authored', {
                'role': 'author'
            })

            author_paper_count[author] += 1

        # Add domain node and edge
        domain = paper.get('domain', 'Other Geometry-CAD AI')
        domain_id = create_node_id('domain', domain)

        add_node(domain_id, 'domain', {
            'name': domain
        })

        add_edge(paper_id, domain_id, 'belongs_to_domain')

        domain_paper_count[domain] += 1

        # Add technique nodes and edges
        for technique in paper.get('techniques', []):
            technique_id = create_node_id('technique', technique)

            add_node(technique_id, 'technique', {
                'name': technique
            })

            add_edge(paper_id, technique_id, 'uses_technique')

            technique_paper_count[technique] += 1

        # Add representation nodes and edges
        for representation in paper.get('representations', []):
            rep_id = create_node_id('representation', representation)

            add_node(rep_id, 'representation', {
                'name': representation
            })

            add_edge(paper_id, rep_id, 'uses_representation')

            representation_paper_count[representation] += 1

    # Update metadata
    graph['metadata']['total_papers'] = len([n for n in graph['nodes'] if n['type'] == 'paper'])
    graph['metadata']['total_authors'] = len([n for n in graph['nodes'] if n['type'] == 'author'])
    graph['metadata']['total_domains'] = len([n for n in graph['nodes'] if n['type'] == 'domain'])
    graph['metadata']['total_techniques'] = len([n for n in graph['nodes'] if n['type'] == 'technique'])
    graph['metadata']['total_representations'] = len([n for n in graph['nodes'] if n['type'] == 'representation'])

    # Add statistics to metadata
    graph['metadata']['top_authors'] = sorted(
        author_paper_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    graph['metadata']['domain_distribution'] = dict(domain_paper_count)
    graph['metadata']['technique_distribution'] = dict(technique_paper_count)
    graph['metadata']['representation_distribution'] = dict(representation_paper_count)

    return graph


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    enriched_papers_file = data_dir / 'enriched_papers.json'
    knowledge_graph_file = data_dir / 'knowledge_graph.json'

    print("=" * 60)
    print("Knowledge Graph Builder")
    print("=" * 60)

    # Load enriched papers
    papers = load_json(enriched_papers_file)
    print(f"\nLoaded {len(papers)} enriched papers")

    if not papers:
        print("No papers to process. Exiting.")
        return

    # Build knowledge graph
    print("\nBuilding knowledge graph...")
    graph = build_knowledge_graph(papers)

    # Save graph
    save_json(graph, knowledge_graph_file)

    # Print statistics
    print("\n" + "=" * 60)
    print("Knowledge Graph Statistics:")
    print("=" * 60)
    print(f"Total nodes: {len(graph['nodes'])}")
    print(f"  - Papers: {graph['metadata']['total_papers']}")
    print(f"  - Authors: {graph['metadata']['total_authors']}")
    print(f"  - Domains: {graph['metadata']['total_domains']}")
    print(f"  - Techniques: {graph['metadata']['total_techniques']}")
    print(f"  - Representations: {graph['metadata']['total_representations']}")
    print(f"\nTotal edges: {len(graph['edges'])}")

    print("\nDomain distribution:")
    for domain, count in sorted(
        graph['metadata']['domain_distribution'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  {domain}: {count}")

    print("\nTop 5 authors by paper count:")
    for author, count in graph['metadata']['top_authors'][:5]:
        print(f"  {author}: {count}")

    print("\n" + "=" * 60)
    print(f"Saved knowledge graph to {knowledge_graph_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
