# WuffChat Ops (Data Management)

This repository manages the Weaviate vector database content and schemas for WuffChat. For comprehensive documentation, please refer to the [main WuffChat README](../README.md).

## Quick Links

- 📚 [Full Documentation](../README.md)
- 🏗️ [Architecture Overview](../README.md#️-architecture-overview)
- 🧠 [Core Instincts Model](../README.md#core-instincts-model)
- 🔧 [Development Setup](../README.md#-development)

## Local Usage

```bash
# Setup Weaviate with all data
python setup_wuffchat_weaviate.py

# View available options
python setup_wuffchat_weaviate.py --help
```

## Data Collections

- **Allgemein**: General dog information
- **Instinkte**: Core instincts (Jagd, Territorial, Rudel, Sexual)
- **Instinktveranlagung**: Breed instinct predispositions
- **Rassen**: Dog breed information
- **Erziehung**: Training exercises
- **Symptome**: Behavioral symptoms

## Content-as-Code Approach

All data is managed as structured JSON files for version control and easy updates.

For detailed information, see the [main repository documentation](../README.md).