title: 'Story Toolkit: A Python Package for Narrative Generation and Coherence Analysis'
tags:
  - Python
  - natural language processing
  - creative writing
  - LLM
  - narrative generation
  - education technology
authors:
  - name: Milad Rezanezhad
    orcid: 0009-0006-1311-6960
    affiliation: 1
affiliations:
  - name: Independent Researcher, Iran
    index: 1
date: 09 May 2026
bibliography: paper.bib

# Summary

The `story-toolkit` is a comprehensive Python package designed to assist in the generation, structuring, and analysis of narratives. It provides a modular framework for creating characters, plots, dialogues, and fictional worlds. The package is designed for two primary audiences: researchers in computational creativity who need a structured environment for narrative generation experiments, and educators who wish to teach concepts of narrative theory and creative writing through a programmable interface.

# Statement of need

The field of computational storytelling has seen significant growth, yet available tools often focus on either raw text generation using language models or grammar-based text production. A notable gap exists for a package that bridges structured narrative elements (characters, plot points, world rules) with flexible generation backends, while also providing quantitative analysis for narrative coherence. `story-toolkit` addresses this gap by offering an integrated environment where users can build narratives from discrete components and optionally leverage large language models for enhanced dialogue generation. The package has already been integrated into the Python ecosystem via PyPI, making it accessible for both research and pedagogical applications.

# State of the field

Several Python packages exist for text generation, including `tracery` for grammar-based text expansion and `textgenrnn` for recurrent neural network-based generation. However, these tools primarily operate at the level of surface text. `story-toolkit` distinguishes itself by providing structured modules for distinct narrative elements (character arcs, plot structures, world-building rules). The closest comparable tools are research-specific codebases that are not packaged for general reuse. By providing a well-documented, installable package with a unified API, `story-toolkit` lowers the barrier to entry for researchers and educators interested in narrative generation and analysis.

# Software design

The package is organized into several modules: `core` (base classes for story elements), `generators` (for creating characters and plots), `nlp` (coherence checking and text analysis), and `llm` (an optional abstraction layer for OpenAI, Anthropic, and local models). This design separates core narrative logic from generation and analysis, allowing researchers to substitute their own generators or coherence metrics. The coherence checker, in particular, provides quantitative metrics that can be used in experimental studies of narrative quality. Unit tests for each module ensure reliability, and the package supports multiple export formats (JSON, PDF, EPUB, HTML) for interoperability.

# Research impact statement

`story-toolkit` has been adopted in several educational contexts for teaching narrative structure. The package has been released on PyPI and has accumulated initial installs from the Python community. The maintainer is available to support research collaborations and feature development for specific research needs.

# AI usage disclosure

Generative AI tools were used in the creation of this paper and the package documentation. Portions of docstrings and README sections were drafted with AI assistance, and boilerplate code structures were generated using AI. All AI-generated content was manually reviewed, edited, and verified for correctness by the human author. The core logic of the package (character, plot, coherence, and world-building modules) was written entirely by the human author without AI assistance.
