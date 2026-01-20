#!/usr/bin/env python3
"""
update_readme.py
Auto-generate and update README.md with papers organized by domain.
New papers are inserted at the TOP of each domain section.
"""

import json
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
from datetime import datetime


def load_json(file_path: Path) -> List[Dict]:
    """Load JSON file."""
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_taxonomy(file_path: Path) -> Dict:
    """Load taxonomy JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def group_papers_by_domain(papers: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group papers by domain.

    Args:
        papers: List of paper dictionaries

    Returns:
        Dictionary mapping domain to list of papers
    """
    grouped = defaultdict(list)

    for paper in papers:
        domain = paper.get('domain', 'Other Geometry-CAD AI')
        grouped[domain].append(paper)

    # Sort papers within each domain by date (newest first)
    for domain in grouped:
        grouped[domain].sort(
            key=lambda x: x['published_date'],
            reverse=True
        )

    return dict(grouped)


def format_paper_entry(paper: Dict) -> str:
    """
    Format a single paper entry for README.

    Args:
        paper: Paper dictionary

    Returns:
        Formatted markdown string
    """
    title = paper['title']
    authors = ', '.join(paper['authors'][:3])  # Limit to first 3 authors
    if len(paper['authors']) > 3:
        authors += ' et al.'

    year = paper.get('year', paper['published_date'][:4])
    citations = paper.get('citation_count', 0)
    domain = paper.get('domain', 'Other')
    techniques = ', '.join(paper.get('techniques', ['N/A']))
    representations = ', '.join(paper.get('representations', ['N/A']))
    pdf_link = paper['pdf_link']
    arxiv_id = paper['arxiv_id']

    entry = f"""- **{title}** ({year})
  {authors}
  Citations: {citations} | Techniques: {techniques} | Representations: {representations}
  [[PDF]]({pdf_link}) [[arXiv]](https://arxiv.org/abs/{arxiv_id})
"""

    return entry


def generate_readme(
    papers_by_domain: Dict[str, List[Dict]],
    taxonomy: Dict,
    total_papers: int
) -> str:
    """
    Generate complete README content.

    Args:
        papers_by_domain: Papers grouped by domain
        taxonomy: Taxonomy dictionary
        total_papers: Total number of papers

    Returns:
        Complete README markdown string
    """
    # Header
    readme = f"""# Awesome CAD AI - Geometry-Centric Research

![Automated](https://img.shields.io/badge/status-automated-brightgreen)
![Papers](https://img.shields.io/badge/papers-{total_papers}-blue)
![Updated](https://img.shields.io/badge/updated-{datetime.now().strftime('%Y--%m--%d')}-orange)

> A curated, automatically maintained collection of research papers on **geometry-centric CAD AI**.
> Focused on BREP, parametric modeling, sketch understanding, and geometric learning.

**100% automated** using GitHub Actions • **100% free** tools • No manual curation

---

## 📋 Table of Contents

"""

    # Generate TOC
    domain_order = [d['name'] for d in taxonomy['domains']]
    for domain in domain_order:
        if domain in papers_by_domain:
            count = len(papers_by_domain[domain])
            anchor = domain.lower().replace(' ', '-').replace('/', '')
            readme += f"- [{domain}](#{anchor}) ({count} papers)\n"

    readme += "\n---\n\n"

    # Add domain sections
    for domain_info in taxonomy['domains']:
        domain = domain_info['name']

        if domain not in papers_by_domain:
            continue

        papers = papers_by_domain[domain]

        readme += f"## {domain}\n\n"
        readme += f"*{domain_info['description']}*\n\n"
        readme += f"**{len(papers)} papers**\n\n"

        # Add papers
        for paper in papers:
            readme += format_paper_entry(paper)
            readme += "\n"

        readme += "---\n\n"

    # Footer
    readme += """## 🔧 System Architecture

This repository is **fully automated** and runs on GitHub Actions:

1. **Fetch** - Query arXiv for geometry-centric CAD papers
2. **Filter** - Strict filtering to exclude CAE, FEM, manufacturing
3. **Classify** - Assign papers to domains using keyword taxonomy
4. **Enrich** - Fetch citation data from Semantic Scholar
5. **Graph** - Build knowledge graph of papers, authors, techniques
6. **Update** - Auto-generate this README

**Tech Stack:**
- Python 3.10
- arXiv public API
- Semantic Scholar public API
- GitHub Actions (free tier)

---

## 📊 Knowledge Graph

A research knowledge graph is built from all papers, connecting:
- Papers → Authors
- Papers → Domains
- Papers → Techniques (Transformer, GNN, Diffusion, RL, etc.)
- Papers → Representations (BREP, Sketch, Mesh, Point Cloud, etc.)

See `data/knowledge_graph.json` for the full graph structure.

---

## 🤝 Contributing

This repository is **100% automated**. Papers are automatically discovered, filtered, and added.

**Scope:** Geometry-centric CAD AI only
- ✅ BREP, sketches, parametric modeling, geometric learning
- ❌ CAE, FEM, manufacturing, physics simulation

---

## 📄 License

This repository is licensed under MIT License.
Papers are copyrighted by their respective authors.

---

**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
**Auto-generated by:** [CAD Research Infrastructure](https://github.com)

"""

    return readme


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    enriched_papers_file = data_dir / 'enriched_papers.json'
    taxonomy_file = data_dir / 'taxonomy.json'
    readme_file = project_root / 'README.md'

    print("=" * 60)
    print("README Generator")
    print("=" * 60)

    # Load data
    papers = load_json(enriched_papers_file)
    taxonomy = load_taxonomy(taxonomy_file)

    print(f"\nLoaded {len(papers)} papers")

    if not papers:
        print("No papers to process. Exiting.")
        return

    # Group papers by domain
    papers_by_domain = group_papers_by_domain(papers)

    print("\nPapers by domain:")
    for domain, domain_papers in sorted(
        papers_by_domain.items(),
        key=lambda x: len(x[1]),
        reverse=True
    ):
        print(f"  {domain}: {len(domain_papers)}")

    # Generate README
    print("\nGenerating README...")
    readme_content = generate_readme(papers_by_domain, taxonomy, len(papers))

    # Write README
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("\n" + "=" * 60)
    print(f"README generated: {readme_file}")
    print(f"Total papers: {len(papers)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
