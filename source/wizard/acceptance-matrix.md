# Universal Wizard Specialist Acceptance Matrix

This matrix defines the real-data acceptance coverage for the SF4 Universal Wizard specialist.

The acceptance package is read-only. It validates static structure, action chains, payload references, visual config and module installer bridge signals. It does not execute Bitrix, wizard actions, imports, DB writes or filesystem-changing runtime operations.

## Scenario Matrix

| Scenario | Source | Purpose | Expected Result |
| --- | --- | --- | --- |
| `simai-sveden-ready-runtime-master` | `/Users/rim/Sites/sf4.test/simai/wizard/master/simai.sveden` | Prove the specialist understands a complete runtime universal master: config, visuals, action chain, fallback action resolution and package payload paths. | `ready`, 19 actions, 0 findings, 16 high-risk side effects classified, logo/background paths resolved. |
| `simai-sf4university-missing-config` | `/Users/rim/Sites/university.test/simai/wizard/master/simai.sf4university` | Prove missing `.wizard.config.php` is a real blocker, not a guess. | `blocked`, findings include `missing_config` and `missing_master_config`. |
| `simai-sf4biblio-module-bridge` | `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4biblio` | Prove prebuilt module payload assembly is recognized before calling missing runtime `data/*` an error. | `ready`, installer bridge signals include `install_wizard_data`, `config_zip`, `medialibrary_zip`, `module_zip`, wrapper copy and redirect. |
| `simai-sf4med-module-bridge` | `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4med` | Prove another prebuilt module bridge variant is recognized. | `ready`, installer bridge signals include `install_wizard_data`, `runtime_master_data`, wrapper copy and redirect. |
| `simai-sf4university-assembled-module-bridge` | `/Users/rim/Sites/test.test/bitrix/modules/simai.sf4university` | Prove assembled installer payloads are recognized: config, iblock archives, php_interface, root and site. | `ready`, installer bridge signals include `install_ru_config`, `install_iblock`, `install_php_interface`, `install_ru_root`, `install_ru_site`, wrapper copy and redirect. |

## Capability Coverage

| Capability | Covered By |
| --- | --- |
| Master config detection | `simai-sveden-ready-runtime-master`, `simai-sf4university-missing-config` |
| Action chain parsing | `simai-sveden-ready-runtime-master` |
| Action file resolution | `simai-sveden-ready-runtime-master` |
| DATA input/output chain visibility | `simai-sveden-ready-runtime-master` |
| Side-effect classification | `simai-sveden-ready-runtime-master` |
| Visual contract | `simai-sveden-ready-runtime-master` |
| Missing config blocker | `simai-sf4university-missing-config` |
| Prebuilt module bridge | `simai-sf4biblio-module-bridge`, `simai-sf4med-module-bridge` |
| Assembled module bridge | `simai-sf4university-assembled-module-bridge` |
| Iblock archive package presence | `simai-sf4university-assembled-module-bridge` |

## Acceptance Runner

Run:

```bash
python3 scripts/sf4_wizard_acceptance.py --manifest source/wizard/acceptance-fixtures.json --json source/output/wizard-acceptance/report.json
```

Expected:

- runner status `success`;
- every scenario status `success`;
- generated per-scenario audit reports under `source/output/wizard-acceptance/audit/`;
- no live/runtime mutation.

## Stop Conditions

- A scenario source path no longer exists.
- A missing config scenario is no longer blocked without updating this matrix.
- Installer bridge signals change and the module packaging model must be re-studied.
- `sf4_wizard_audit.py` reports missing action files or missing payloads for a ready scenario.
- Acceptance runner attempts anything other than read-only audit plus JSON report writes.
