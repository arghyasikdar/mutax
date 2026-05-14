# MutaX Architecture

MutaX is organized as a profile-aware mutation pipeline. Mutators are deliberately small:
each one owns one transformation family, emits candidate strings, and lets the engine attach
metadata, scores, entropy, and transformation history.

```mermaid
flowchart LR
  CLI["Typer/Rich CLI"] --> Engine["MutationEngine"]
  Config["YAML Config"] --> Engine
  Profiles["Profile Registry"] --> Engine
  Engine --> Pipeline["MutationPipeline"]
  Pipeline --> Mutators["Mutator ABC Implementations"]
  Mutators --> Models["Mutation Records"]
  Models --> Dedupe["Deduplication and Similarity Filter"]
  Dedupe --> Output["Rich Renderer / JSON / Text Export"]
```

Future HTTP testing modules can consume `MutationBatch` directly without parsing terminal output.

