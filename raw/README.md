# Raw Sources Repository

This directory contains **immutable source documents** deposited by the human researcher.

## Rules
1. **Immutability**: The LLM agent will read from files in this folder but will **never edit, rename, or delete** them.
2. **Acceptable Formats**:
   - Markdown documents (`.md`), such as articles captured via Obsidian Web Clipper.
   - Plain text notes, transcripts, or PDF text extracts (`.txt`, `.md`).
   - FASTA sequence headers or database dumps (`.fasta`, `.csv`).
3. **Ingestion Process**:
   - Once a file is added here, ask the LLM agent:
     `Ingest raw/<filename>`
   - The agent will process the contents, update the wiki entity/concept pages, refresh `wiki/index.md`, and log the action in `wiki/log.md`.
