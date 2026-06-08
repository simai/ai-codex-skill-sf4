# Universal Wizard Visual Contract

This file captures how SF4 universal masters and legacy Bitrix wizards control appearance and step output.

## SF4 Universal Master Visual Source

Primary source is `.wizard.config.php` `description`.

Observed fields in `simai.sveden`:

```php
"description" => array(
    "name" => Loc::getMessage("WIZARD_SOLUTION"),
    "code" => "simai_sveden",
    "stage_renew" => "Y",
    "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
    "author" => "Rim Zabarov <rim@zabarov.ru>",
    "copyright" => "...",
    "background" => array(
        "color" => "#134A5B",
        "image" => Wizard::getLocal(__DIR__) . "/image/wizard_bg.jpg",
        "position" => "bottom",
        "repeat" => "no-repeat",
        "size" => "cover",
        "attachment" => "fixed",
    ),
    "color" => array(
        "primary" => "#F34E3F",
        "secondary" => "#134A5B",
    ),
    "modifier" => array(
        "page_body" => "theme-dark bg-theme-50 p-md-5 py-4 py-lg-6",
        "wizard_wrap" => "r-2 w-80 wr-md-7 mx-auto",
        "wizard_area" => "p-4 bg-white theme-light",
        "wizard_nav" => "p-4 bg-white",
        "wizard_copyright" => "p-2 t-center t--1 c-text-secondary l-inherit l-underline",
    ),
)
```

## Field Contract

| Field | Purpose | Rules |
|---|---|---|
| `description.name` | Master title shown in UI/header context | Use `Loc::getMessage` for localization. |
| `description.code` | Wizard storage key and logical code | Must be stable; changing it resets/changes persisted state namespace. |
| `stage_renew` | Allows stage state refresh/restart behavior | Verify runtime behavior before changing on installed masters. |
| `logo` | Logo image path | Use `Wizard::getLocal(__DIR__)`; verify file exists. |
| `author` | Metadata/visible author depending on template | Avoid sensitive personal data in public packages unless intended. |
| `copyright` | Footer/copyright HTML | May include links; keep safe and localized if needed. |
| `background.color` | Fallback/background color | Must contrast with wizard content and loading state. |
| `background.image` | Wizard page background image | Use real asset path; ensure package copies image. |
| `background.position` | CSS background-position | Use valid CSS values. |
| `background.repeat` | CSS background-repeat | Use valid CSS values. |
| `background.size` | CSS background-size | `cover` is common for full-page background. |
| `background.attachment` | CSS background-attachment | `fixed` is observed; test mobile behavior if visual polish matters. |
| `color.primary` | Primary accent | Used by template/theme styles; verify contrast. |
| `color.secondary` | Secondary accent | Used by template/theme styles; verify contrast. |
| `modifier.page_body` | Classes on page body/wrapper | Should use existing SF4 utility/theme classes. |
| `modifier.wizard_wrap` | Outer wizard container classes | Controls width/radius/margins. |
| `modifier.wizard_area` | Main content area classes | Controls background/padding/theme. |
| `modifier.wizard_nav` | Navigation area classes | Controls button row styling. |
| `modifier.wizard_copyright` | Footer classes | Controls copyright text style. |

## Step Visual Output

Each action entry contributes:

- `name`: displayed step/action title;
- `autocomplete`: can allow automatic progress when action completes;
- `GO_BACK`/navigation behavior if action sets it;
- HTML printed by `action.php`;
- button enabled/disabled state through runtime and action JS.

Action examples:

- `site.choice.sveden` renders form controls and gates the Next button until the selected site data is saved.
- `iblock.import.archive` renders a progress div and JS queue.
- `iblock.export.archive` renders a progress div and JS queue.
- `info` renders final message/links with placeholder substitution.

Specialist rule: visible action text belongs in lang files or config `Loc::getMessage`, not hard-coded action bodies unless package-specific.

## Progress And Navigation Contract

The universal wizard UI depends on persisted stage status:

- `NEW`: action has not started;
- `WORK`: current stage is running or waiting for AJAX/polling;
- `SUCCESS`: stage can advance;
- `ERROR`: stop and show error state.

Navigation is affected by:

- runtime template buttons (`sf-wizard-stage-prev`, `sf-wizard-stage-next`);
- action-local JS enabling/disabling buttons after AJAX work;
- component epilog polling when status remains `WORK`.

For long actions, visual progress must not only show text; it must eventually update storage to `SUCCESS`.

## Legacy Bitrix Wizard Visuals

Legacy solution wizards (`simai.fund`, `simai.educenter`, `simai.school`) use standard Bitrix wizard assets and steps:

- `.description.php`;
- `wizard.gif`;
- `wizard_clear.gif`;
- `css/panel.css`;
- template previews/screenshots;
- `ShowStep()` HTML inside step classes.

Common legacy steps:

- site selection;
- template selection;
- theme selection;
- site settings;
- data install;
- finish.

Legacy site settings can write many visual/content options:

- colors;
- logo;
- header/footer backgrounds;
- organization text;
- address/phone/email;
- map coordinates;
- social widget settings;
- copyright.

Specialist rule: legacy preview assets are for Bitrix `wizard_sol` UI, while universal master visuals are controlled by `.wizard.config.php` and SF4 wizard templates.

## Visual QA Checklist

- Background image exists after installer assembly.
- Logo exists and renders in the master template.
- Text contrast is acceptable for dark/light theme modifiers.
- Buttons are visible in `NEW`, `WORK`, `SUCCESS`, `ERROR` states.
- Long action progress text updates and final navigation is enabled.
- Localized action names exist for current `LANGUAGE_ID`.
- Legacy wrapper preview assets are present if the wizard must appear polished in Bitrix wizard list.
- No visual-only change modifies action logic or data keys.
