# Awesome CAD AI 🎨

![Automated](https://img.shields.io/badge/status-automated-brightgreen)
![Papers](https://img.shields.io/badge/papers-12-blue)
![Updated](https://img.shields.io/badge/updated-2026--01--20-orange)

> A curated, automatically maintained collection of research papers on **geometry-centric CAD AI**.
> Focused on BREP, parametric modeling, sketch understanding, and geometric learning.

**100% automated** using GitHub Actions • **100% free** tools • No manual curation

---

## 📋 Table of Contents

- [CAD Geometry Core](#cad-geometry-core) (2 papers)
- [Computer Vision for Geometry](#computer-vision-for-geometry) (1 papers)
- [Reinforcement Learning for Geometry](#reinforcement-learning-for-geometry) (1 papers)
- [Diffusion Models for Geometry](#diffusion-models-for-geometry) (2 papers)
- [Multimodal Geometry Models](#multimodal-geometry-models) (1 papers)
- [Graph-Based Geometry Learning](#graph-based-geometry-learning) (2 papers)
- [Sketch / Constraint Understanding](#sketch--constraint-understanding) (1 papers)
- [Shape Representation Learning](#shape-representation-learning) (2 papers)

---

## CAD Geometry Core

*Core CAD geometry modeling, parametric design, feature-based modeling, BREP operations*

| Paper | Venue | Links |
|-------|-------|-------|
| [SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks](https://arxiv.org/abs/2308.05739) | ICML 2023 | [PDF](https://arxiv.org/pdf/2308.05739.pdf) [Project](https://skexgen.github.io/) [Code](https://github.com/samxuxiang/SkexGen) |
| [DeepCAD: A Deep Generative Network for Computer-Aided Design Models](https://arxiv.org/abs/2105.09492) | SIGGRAPH Asia 2021 | [PDF](https://arxiv.org/pdf/2105.09492.pdf) [Project](https://www.cs.columbia.edu/~rw2786/deepcad/) [Code](https://github.com/ChrisWu1997/DeepCAD) |

---

## Computer Vision for Geometry

*Vision-based geometry understanding, image-to-CAD, 3D reconstruction from images*

| Paper | Venue | Links |
|-------|-------|-------|
| [CADTransformer: Panoptic Symbol Spotting Transformer for CAD Drawings](https://arxiv.org/abs/2206.08082) | CVPR 2022 | [PDF](https://arxiv.org/pdf/2206.08082.pdf) [Code](https://github.com/VITA-Group/CADTransformer) |

---

## Reinforcement Learning for Geometry

*RL-based CAD generation, geometric policy learning, sequential geometry construction*

| Paper | Venue | Links |
|-------|-------|-------|
| [AutoMate: Specialist and Generalist Assembly Policies over Diverse Geometries](https://arxiv.org/abs/2210.05258) | CoRL 2022 | [PDF](https://arxiv.org/pdf/2210.05258.pdf) [Project](https://automate-assembly.github.io/) |

---

## Diffusion Models for Geometry

*Diffusion-based generative models for CAD and geometric shapes*

| Paper | Venue | Links |
|-------|-------|-------|
| [Shap-E: Generating Conditional 3D Implicit Functions](https://arxiv.org/abs/2305.02463) | arXiv 2023 | [PDF](https://arxiv.org/pdf/2305.02463.pdf) [Code](https://github.com/openai/shap-e) |
| [Point-E: A System for Generating 3D Point Clouds from Complex Prompts](https://arxiv.org/abs/2211.13768) | arXiv 2022 | [PDF](https://arxiv.org/pdf/2211.13768.pdf) [Code](https://github.com/openai/point-e) |

---

## Multimodal Geometry Models

*Text-to-CAD, language-driven design, multimodal geometric generation*

| Paper | Venue | Links |
|-------|-------|-------|
| [Text2Shape: Generating Shapes from Natural Language by Learning Joint Embeddings](https://arxiv.org/abs/1809.02794) | ECCV 2018 | [PDF](https://arxiv.org/pdf/1809.02794.pdf) [Project](http://text2shape.stanford.edu/) [Code](https://github.com/kchen92/text2shape) |

---

## Graph-Based Geometry Learning

*Graph neural networks for CAD, feature graphs, topological learning*

| Paper | Venue | Links |
|-------|-------|-------|
| [StructureNet: Hierarchical Graph Networks for 3D Shape Generation](https://arxiv.org/abs/1912.03858) | SIGGRAPH Asia 2019 | [PDF](https://arxiv.org/pdf/1912.03858.pdf) [Project](https://cs.stanford.edu/~kaichun/structurenet/) [Code](https://github.com/daerduoCarey/structurenet) |
| [PartNet: A Large-scale Benchmark for Fine-grained and Hierarchical Part-level 3D Object Understanding](https://arxiv.org/abs/1911.10082) | CVPR 2019 | [PDF](https://arxiv.org/pdf/1911.10082.pdf) [Project](https://partnet.cs.stanford.edu/) [Code](https://github.com/daerduoCarey/partnet_dataset) |

---

## Sketch / Constraint Understanding

*2D sketch understanding, constraint solving, sketch-based modeling*

| Paper | Venue | Links |
|-------|-------|-------|
| [SketchGraphs: A Large-Scale Dataset for Modeling Relational Geometry in Computer-Aided Design](https://arxiv.org/abs/2003.13319) | arXiv 2020 | [PDF](https://arxiv.org/pdf/2003.13319.pdf) [Project](https://sketchgraphs.cs.princeton.edu/) [Code](https://github.com/PrincetonLIPS/SketchGraphs) |

---

## Shape Representation Learning

*Learning geometric representations, shape encodings, latent geometry spaces*

| Paper | Venue | Links |
|-------|-------|-------|
| [Learning to Infer Semantic Parameters for 3D Shape Editing](https://arxiv.org/abs/2104.05652) | 3DV 2021 | [PDF](https://arxiv.org/pdf/2104.05652.pdf) |
| [CAPRI-Net: Learning Compact CAD Shapes with Adaptive Primitive Assembly](https://arxiv.org/abs/2007.03983) | CVPR 2020 | [PDF](https://arxiv.org/pdf/2007.03983.pdf) [Project](https://capri-net.github.io/) [Code](https://github.com/ChrisWu1997/CAPRI-Net) |

---

## 🔧 System Architecture

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

