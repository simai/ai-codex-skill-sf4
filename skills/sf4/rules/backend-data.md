# Backend Data, Iblocks And Wizards

- In package/source templates do not concatenate `SITE_ID` for
  `IBLOCK_TYPE`/`IBLOCK_CODE` where the replacement flow expects canonical
  placeholders.
- For module installers and installable demo payloads (real entities created at
  install time) build site-aware codes from the target site id:
  - data iblock type: `sf_<site_code>_map_data`;
  - reference iblock type: `sf_<site_code>_map_ref`;
  - iblock code: `sf-<site_code>-<suffix>`;
  - keep component params aligned with resolved codes, including dynamic keys
    like `SOURCE_*_<iblock_code>`.
- Read `references/iblock-hl-standard.md` before creating new entities;
  configure iblock edit forms with `.iblock.config.php` and
  `.iblock.section.config.php`.
- Reuse `simai:sf.grid`, `simai:sf.iblock.*`, `simai:sf.highloadblock.grid`,
  `simai:sf.wizard`; use wizard import/export flows for package-style iblock/HL
  migration.
- Before release on backend-heavy tasks run `scripts/sf4_backend_risk_scan.py`
  and resolve critical findings (`IBLOCK_TYPE`/`IBLOCK_CODE` patterns,
  `DOMContentLoaded` misuse, `Block\Edit` overlay wrappers, asset loading).
- Wizard work: verify the runtime model (entry -> master -> stage -> action ->
  property storage) and installer payload assembly for
  `master/<wizard>/data/*`; action code matches the action folder name;
  install/update chains stay reproducible and file-safe.
