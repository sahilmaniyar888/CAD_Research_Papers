#!/usr/bin/env python3
"""
fetch_arxiv.py
Fetch latest papers from arXiv focused on geometry-centric CAD AI.
Uses arXiv public API (no API key required).
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


# arXiv API configuration
ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Geometry-centric CAD AI search terms
SEARCH_TERMS = [
    "CAD",
    "BREP",
    "parametric modeling",
    "feature-based modeling",
    "computational geometry",
    "solid modeling",
    "sketch understanding",
    "shape representation",
    "geometric learning",
    "CAD generation",
    "3D CAD",
    "boundary representation"
]

# Search configuration
MAX_RESULTS = 100
LOOKBACK_DAYS = 30


def build_arxiv_query() -> str:
    """Build arXiv API query string for geometry-centric CAD papers."""
    # Combine search terms with OR logic
    terms = " OR ".join([f'all:"{term}"' for term in SEARCH_TERMS])

    # Focus on CS (Computer Science) categories
    category_filter = "cat:cs.CV OR cat:cs.LG OR cat:cs.GR OR cat:cs.CG OR cat:cs.AI"

    # Combine with AND logic
    query = f"({terms}) AND ({category_filter})"

    return query


def fetch_arxiv_papers(max_results: int = MAX_RESULTS) -> List[Dict]:
    """
    Fetch papers from arXiv API.

    Args:
        max_results: Maximum number of papers to fetch

    Returns:
        List of paper dictionaries
    """
    query = build_arxiv_query()

    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"

    print(f"Fetching papers from arXiv...")
    print(f"Query: {query[:100]}...")

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            xml_data = response.read()
    except Exception as e:
        print(f"Error fetching from arXiv: {e}")
        return []

    # Parse XML response
    papers = parse_arxiv_response(xml_data)

    print(f"Fetched {len(papers)} papers from arXiv")

    return papers


def parse_arxiv_response(xml_data: bytes) -> List[Dict]:
    """
    Parse arXiv API XML response.

    Args:
        xml_data: Raw XML response bytes

    Returns:
        List of parsed paper dictionaries
    """
    # Define XML namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }

    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall('atom:entry', namespaces):
        try:
            # Extract arXiv ID from the entry ID URL
            entry_id = entry.find('atom:id', namespaces).text
            arxiv_id = entry_id.split('/abs/')[-1]

            # Extract title (clean whitespace)
            title = entry.find('atom:title', namespaces).text
            title = ' '.join(title.split())

            # Extract authors
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name = author.find('atom:name', namespaces).text
                authors.append(name)

            # Extract abstract (clean whitespace)
            abstract = entry.find('atom:summary', namespaces).text
            abstract = ' '.join(abstract.split())

            # Extract published date
            published = entry.find('atom:published', namespaces).text
            published_date = published.split('T')[0]  # Get YYYY-MM-DD

            # Extract PDF link
            pdf_link = None
            for link in entry.findall('atom:link', namespaces):
                if link.get('type') == 'application/pdf':
                    pdf_link = link.get('href')
                    break

            if not pdf_link:
                pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            # Extract categories
            categories = []
            primary_category = entry.find('arxiv:primary_category', namespaces)
            if primary_category is not None:
                categories.append(primary_category.get('term'))

            for category in entry.findall('atom:category', namespaces):
                cat_term = category.get('term')
                if cat_term not in categories:
                    categories.append(cat_term)

            paper = {
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'published_date': published_date,
                'pdf_link': pdf_link,
                'categories': categories,
                'fetch_timestamp': datetime.now().isoformat()
            }

            papers.append(paper)

        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue

    return papers


def save_papers(papers: List[Dict], output_path: Path) -> None:
    """
    Save papers to JSON file.

    Args:
        papers: List of paper dictionaries
        output_path: Path to output JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(papers)} papers to {output_path}")


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    output_file = data_dir / 'raw_papers.json'

    print("=" * 60)
    print("arXiv Paper Fetcher - Geometry-Centric CAD AI")
    print("=" * 60)

    # Fetch papers
    papers = fetch_arxiv_papers(max_results=MAX_RESULTS)

    if not papers:
        print("No papers fetched. Exiting.")
        return

    # Save to file
    save_papers(papers, output_file)

    print("\n" + "=" * 60)
    print("Fetch complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
