# Runtime Model

## Mental Model

The SF4 universal wizard is a stateful orchestration engine.

It separates:

- master scenario: `simai/wizard/master/<wizard_code>/`;
- action library: `simai/wizard/action/<action_code>/`;
- payload: `master/<wizard_code>/data/*`;
- runtime state: `SIMAI\Main\Configuration\Property` under the wizard code;
- UI/state runner: `simai:sf.wizard` and `simai:sf.wizard.stage`.

## Entry Point

`master/<wizard_code>/index.php`:

1. Defines language if needed.
2. Includes Bitrix prolog.
3. Includes `simai.framework`.
4. Loads wizard UI assets.
5. Resolves local wizard directory with `SIMAI\Wizard::getLocal(__DIR__)`.
6. Calls `simai:sf.wizard`.

Important parameters:

- `WIZARD_DIR`
- `WIZARD_TEMP_DIR`
- `WIZARD_CONFIG_FILE`
- `AJAX_TIME_STEP`
- `AJAX_TIME_INTERVAL`
- `CACHE_TYPE = N`

## Config Contract

`.wizard.config.php` returns:

- `description`: wizard metadata and UI style.
- `action`: ordered stages.

Action stage fields observed:

- `name`
- `code`
- `data_input_code`
- `data_output_code`
- `autocomplete`
- `condition`
- `parameter`

## Main Component Flow

`simai:sf.wizard`:

1. Requires admin user.
2. Defines `SF_WIZARD_DIR`, `SF_WIZARD_PATH`, `SF_WIZARD_TEMP_DIR`, `SF_WIZARD_TEMP_PATH`.
3. Loads `.wizard.config.php`.
4. Normalizes config keys to uppercase.
5. Reads previous runtime state from `Property::getInstance()->getArray($wizardCode)`.
6. Determines current stage from request and saved state.
7. Evaluates stage conditions against `$arResult["DATA"]`.
8. Skips stages whose condition is false.
9. Prepares `STAGE`: `CURRENT`, `NEXT`, `PREV`, `COUNT`, `STATUS`.
10. Selects current `ACTION` from config.
11. Resolves the action file:
    - first: `SF_WIZARD_DIR/action/<action_code>/action.php`;
    - fallback: `/simai/wizard/action/<action_code>/action.php`.
12. Sets action input from `DATA[data_input_code]`.
13. Writes full `$arResult` back to `Property`.
14. Includes component template.

## Stage Component Flow

`simai:sf.wizard.stage`:

1. Reads stored wizard state by `WIZARD_CODE`.
2. Applies stage AJAX id.
3. Writes state back to `Property`.
4. Includes its template.

The stage template executes the action through:

```php
require $arResult["ACTION"]["FILE"];
```

## Shared State

The data bus is `$arResult["DATA"]`.

`DATA_OUTPUT_CODE` writes action output:

```php
$arResult["DATA"][$arResult["ACTION"]["DATA_OUTPUT_CODE"]] = $arResult["ACTION"]["OUTPUT"];
```

`DATA_INPUT_CODE` reads prior output:

```php
$arResult["ACTION"]["INPUT"] = $arResult["DATA"][$arResult["ACTION"]["DATA_INPUT_CODE"]];
```

Observed core data packet:

- `site_config.site`
- `site_config.dir`
- `site_config.sf4`
- `site_config.rename_public`
- `site_config.master`

## Stage Statuses

- `NEW`: stage was created.
- `WORK`: action is running or waiting for AJAX continuation.
- `SUCCESS`: stage is complete and Next may be enabled.
- `ERROR`: action failed or required input is missing.

## Long-Running Actions

Long-running actions persist progress in `ACTION.DATA`, for example:

- `STEP_COPY`
- `STEP_ZIP`
- `STEP_UNZIP`
- `STEP_PATH`
- `STEP_BREAK_POINT`

They process until `AJAX_TIME_STEP` is reached, save state, and keep `STAGE.STATUS = WORK`.

`component_epilog.php` schedules repeated AJAX calls while status is `WORK`. Some actions also use their own `ajax.php` and set `STAGE.STATUS = SUCCESS` when finished.

## Conditions

Conditions compare values in `$arResult["DATA"]`.

Observed operators:

- `==`
- `!=`
- `>`
- `<`
- `>=`
- `<=`

Observed condition fields:

- `array`
- `key`
- `value`
- `operator`
- optional `type = OR`; default behavior is single condition or AND-like evaluation.

## Autocomplete

If `AUTOCOMPLETE = Y`, the wizard auto-advances after success. This is handled through template/epilog JavaScript that triggers the next button.

## Safety Notes

- Runtime requires admin user.
- Actions can write files, update sites, import iblocks, update options, add URL rewrite rules and modify public PHP files.
- Read-only analysis is safe; execution is not safe without explicit boundary, backup, rollback and target site confirmation.
