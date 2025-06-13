# GraphRAG + Knowledge Base for Medical Device Assistant

## Project Overview
This document outlines the implementation of a Graph-based Retrieval Augmented Generation (GraphRAG) system for creating an intelligent medical device assistant, with a focus on blood pressure monitors.

## Query Examples

The system should be able to handle queries such as:

1. "Please list all blood pressure monitor models and their advantages and disadvantages."
2. "Compare all blood pressure monitor models and help me choose the right one."
3. "Which models have backlight features?"
4. "Which models have voice functionality?"
5. "What are the specifications of each blood pressure monitor model?"

## Agent Instructions

The agent should:
- Provide precise, factual answers about blood pressure monitors
- Compare different models based on features, price, and target users
- Make personalized recommendations based on user needs
- Present information in a structured, easy-to-understand format

## Implementation Steps

1. **Knowledge Base Creation**
   * GraphRAG + Neptune database
   * Vector-based RAG with OpenSearch as an alternative approach

2. **Document Processing**
   * Convert PDF documents to Markdown format for improved accuracy
   * Process the following blood pressure monitor manuals:
     - YE660C (with voice function)
     - YE670D
     - YE670E (with voice function + backlight + 360)
     - YE690C
     - YE8100C
     - YE8900A (with voice function)

3. **Knowledge Graph Construction**
   * Extract entities and relationships from processed documents
   * Build a comprehensive knowledge graph in Neptune

4. **User Interface Development**
   * Create a Streamlit application for interacting with the agent

## System Architecture

[Architecture diagram to be added]

## Future Roadmap

1. **Multi-Agent Collaboration**
   * Develop specialized agents for different medical device categories
   * Implement agent coordination mechanisms

2. **Multimodal Capabilities**
   * Integrate multimodal embedding models for image search
   * Enable visual query processing

3. **Enhanced Personalization**
   * Develop user profiles for more targeted recommendations
   * Implement feedback mechanisms for continuous improvement

## References

- [WeChat article on medical device assistants](https://mp.weixin.qq.com/s/z7VxAGueILkJ1ptMKWTzOA)
- [When to use Graphs in RAG: A Comprehensive Analysis for Graph Retrieval-Augmented Generation](https://arxiv.org/pdf/2506.05690)
