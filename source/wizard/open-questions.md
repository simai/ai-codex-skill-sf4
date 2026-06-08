# Open Questions

## Config Provenance

- Where is `.wizard.config.php` for `simai.sf4university` generated or stored?
- Is `simai.sf4university` intended to be executed directly, or only installed through another module/wrapper?

## Runtime Component Source

- Which source is canonical for `simai:sf.wizard` and `simai:sf.wizard.stage`: packaged payload under `master/*/data/bitrix/components`, module source, or deployed `/bitrix/components/simai`?

## Action Versions

- Are action folders in `university.test` newer, older, or mixed relative to `sf4.test`?
- Which action library should be treated as canonical for specialist training?

## Encoding

- Some action files contain mojibake comments/messages. Should the specialist preserve legacy encoding notes, normalize to UTF-8 summaries only, or document encoding risk separately?

## Execution Boundaries

- Which wizard actions are allowed in local dev without backup?
- Which actions require ops gate even in staging?

## Graph Promotion

- Should the specialist become a raw-source specialist only, or also a graph-visible specialist/capability?
