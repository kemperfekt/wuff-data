## dogbot-ops
Structured knowledge powering canine insights.
This repository contains the curated content and semantic building blocks for DogBot – including behavior patterns, symptoms, diagnostic questions, instinct explanations, breed profiles, and Weaviate schemas.

These operational datasets form the knowledge base that enables DogBot to understand and interpret dog behavior in a meaningful, structured way.

## 🧠 Purpose
dogbot-ops serves as the foundation for the DogBot diagnosis engine. It provides all the content needed for GPT to deliver context-aware, instinct-driven explanations and advice.

- The data is structured and optimized for semantic search via Weaviate, and includes:
- Symptoms – with tags, instinct variants, and at-home hypotheses
- Behavior patterns – offering clear explanations and therapy suggestions
- Instinct questions – used during diagnosis to narrow down instinctual causes
- Breed information – including instinct distributions and training notes
- Weaviate schemas – to structure and validate all data collections

## 🧱 Data Overview
Component           Description
symptome.json	    Problem behavior including tags and root cause guesses
verhaltensmuster	Structured explanations of typical behavioral patterns
rueckfragen_*	    Follow-up questions by instinct type
rassen.json	        Breed-specific instinct profiles
schema_*.py	        Scripts to define or update Weaviate schemas

## 🔄 Related Repositories
🤖 GPT-powered backend for diagnosis: https://github.com/kemperfekt/dogbot-agent
🖥️ Visual frontend for human–dog interaction: https://github.com/kemperfekt/dogbot-ui
🐶 Project meta-repo with vision and coordination: https://github.com/kemperfekt/dogbot
