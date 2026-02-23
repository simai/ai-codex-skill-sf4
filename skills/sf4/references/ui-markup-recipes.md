# SF4 Markup Recipes

## Goal

Provide compact, reusable markup skeletons aligned with SF4 class language for common block tasks.

Use together with:

- `references/ui-catalog.md`
- `references/ui-class-cheatsheet.md`

## Recipe 1: Feature Cards Grid

Use for:

- service cards, catalog teasers, value proposition blocks.

Skeleton:

```php
<div class="row g-3">
\t<?foreach ($arResult["ITEMS"] as $item):?>
\t\t<div class="col-sm-6 col-lg-4">
\t\t\t<article class="sf-example p-3 h-100 bg-white shadow">
\t\t\t\t<h3 class="sf-title t-3 mb-2"><?=htmlspecialcharsbx($item["NAME"])?></h3>
\t\t\t\t<div class="c-text-secondary">
\t\t\t\t\t<?=htmlspecialcharsBack($item["PREVIEW_TEXT"])?>
\t\t\t\t</div>
\t\t\t</article>
\t\t</div>
\t<?endforeach;?>
</div>
```

## Recipe 2: Split Hero (Text + Action)

Use for:

- top-screen promo section in home/main view.

Skeleton:

```php
<section class="theme-light p-4 p-lg-5">
\t<div class="row align-items-center">
\t\t<div class="col-lg-8">
\t\t\t<h1 class="sf-title t-1 mb-3"><?=htmlspecialcharsbx($arBlockProperty[$nameTemplate . "__TITLE"])?></h1>
\t\t\t<div class="t-4 c-text-secondary">
\t\t\t\t<?=htmlspecialcharsBack($arBlockProperty[$nameTemplate . "__TEXT"])?>
\t\t\t</div>
\t\t</div>
\t\t<div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
\t\t\t<a class="sf-link btn btn-primary" href="<?=htmlspecialcharsbx($arBlockProperty[$nameTemplate . "__LINK"])?>">
\t\t\t\t<?=htmlspecialcharsbx($arBlockProperty[$nameTemplate . "__LINK_TEXT"])?>
\t\t\t</a>
\t\t</div>
\t</div>
</section>
```

## Recipe 3: Compact Form Block

Use for:

- subscribe, lead, callback mini-form.

Skeleton:

```php
<form class="sf-form p-3 bg-gray-100" method="post">
\t<div class="mb-3">
\t\t<label class="sf-form-label t-5" for="email"><?=$arParams["LABEL_EMAIL"]?></label>
\t\t<input class="sf-form-control" id="email" name="email" type="email" required>
\t</div>
\t<div class="d-flex align-items-center justify-content-between">
\t\t<button class="btn btn-primary" type="submit"><?=$arParams["BUTTON_TEXT"]?></button>
\t\t<span class="text-muted t--2"><?=$arParams["HINT_TEXT"]?></span>
\t</div>
</form>
```

## Adaptation Rules

1. Keep structure first; bind runtime fields second.
2. Prefer existing project tokens/classes over introducing new custom modifiers.
3. If block must be editor-configurable, expose labels/links/modifiers via `.parameters.php`.
4. Keep form fields aligned with `component/form/*` examples in `/ru/ui`.
5. Validate layout on mobile and desktop after data binding.
