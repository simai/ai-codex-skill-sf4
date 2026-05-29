# GrowGraph Contract Gate

Run before claiming repo-local `GGA9`:

```bash
python3 scripts/growgraph_contract_gate.py
```

The gate is read-only. It verifies semantic preservation, effectiveness,
adoption, federation export and integration review artifacts. It never grants
canonical writes.
