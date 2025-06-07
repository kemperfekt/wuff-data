# DogBot Ops (Data Management)

This repository manages the Weaviate vector database content and schemas for DogBot. For comprehensive documentation, please refer to the [main DogBot README](../README.md).

## Quick Links

- 📚 [Full Documentation](../README.md)
- 🏗️ [Architecture Overview](../README.md#️-architecture-overview)
- 🧠 [Core Instincts Model](../README.md#core-instincts-model)
- 🔧 [Development Setup](../README.md#-development)

## Local Usage

### Environment Setup

⚠️ **Important**: Configure environment variables before running any scripts:

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your credentials:
# - WEAVIATE_URL (your Weaviate cluster URL)
# - WEAVIATE_API_KEY (your Weaviate API key)
# - OPENAI_APIKEY (your OpenAI API key)
```

### Running Scripts

```bash
# Setup Weaviate with all data
python scripts/setup_dogbot_weaviate.py

# Import specific data
python scripts/weaviate_data_import.py

# View available options
python scripts/setup_dogbot_weaviate.py --help
```

### Security Notes

- Never commit `.env` files to version control
- API keys are loaded from environment variables only
- All scripts validate configuration before execution

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