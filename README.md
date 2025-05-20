# 🧠 DogBot Ops – Structured Content for RAG with Weaviate

This repository provides the **Data Operations layer** for the DogBot ecosystem. It manages structured content and schema definitions for a [Weaviate](https://weaviate.io) vector database, enabling **Retrieval-Augmented Generation (RAG)** through a **Content-as-Code** approach.

---

## 📐 Schema Overview

The Weaviate schema consists of the following collections:

- **Allgemein** – General information about dogs
- **Instinkte** – The four core canine instincts (Jagd, Territorial, Rudel, Sexual)
- **Instinktveranlagung** – Instinct distributions per breed group
- **Rassen** – Dog breeds, linked to their instinct profiles
- **Erziehung** – Training tasks mapped to instincts
- **Symptome** – Problem behaviors with underlying instinct drivers and solution hints

---

## 🔗 Relationships

The schema defines the following links:

- `Rassen → Instinktveranlagung` via `gruppen_code` and `hatInstinktveranlagung`
- `Erziehung → Instinkte` via `relevante_instinkte` and `betrifftInstinkte`
- `Symptome → Instinkte` via `beziehtSichAufInstinkte`
- `Symptome → Erziehung` via `empfohleneErziehungsaufgaben`

These references are set during import and validated in automated tests.

---

## 📦 Content-as-Code: Data & Automation

All content is stored and versioned in structured JSON files under `../data/json/`, including:

- `dogbot_content_Allgemein.json`
- `dogbot_content_Instinkte.json`
- `dogbot_content_Instinktveranlagung.json`
- `dogbot_content_Rassen.json`
- `dogbot_content_Erziehung.json`
- `dogbot_content_Symptome.json`

The setup process is fully automated via:

```bash
python3 setup_dogbot_weaviate.py --all
```

This will:
1. Delete the existing schema
2. Recreate all collections
3. Import and link all data
4. Run test scripts to validate setup

You can also run steps individually using `--schema`, `--import`, or `--test`.

---

## 🔍 Vectorization & RAG

All text fields are vectorized using `text2vec-openai`. Special attention has been given to the *"hundeperspektive_"* fields within `Symptome`, as they form the backbone of semantic search and GPT-based reasoning.

These fields allow the Dog Agent to:
1. Understand user questions
2. Retrieve matching symptoms
3. Identify underlying instincts
4. Generate contextual responses from a dog's perspective
5. Suggest personalized training tasks

---

## 📈 Planned Extensions

- Individual dog profiles linked to `Rassen`
- Auto-generated schema from structured content
- Weighted instinct analysis for symptom interpretation

---

## 🤝 DogBot Ecosystem Repositories

- 🤖 **Backend for GPT-based diagnosis**: [dogbot-agent](https://github.com/kemperfekt/dogbot-agent)
- 🖥️ **Frontend for human–dog interaction**: [dogbot-ui](https://github.com/kemperfekt/dogbot-ui)
- 🐶 **Project meta repo** with vision and coordination: [dogbot](https://github.com/kemperfekt/dogbot)

---

## ⚙️ Requirements

- Python 3.10+
- `weaviate-client` 4.x
- Access to a running Weaviate instance with OpenAI vectorizer
- Environment variables:
  - `WEAVIATE_URL`
  - `WEAVIATE_API_KEY`
  - `OPENAI_APIKEY`

---

## 📜 License

MIT License – see `LICENSE.md`.

---

*DogBot Ops: Because great GPT output starts with great structured data.*
