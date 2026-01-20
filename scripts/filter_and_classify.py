#!/usr/bin/env python3
"""
filter_and_classify.py
Strictly filter papers to geometry-centric CAD AI only.
Classify accepted papers into taxonomy domains.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set, Optional


# Exclusion keywords - automatic rejection if found
EXCLUSION_KEYWORDS = [
    # CAE / Simulation
    'finite element', 'FEM', 'FEA', 'CAE',
    'structural analysis', 'stress analysis',
    'modal analysis', 'thermal analysis',
    'fluid dynamics', 'CFD',

    # Manufacturing / CAM
    'toolpath', 'CNC', 'CAM', 'machining',
    'additive manufacturing', '3D printing',
    'subtractive manufacturing',

    # Materials
    'material properties', 'material science',
    'metallurgy', 'composite materials',

    # Robotics (without geometry learning)
    'robot control', 'motion planning',
    'path planning', 'trajectory optimization',
    'manipulation without geometry',

    # Physics simulation
    'physics simulation', 'rigid body dynamics',
    'collision detection', 'contact mechanics'
]

# Strong inclusion signals (prioritize if found)
STRONG_INCLUSION_KEYWORDS = [
    'BREP', 'B-Rep', 'boundary representation',
    'sketch', 'constraint', 'parametric',
    'feature-based', 'feature graph',
    'CAD model', 'solid model',
    'geometric learning', 'geometry learning',
    'shape representation', 'shape generation',
    'CAD generation', 'CAD synthesis'
]

# Geometry representation keywords
GEOMETRY_REPRESENTATIONS = {
    'BREP': ['brep', 'b-rep', 'boundary representation', 'solid model'],
    'Sketch': ['sketch', 'drawing', '2d profile'],
    'Mesh': ['mesh', 'triangular mesh', 'polygon mesh'],
    'Point Cloud': ['point cloud', 'point set'],
    'Feature Graph': ['feature graph', 'feature tree', 'cad graph'],
    'Voxel': ['voxel', 'volumetric'],
    'Implicit': ['implicit', 'sdf', 'signed distance']
}

# Technique keywords
TECHNIQUES = {
    'Transformer': ['transformer', 'attention', 'bert', 'gpt'],
    'GNN': ['graph neural', 'gnn', 'graph convolution', 'gcn'],
    'Diffusion': ['diffusion', 'denoising', 'score-based'],
    'RL': ['reinforcement learning', 'rl', 'policy'],
    'CNN': ['convolutional', 'cnn', 'resnet', 'unet'],
    'VAE': ['vae', 'variational autoencoder'],
    'Hybrid': ['hybrid', 'multi-modal']
}

# Domain classification keywords
DOMAIN_KEYWORDS = {
    'CAD Geometry Core': [
        'cad', 'parametric', 'feature-based', 'brep', 'solid modeling'
    ],
    'Computer Vision for Geometry': [
        'image to cad', 'vision', 'reconstruction', 'recognition'
    ],
    'Reinforcement Learning for Geometry': [
        'reinforcement learning', 'rl', 'policy', 'agent'
    ],
    'Diffusion Models for Geometry': [
        'diffusion', 'denoising', 'score-based', 'generative'
    ],
    'Multimodal Geometry Models': [
        'multimodal', 'multi-modal', 'text to cad', 'language'
    ],
    'Graph-Based Geometry Learning': [
        'graph', 'gnn', 'graph neural'
    ],
    'Sketch / Constraint Understanding': [
        'sketch', 'constraint', 'drawing'
    ],
    'Shape Representation Learning': [
        'shape representation', 'geometry representation', 'encoding'
    ]
}


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


def load_seen_papers(file_path: Path) -> Set[str]:
    """Load set of already processed arXiv IDs."""
    if not file_path.exists():
        return set()

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return set(data)


def save_seen_papers(seen_ids: Set[str], file_path: Path) -> None:
    """Save set of processed arXiv IDs."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(seen_ids)), f, indent=2)


def should_exclude(paper: Dict) -> bool:
    """
    Check if paper should be excluded based on strict rules.

    Args:
        paper: Paper dictionary

    Returns:
        True if paper should be excluded
    """
    text = f"{paper['title']} {paper['abstract']}".lower()

    # Check exclusion keywords
    for keyword in EXCLUSION_KEYWORDS:
        if keyword.lower() in text:
            return True

    return False


def has_geometry_focus(paper: Dict) -> bool:
    """
    Check if paper has strong geometry focus.

    Args:
        paper: Paper dictionary

    Returns:
        True if paper has geometry focus
    """
    text = f"{paper['title']} {paper['abstract']}".lower()

    # Check for strong inclusion signals
    for keyword in STRONG_INCLUSION_KEYWORDS:
        if keyword.lower() in text:
            return True

    # Check for geometry representation mentions
    geometry_mentions = 0
    for rep_keywords in GEOMETRY_REPRESENTATIONS.values():
        for keyword in rep_keywords:
            if keyword.lower() in text:
                geometry_mentions += 1
                break

    # Require at least one geometry representation mention
    return geometry_mentions > 0


def classify_domain(paper: Dict) -> str:
    """
    Classify paper into ONE domain.

    Args:
        paper: Paper dictionary

    Returns:
        Domain string
    """
    text = f"{paper['title']} {paper['abstract']}".lower()

    # Score each domain
    domain_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        domain_scores[domain] = score

    # Return highest scoring domain
    if max(domain_scores.values()) > 0:
        return max(domain_scores, key=domain_scores.get)

    # Default to "Other Geometry-CAD AI" if no clear match
    return "Other Geometry-CAD AI"


def detect_techniques(paper: Dict) -> List[str]:
    """
    Detect techniques used in paper.

    Args:
        paper: Paper dictionary

    Returns:
        List of technique names
    """
    text = f"{paper['title']} {paper['abstract']}".lower()

    detected = []
    for technique, keywords in TECHNIQUES.items():
        for keyword in keywords:
            if keyword.lower() in text:
                detected.append(technique)
                break

    return detected if detected else ["Other"]


def detect_representations(paper: Dict) -> List[str]:
    """
    Detect geometry representations in paper.

    Args:
        paper: Paper dictionary

    Returns:
        List of representation names
    """
    text = f"{paper['title']} {paper['abstract']}".lower()

    detected = []
    for rep, keywords in GEOMETRY_REPRESENTATIONS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                detected.append(rep)
                break

    return detected if detected else ["Other"]


def filter_and_classify_papers(
    raw_papers: List[Dict],
    seen_ids: Set[str]
) -> tuple[List[Dict], Set[str]]:
    """
    Filter and classify papers.

    Args:
        raw_papers: List of raw papers from arXiv
        seen_ids: Set of already processed arXiv IDs

    Returns:
        Tuple of (accepted papers, updated seen IDs)
    """
    accepted = []
    new_seen_ids = seen_ids.copy()

    for paper in raw_papers:
        arxiv_id = paper['arxiv_id']

        # Skip if already seen
        if arxiv_id in seen_ids:
            print(f"  Skipping duplicate: {arxiv_id}")
            continue

        # Mark as seen
        new_seen_ids.add(arxiv_id)

        # Apply exclusion filter
        if should_exclude(paper):
            print(f"  Excluded (non-geometry): {paper['title'][:60]}...")
            continue

        # Check geometry focus
        if not has_geometry_focus(paper):
            print(f"  Excluded (weak geometry): {paper['title'][:60]}...")
            continue

        # Classify
        domain = classify_domain(paper)
        techniques = detect_techniques(paper)
        representations = detect_representations(paper)

        # Add classification metadata
        paper['domain'] = domain
        paper['techniques'] = techniques
        paper['representations'] = representations

        accepted.append(paper)
        print(f"  ✓ Accepted: {paper['title'][:60]}...")
        print(f"    Domain: {domain}")
        print(f"    Techniques: {', '.join(techniques)}")
        print(f"    Representations: {', '.join(representations)}")

    return accepted, new_seen_ids


def main():
    """Main execution function."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    raw_papers_file = data_dir / 'raw_papers.json'
    new_papers_file = data_dir / 'new_papers.json'
    seen_papers_file = data_dir / 'seen_papers.json'

    print("=" * 60)
    print("Paper Filter & Classifier - Geometry-Centric CAD AI")
    print("=" * 60)

    # Load raw papers
    raw_papers = load_json(raw_papers_file)
    print(f"\nLoaded {len(raw_papers)} raw papers")

    # Load seen papers
    seen_ids = load_seen_papers(seen_papers_file)
    print(f"Already processed: {len(seen_ids)} papers")

    # Filter and classify
    print("\nFiltering and classifying papers...\n")
    accepted_papers, updated_seen_ids = filter_and_classify_papers(
        raw_papers, seen_ids
    )

    # Save results
    save_json(accepted_papers, new_papers_file)
    save_seen_papers(updated_seen_ids, seen_papers_file)

    print("\n" + "=" * 60)
    print(f"Accepted: {len(accepted_papers)} new papers")
    print(f"Total processed: {len(updated_seen_ids)} papers")
    print("=" * 60)


if __name__ == "__main__":
    main()
