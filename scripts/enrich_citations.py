#!/usr/bin/env python3
"""
enrich_citations.py
Enrich papers with citation data from Semantic Scholar public API.
No API key required - uses public endpoint with rate limiting.
"""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional


# Semantic Scholar API configuration
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
REQUEST_DELAY = 3  # seconds between requests to respect rate limits


def load_json(file_path: Path) -> List[Dict]:
    """Load JSON file."""
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: List[Dict], file_path: Path) -> None:
    """Save JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def query_semantic_scholar_by_arxiv(arxiv_id: str) -> Optional[Dict]:
    """
    Query Semantic Scholar by arXiv ID.

    Args:
        arxiv_id: arXiv paper ID

    Returns:
        Paper metadata dict or None if not found
    """
    # Clean arXiv ID (remove version if present)
    clean_id = arxiv_id.split('v')[0]

    url = f"{SEMANTIC_SCHOLAR_API}/paper/arXiv:{clean_id}"
    params = {
        'fields': 'citationCount,year,venue,publicationDate,externalIds'
    }

    full_url = f"{url}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(full_url)
        req.add_header('User-Agent', 'CAD-Research-Bot/1.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            return data

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # Paper not found in Semantic Scholar
        elif e.code == 429:
            print(f"    Rate limited, waiting 10s...")
            time.sleep(10)
            return None
        else:
            print(f"    HTTP error {e.code}")
            return None

    except Exception as e:
        print(f"    Error: {e}")
        return None


def query_semantic_scholar_by_title(title: str) -> Optional[Dict]:
    """
    Query Semantic Scholar by paper title (fallback).

    Args:
        title: Paper title

    Returns:
        Paper metadata dict or None if not found
    """
    url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
    params = {
        'query': title,
        'limit': 1,
        'fields': 'citationCount,year,venue,publicationDate,externalIds'
    }

    full_url = f"{url}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(full_url)
        req.add_header('User-Agent', 'CAD-Research-Bot/1.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())

            if data.get('data') and len(data['data']) > 0:
                return data['data'][0]

            return None

    except Exception as e:
        print(f"    Title search error: {e}")
        return None


def enrich_paper(paper: Dict) -> Dict:
    """
    Enrich paper with citation data from Semantic Scholar.

    Args:
        paper: Paper dictionary

    Returns:
        Enriched paper dictionary
    """
    print(f"\n  Enriching: {paper['title'][:60]}...")

    # Try arXiv ID lookup first
    s2_data = query_semantic_scholar_by_arxiv(paper['arxiv_id'])

    # Fallback to title search if arXiv lookup fails
    if not s2_data:
        print("    arXiv lookup failed, trying title search...")
        time.sleep(REQUEST_DELAY)
        s2_data = query_semantic_scholar_by_title(paper['title'])

    if s2_data:
        # Extract citation data
        paper['citation_count'] = s2_data.get('citationCount', 0)
        paper['venue'] = s2_data.get('venue', 'arXiv')
        paper['year'] = s2_data.get('year', paper['published_date'][:4])

        # Extract Semantic Scholar ID if available
        if 'paperId' in s2_data:
            paper['semantic_scholar_id'] = s2_data['paperId']

        print(f"    ✓ Citations: {paper['citation_count']}, Venue: {paper['venue']}")

    else:
        # Set defaults if enrichment fails
        paper['citation_count'] = 0
        paper['venue'] = 'arXiv'
        paper['year'] = paper['published_date'][:4]

        print("    ⚠ Enrichment failed, using defaults")

    return paper


def enrich_papers(papers: List[Dict]) -> List[Dict]:
    """
    Enrich all papers with citation data.

    Args:
        papers: List of paper dictionaries

    Returns:
        List of enriched papers
    """
    enriched = []

    for i, paper in enumerate(papers, 1):
        print(f"[{i}/{len(papers)}]", end=" ")

        enriched_paper = enrich_paper(paper)
        enriched.append(enriched_paper)

        # Rate limiting - wait between requests
        if i < len(papers):
            time.sleep(REQUEST_DELAY)

    return enriched


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    new_papers_file = data_dir / 'new_papers.json'
    enriched_papers_file = data_dir / 'enriched_papers.json'

    print("=" * 60)
    print("Citation Enrichment - Semantic Scholar API")
    print("=" * 60)

    # Load new papers
    new_papers = load_json(new_papers_file)
    print(f"\nLoaded {len(new_papers)} new papers to enrich")

    if not new_papers:
        print("No papers to enrich. Exiting.")
        return

    # Load existing enriched papers
    existing_enriched = load_json(enriched_papers_file)
    existing_ids = {p['arxiv_id'] for p in existing_enriched}

    # Filter out already enriched papers
    to_enrich = [p for p in new_papers if p['arxiv_id'] not in existing_ids]

    if not to_enrich:
        print("All papers already enriched. Exiting.")
        return

    print(f"Papers to enrich: {len(to_enrich)}")
    print(f"Estimated time: ~{len(to_enrich) * REQUEST_DELAY / 60:.1f} minutes")
    print("\nStarting enrichment...")

    # Enrich papers
    enriched = enrich_papers(to_enrich)

    # Merge with existing enriched papers
    all_enriched = existing_enriched + enriched

    # Save results
    save_json(all_enriched, enriched_papers_file)

    print("\n" + "=" * 60)
    print(f"Enriched {len(enriched)} new papers")
    print(f"Total enriched papers: {len(all_enriched)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
