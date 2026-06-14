#!/usr/bin/env python3
"""
Propose-only generator for SF4 universal wizard master skeletons.

The generator writes candidate files into source/output by default. It is
deliberately not a live installer: it does not touch /Users/rim/Sites, /simai,
/bitrix, public site roots, Bitrix DB or wizard runtime state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List


SCHEMA_VERSION = "1.0.0"
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000a49444154789c6360000002000100ffff0300000600"
    "057bfabf0000000049454e44ae426082"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slug_code(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ValueError("code must contain only letters, digits, dot, underscore or hyphen")
    return value


def php_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ensure_safe_output(path: Path, root: Path) -> Path:
    resolved = path.expanduser().resolve()
    allowed = (root / "source" / "output").resolve()
    if allowed not in [resolved, *resolved.parents]:
        raise ValueError(f"output_dir must be inside {allowed}")
    return resolved


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def mkdirs(paths: List[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def build_actions(profile: str, name: str) -> str:
    actions: List[str] = [
        """
        array(
            "name" => Loc::getMessage("SITE_CHOICE"),
            "code" => "site.choice.sveden",
            "data_output_code" => "site_config",
            "parameter" => array(),
        )""".strip()
    ]

    if profile in {"config", "iblock"}:
        actions.extend(
            [
                """
        array(
            "name" => Loc::getMessage("CREATE_IBLOCKCONFIG"),
            "code" => "iblockconfig.import.data",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "site" => array(
                    "array" => "site_config",
                    "key" => "site",
                ),
                "file" => array(
                    "iblock" => array(
                        "config" => Wizard::getLocal(__DIR__) . "/data/config/.iblock.config.php",
                        "lang" => Wizard::getLocal(__DIR__) . "/data/config/lang/ru/.iblock.config.php",
                    ),
                    "iblocksection" => array(
                        "config" => Wizard::getLocal(__DIR__) . "/data/config/.iblock.section.config.php",
                        "lang" => Wizard::getLocal(__DIR__) . "/data/config/lang/ru/.iblock.section.config.php",
                    ),
                    "tmp" => Wizard::getLocal(__DIR__) . "/tmp/",
                ),
            ),
        )""".strip(),
                """
        array(
            "name" => Loc::getMessage("ADD_URLREWRITE"),
            "code" => "urlrewrite.add",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "source" => Wizard::getLocal(__DIR__) . "/data/config/urlrewrite.php",
            ),
        )""".strip(),
            ]
        )

    if profile == "iblock":
        actions.extend(
            [
                """
        array(
            "name" => Loc::getMessage("CREATE_IBLOCK_TYPE"),
            "code" => "iblocktype.import.data",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "source" => Wizard::getLocal(__DIR__) . "/data/config/.iblocktype.config.php",
            ),
        )""".strip(),
                """
        array(
            "name" => Loc::getMessage("IMPORT_IBLOCK_ARCHIVE"),
            "code" => "iblock.import.archive",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                array(
                    "source" => Wizard::getLocal(__DIR__) . "/data/iblock/sample.zip",
                    "destination" => "sf_ru_map_data",
                    "site" => array(
                        "array" => "site_config",
                        "key" => "site",
                    ),
                    "name" => """ + php_string(name + " sample archive") + """,
                ),
            ),
        )""".strip(),
            ]
        )

    actions.append(
        """
        array(
            "name" => Loc::getMessage("FINISH"),
            "code" => "info",
            "autocomplete" => "Y",
            "parameter" => array(
                "text" => Loc::getMessage("FINISH_MESSAGE"),
            ),
        )""".strip()
    )
    return ",\n\n        ".join(actions)


def render_config(code: str, storage_code: str, name: str, profile: str) -> str:
    actions = build_actions(profile, name)
    return f"""<?
\\Bitrix\\Main\\Loader::includeSharewareModule("simai.framework");

use Bitrix\\Main\\Localization\\Loc;
use SIMAI\\Wizard;

Loc::loadMessages(__FILE__);

return array(
    "description" => array(
        "name" => Loc::getMessage("WIZARD_SOLUTION"),
        "code" => "{storage_code}",
        "stage_renew" => "Y",
        "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
        "author" => "SIMAI",
        "copyright" => "© <a href=\\"https://simai.ru\\" target=\\"_blank\\" rel=\\"noopener\\">SIMAI</a>, 2026",
        "background" => array(
            "color" => "#f4f7fb",
            "image" => Wizard::getLocal(__DIR__) . "/image/wizard_bg.jpg",
            "position" => "center",
            "repeat" => "no-repeat",
            "size" => "cover",
            "attachment" => "fixed",
        ),
        "color" => array(
            "primary" => "#B4232E",
            "secondary" => "#134A5B",
        ),
        "modifier" => array(
            "page_body" => "theme-dark bg-theme-50 p-md-5 py-4 py-lg-6",
            "wizard_wrap" => "r-2 w-80 wr-md-7 mx-auto",
            "wizard_area" => "p-4 bg-white theme-light",
            "wizard_nav" => "p-4 bg-white",
            "wizard_copyright" => "p-2 t-center t--1 c-text-secondary l-inherit l-underline",
        ),
    ),
    "action" => array(
        {actions}
    ),
);
"""


def render_index() -> str:
    return """<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {
    require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/header.php");
}

define("WIZARD_DIR", __DIR__);
define("WIZARD_TEMP_DIR", __DIR__ . "/tmp");
define("WIZARD_CONFIG_FILE", __DIR__ . "/.wizard.config.php");

$APPLICATION->IncludeComponent(
    "simai:sf.wizard",
    "",
    array(
        "WIZARD_DIR" => WIZARD_DIR,
        "WIZARD_TEMP_DIR" => WIZARD_TEMP_DIR,
        "WIZARD_CONFIG_FILE" => WIZARD_CONFIG_FILE,
        "AJAX_TIME_STEP" => 5,
        "AJAX_TIME_INTERVAL" => 500,
        "AJAX_MODE" => "Y",
        "CACHE_TYPE" => "N",
    )
);

require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/footer.php");
"""


def render_wizard_template() -> str:
    return """<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED!==true)die();

use Bitrix\\Main\\Localization\\Loc;
use SIMAI\\Main\\Page\\Asset;

Loc::loadMessages(__FILE__);

Asset::getInstance()->load("jquery");
Asset::getInstance()->load("simai-framework");

$isWizardFinished = (
    isset($arResult["STAGE"]["CURRENT"], $arResult["STAGE"]["COUNT"])
    && $arResult["STAGE"]["COUNT"] > 0
    && $arResult["STAGE"]["CURRENT"] >= $arResult["STAGE"]["COUNT"]
);
$stageCount = (int)$arResult["STAGE"]["COUNT"];
$stageCurrent = (int)$arResult["STAGE"]["CURRENT"];
$progressWidth = $stageCount > 0 ? min(100, (($stageCurrent + 1) / $stageCount * 100)) : 0;
$siteDir = "/";

if (is_array($arResult["DATA"]["site_config"]) && $arResult["DATA"]["site_config"]["dir"] !== "")
{
    $siteDir = $arResult["DATA"]["site_config"]["dir"];
}

$siteDir = "/" . trim($siteDir, "/") . "/";
if ($siteDir == "//")
{
    $siteDir = "/";
}

$finishUrl = $siteDir;
?>
<html>
    <head>
        <?$APPLICATION->ShowHead();?>
        <?require "style.php";?>
    </head>
    <body
        style="
            background-color: <?=$arResult["WIZARD"]["BACKGROUND"]["COLOR"]?>;
            background-image: url('<?=$arResult["WIZARD"]["BACKGROUND"]["IMAGE"]?>');
            background-position: <?=$arResult["WIZARD"]["BACKGROUND"]["POSITION"]?>;
            background-repeat: <?=$arResult["WIZARD"]["BACKGROUND"]["REPEAT"]?>;
            background-size: <?=$arResult["WIZARD"]["BACKGROUND"]["SIZE"]?>;
            background-attachment: <?=$arResult["WIZARD"]["BACKGROUND"]["ATTACHMENT"]?>;
        "
        class="<?=$arResult["WIZARD"]["MODIFIER"]["PAGE_BODY"];?>">
        <div class="sf-wizard-wrap <?=$arResult["WIZARD"]["MODIFIER"]["WIZARD_WRAP"];?>">
            <div class="sf-progress">
                <div class="sf-progress-bar" style="width: <?=$progressWidth;?>%"></div>
            </div>

            <div class="sf-wizard-area <?=$arResult["WIZARD"]["MODIFIER"]["WIZARD_AREA"];?>">
                <div id="sf-wizard-stage-area">
                    <div class="sf-wizard-heading">
                        <?if($arResult["WIZARD"]["LOGO"]):?>
                            <div class="sf-wizard-logo">
                                <img src="<?=htmlspecialcharsbx($arResult["WIZARD"]["LOGO"]);?>" alt="<?=htmlspecialcharsbx($arResult["WIZARD"]["NAME"]);?>">
                            </div>
                        <?endif;?>
                        <div class="sf-wizard-heading-content">
                            <h1 class="sf-title"><?=$arResult["WIZARD"]["NAME"];?></h1>
                            <p class="t-1 c-text-secondary"><?=$isWizardFinished ? Loc::getMessage("WIZARD_FINISH_SUBTITLE") : $arResult["ACTION"]["NAME"];?></p>
                        </div>
                    </div>

                    <div id="sf-wizard-action-area">
                        <?if($isWizardFinished):?>
                            <div class="sf-wizard-finish">
                                <div class="sf-wizard-finish-icon">
                                    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                                        <path d="M20 6L9 17l-5-5"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h2><?=Loc::getMessage("WIZARD_FINISH_TITLE");?></h2>
                                    <p><?=Loc::getMessage("WIZARD_FINISH_TEXT");?></p>
                                </div>
                            </div>
                        <?else:?>
                            <?
                            $APPLICATION->IncludeComponent(
                                "simai:sf.wizard.stage",
                                ".default",
                                array(
                                    "COMPONENT_TEMPLATE" => ".default",
                                    "WIZARD_CODE" => $arResult["WIZARD"]["CODE"],
                                    "AJAX_MODE" => "Y",
                                    "AJAX_OPTION_JUMP" => "N",
                                    "AJAX_OPTION_STYLE" => "N",
                                    "AJAX_OPTION_HISTORY" => "N",
                                    "AJAX_OPTION_ADDITIONAL" => "",
                                    "PARENT_AJAX_ID" => $arParams["AJAX_ID"],
                                    "AJAX_ID" => $arResult["STAGE"]["AJAX_ID"],
                                    "CACHE_TYPE" => "N",
                                ),
                                false
                            );
                            ?>
                        <?endif;?>
                    </div>
                </div>
            </div>

            <div class="sf-wizard-nav <?=$arResult["WIZARD"]["MODIFIER"]["WIZARD_NAV"];?>">
                <div class="row mb-0 mt-4">
                    <div class="col-6 t-left">
                        <?if(!$isWizardFinished && isset($arResult["STAGE"]["PREV"]) && $arResult["STAGE"]["CURRENT"]>0):?>
                            <form action="<?=POST_FORM_ACTION_URI?>" method="post" enctype="multipart/form-data" class="m-0">
                                <input type="hidden" name="stage" value="<?=$arResult["STAGE"]["PREV"]?>">
                                <button type="submit" id="sf-wizard-stage-prev" class="btn btn-primary" <?=($arResult["STAGE"]["STATUS"] != "SUCCESS" || $arResult["ACTION"]["GO_BACK"] == "N" ? "disabled" : "")?>><?=Loc::getMessage("WIZARD_STAGE_PREV");?></button>
                            </form>
                        <?endif;?>
                    </div>
                    <div class="col-6 t-right">
                        <?if($isWizardFinished):?>
                            <a class="btn btn-primary" href="<?=htmlspecialcharsbx($finishUrl);?>"><?=Loc::getMessage("WIZARD_FINISH_OPEN");?></a>
                        <?elseif(isset($arResult["STAGE"]["NEXT"]) && $arResult["STAGE"]["CURRENT"] < $arResult["STAGE"]["COUNT"]):?>
                            <form action="<?=POST_FORM_ACTION_URI?>" method="post" enctype="multipart/form-data" class="m-0">
                                <input type="hidden" name="stage" value="<?=$arResult["STAGE"]["NEXT"]?>">
                                <button type="submit" id="sf-wizard-stage-next" class="btn btn-primary" <?=($arResult["STAGE"]["STATUS"] != "SUCCESS" ? "disabled" : "")?>><?=Loc::getMessage("WIZARD_STAGE_NEXT");?></button>
                            </form>
                        <?endif;?>
                    </div>
                </div>
            </div>

            <div class="sf-wizard-copyright <?=$arResult["WIZARD"]["MODIFIER"]["WIZARD_COPYRIGHT"];?>">
                <?=$arResult["WIZARD"]["COPYRIGHT"];?>
            </div>
        </div>

        <script language="JavaScript" type="text/javascript">
          <?if (
            $GLOBALS['AUTOCOMPLETE_SF_WIZARD_STEP'] == 'y'
            || (
                $arResult["ACTION"]["AUTOCOMPLETE"] == "Y"
                && $arResult["STAGE"]["STATUS"] == "SUCCESS"
                && isset($arResult["STAGE"]["NEXT"])
                && $arResult["STAGE"]["CURRENT"] < $arResult["STAGE"]["COUNT"]
            )
          ):?>
            BX.ready(function(){
                window.setTimeout(function(){
                    var nextButton = BX('sf-wizard-stage-next');
                    if (nextButton && !nextButton.disabled) {
                        BX.fireEvent(nextButton, 'click');
                    }
                }, 300);
            });
          <?endif?>
        </script>
    </body>
</html>
"""


def render_wizard_style() -> str:
    return """<?
if(!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED!==true)die();

\\Bitrix\\Main\\Loader::includeSharewareModule('simai.framework');

use \\SIMAI\\Wizard;

define("BTN_BORDER", 5);
define("BTN_BORDER_ACTIVE", 12);
define("BTN_BACKGROUND", 10);

if($arResult["WIZARD"]["COLOR"]["PRIMARY"])
    $colorPrimary = $arResult["WIZARD"]["COLOR"]["PRIMARY"];
else
    $colorPrimary = "#B4232E";

if($arResult["WIZARD"]["COLOR"]["SECONDARY"])
    $colorSecondary = $arResult["WIZARD"]["COLOR"]["SECONDARY"];
else
    $colorSecondary = "#134A5B";
?>
<style>
div[id^="wait_"]{display:none!important}

:root {
    --sf-wizard-primary: <?=$colorPrimary?>;
    --sf-wizard-primary-dark: <?=Wizard::darker($colorPrimary, 14)?>;
    --sf-wizard-secondary: <?=$colorSecondary?>;
    --sf-wizard-surface: #ffffff;
    --sf-wizard-text: #17212b;
    --sf-wizard-muted: #667085;
    --sf-wizard-border: #d8dee8;
    --sf-wizard-shadow: 0 24px 70px rgba(15, 23, 42, 0.18);
}

html {
    min-height: 100%;
    background: #f4f7fb;
}

body {
    position: relative;
    min-height: 100vh;
    margin: 0;
    padding: 48px 20px 32px!important;
    box-sizing: border-box;
    color: var(--sf-wizard-text);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    letter-spacing: 0;
}

body *,
body *::before,
body *::after {
    box-sizing: border-box;
}

.sf-wizard-wrap {
    position: relative!important;
    display: block!important;
    width: min(1720px, calc(100vw - 160px))!important;
    max-width: none!important;
    margin: 0 auto!important;
    padding: 0!important;
    border-radius: 18px!important;
    overflow: hidden!important;
    box-shadow: var(--sf-wizard-shadow);
}

.sf-progress {
    height: 8px;
    background: #e9edf3;
    overflow: hidden;
}

.sf-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--sf-wizard-primary), var(--sf-wizard-primary-dark));
    transition: width 0.25s ease;
}

.sf-wizard-area,
.sf-wizard-nav,
.sf-wizard-copyright {
    position: static!important;
    display: block!important;
    float: none!important;
    clear: none!important;
    width: 100%!important;
    max-width: none!important;
    margin: 0!important;
    border-radius: 0!important;
    box-shadow: none!important;
    background: var(--sf-wizard-surface)!important;
    color: var(--sf-wizard-text);
}

.sf-wizard-area {
    min-height: clamp(360px, 46vh, 680px);
    padding: 44px 48px 28px!important;
}

.sf-wizard-heading {
    display: flex;
    align-items: flex-start;
    gap: 22px;
    margin-bottom: 30px;
}

.sf-wizard-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 82px;
    width: 82px;
    height: 82px;
    border: 1px solid var(--sf-wizard-border);
    border-radius: 14px;
    background: #fff;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
    overflow: hidden;
}

.sf-wizard-logo img {
    display: block;
    max-width: 66px;
    max-height: 66px;
    width: auto;
    height: auto;
}

.sf-title {
    max-width: 980px;
    margin: 0 0 10px;
    color: var(--sf-wizard-text);
    font-size: 34px;
    font-weight: 700;
    line-height: 1.18;
    letter-spacing: 0;
}

.sf-title + p {
    margin: 0;
    color: var(--sf-wizard-muted)!important;
    font-size: 18px;
    font-weight: 600;
}

.sf-wizard-finish {
    display: flex;
    align-items: flex-start;
    gap: 18px;
    max-width: 760px;
    margin: 24px auto 0;
    padding: 24px;
    border: 1px solid rgba(19, 74, 91, 0.14);
    border-radius: 12px;
    background: #f8fafc;
    box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
}

.sf-wizard-finish-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 48px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(180, 35, 46, 0.1);
    color: var(--sf-wizard-primary);
}

.sf-wizard-finish-icon svg {
    display: block;
    width: 24px;
    height: 24px;
    fill: none;
    stroke: currentColor;
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.sf-wizard-finish h2 {
    margin: 0 0 8px;
    color: var(--sf-wizard-text);
    font-size: 24px;
    line-height: 1.25;
}

.sf-wizard-finish p {
    margin: 0;
    color: var(--sf-wizard-muted);
}

.row {display:flex;flex-wrap:wrap;align-items:center;margin-right:-8px;margin-left:-8px}
.col-6 {flex:0 0 50%;max-width:50%;padding-right:8px;padding-left:8px}
.t-left {text-align:left}
.t-right {text-align:right}
.m-0 {margin:0!important}
.mb-0 {margin-bottom:0!important}
.mt-4 {margin-top:0!important}

.sf-wizard-nav {
    padding: 24px 48px!important;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 132px;
    min-height: 44px;
    padding: 10px 22px;
    border: 1px solid transparent;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 700;
    line-height: 1.2;
    text-decoration: none;
    cursor: pointer;
    transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, color 0.18s ease;
}

.btn-primary {
    color: #fff!important;
    background-color: <?=$colorPrimary?>!important;
    border-color: <?=Wizard::darker($colorPrimary, BTN_BORDER)?>!important;
    box-shadow: 0 10px 22px rgba(180, 35, 46, 0.22);
}

.btn-primary:hover,
.btn-primary:active,
.btn-primary:focus {
    color: #fff!important;
    background-color: <?=Wizard::darker($colorPrimary, BTN_BACKGROUND)?>!important;
    border-color: <?=Wizard::darker($colorPrimary, BTN_BORDER_ACTIVE)?>!important;
}

.btn-primary.disabled,
.btn-primary:disabled {
    color: #8a3440!important;
    background: #f7c8c4!important;
    border-color: #f0b6b0!important;
    box-shadow: none;
    cursor: not-allowed;
    opacity: 1;
}

.sf-wizard-copyright {
    padding: 18px 48px 24px!important;
    color: var(--sf-wizard-muted)!important;
    font-size: 14px;
    text-align: center;
}

.sf-wizard-copyright a {
    color: var(--sf-wizard-secondary)!important;
    font-weight: 700;
    text-decoration: none;
}

.sf-wizard-copyright a:hover {
    text-decoration: underline;
}

@media (max-width: 640px) {
    body {padding:18px 12px!important}
    .sf-wizard-wrap {width:100%!important;border-radius:12px!important}
    .sf-wizard-area {min-height:300px;padding:28px 22px 18px!important}
    .sf-wizard-heading {display:block;margin-bottom:22px}
    .sf-wizard-logo {width:64px;height:64px;margin-bottom:16px;border-radius:12px}
    .sf-wizard-logo img {max-width:50px;max-height:50px}
    .sf-title {font-size:26px}
    .sf-title + p {font-size:16px}
    .sf-wizard-nav {padding:18px 22px!important}
    .sf-wizard-finish {display:block;margin-top:18px;padding:20px}
    .sf-wizard-finish-icon {margin-bottom:14px}
    .col-6 {flex-basis:100%;max-width:100%}
    .col-6 + .col-6 {margin-top:12px}
    .t-left,.t-right {text-align:left}
    .btn {width:100%}
    .sf-wizard-copyright {padding:14px 22px 18px!important}
}
</style>
"""


def render_wizard_template_lang() -> str:
    return """<?php
$MESS["WIZARD_STAGE_PREV"] = "Назад";
$MESS["WIZARD_STAGE_NEXT"] = "Далее";
$MESS["WIZARD_FINISH_SUBTITLE"] = "Установка завершена";
$MESS["WIZARD_FINISH_TITLE"] = "Решение установлено";
$MESS["WIZARD_FINISH_TEXT"] = "Раздел готов к проверке на сайте.";
$MESS["WIZARD_FINISH_OPEN"] = "Перейти в раздел";
"""


def render_lang(name: str) -> str:
    return f"""<?
$MESS["WIZARD_SOLUTION"] = {php_string(name)};
$MESS["SITE_CHOICE"] = "Выбор сайта";
$MESS["CREATE_IBLOCKCONFIG"] = "Подготовка конфигурации инфоблоков";
$MESS["ADD_URLREWRITE"] = "Подготовка правил URL";
$MESS["CREATE_IBLOCK_TYPE"] = "Подготовка типов инфоблоков";
$MESS["IMPORT_IBLOCK_ARCHIVE"] = "Подготовка архива инфоблока";
$MESS["FINISH"] = "Завершение";
$MESS["FINISH_MESSAGE"] = "Skeleton мастера подготовлен. Перед live запуском требуется аудит, backup и rollback.";
"""


def render_wrapper_wizard(code: str) -> str:
    return f"""<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {{
    die();
}}

class SelectSiteStep extends CWizardStep
{{
    public function InitStep()
    {{
        $wizard =& $this->GetWizard();
        $wizard->solutionName = "{code}";
        LocalRedirect("/simai/wizard/master/{code}/");
    }}
}}
"""


def render_wrapper_description(code: str, name: str) -> str:
    return f"""<?
if (!defined("B_PROLOG_INCLUDED") || B_PROLOG_INCLUDED !== true) {{
    die();
}}

$arWizardDescription = array(
    "NAME" => {php_string(name)},
    "DESCRIPTION" => "SF4 universal wizard wrapper for {code}",
    "VERSION" => "1.0.0",
    "START_TYPE" => "WINDOW",
    "WIZARD_TYPE" => "INSTALL",
);
"""


def create_sample_zip(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("sample.xml", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><items></items>")


def generate(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root()
    code = slug_code(args.code)
    storage_code = args.storage_code or code.replace(".", "_").replace("-", "_")
    name = args.name or code
    output_root = ensure_safe_output(Path(args.output_dir), root)
    package_root = output_root / code
    master = package_root / "master" / code

    if package_root.exists() and not args.force:
        raise FileExistsError(f"{package_root} already exists; pass --force to replace files in this proposal")

    mkdirs(
        [
            master / "image",
            master / "tmp",
            master
            / "data"
            / "bitrix"
            / "components"
            / "simai"
            / "sf.wizard"
            / "templates"
            / ".default"
            / "lang"
            / "ru",
            master / "data" / "bitrix" / "templates",
            master / "data" / "config" / "lang" / "ru",
            master / "data" / "iblock",
            master / "data" / "module",
            master / "data" / "php_interface",
            master / "data" / "root",
            master / "data" / "site",
            master / "data" / "template",
            master / "data" / "components",
            master / "lang" / "ru",
        ]
    )

    write_text(master / "index.php", render_index())
    write_text(master / ".wizard.config.php", render_config(code, storage_code, name, args.profile))
    write_text(master / "lang" / "ru" / ".wizard.config.php", render_lang(name))
    wizard_template = master / "data" / "bitrix" / "components" / "simai" / "sf.wizard" / "templates" / ".default"
    write_text(wizard_template / "template.php", render_wizard_template())
    write_text(wizard_template / "style.php", render_wizard_style())
    write_text(wizard_template / "lang" / "ru" / "template.php", render_wizard_template_lang())
    write_text(master / "data" / "config" / ".iblock.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / ".iblock.section.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / ".iblocktype.config.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / "urlrewrite.php", "<?\nreturn array();\n")
    write_text(master / "data" / "config" / "lang" / "ru" / ".iblock.config.php", "<?\n$MESS = array();\n")
    write_text(master / "data" / "config" / "lang" / "ru" / ".iblock.section.config.php", "<?\n$MESS = array();\n")
    write_bytes(master / "image" / "logo.png", PNG_1X1)
    write_bytes(master / "image" / "wizard_bg.jpg", PNG_1X1)
    if args.profile == "iblock":
        create_sample_zip(master / "data" / "iblock" / "sample.zip")

    wrapper_root = None
    if args.wrapper:
        wrapper_root = package_root / "module" / "install" / "wizard" / code
        mkdirs([wrapper_root / "lang" / "ru", wrapper_root / "images"])
        write_text(wrapper_root / "wizard.php", render_wrapper_wizard(code))
        write_text(wrapper_root / ".description.php", render_wrapper_description(code, name))
        write_text(wrapper_root / "lang" / "ru" / ".description.php", render_lang(name))
        write_text(wrapper_root / "lang" / "ru" / "wizard.php", render_lang(name))
        write_bytes(wrapper_root / "images" / "wizard.png", PNG_1X1)

    readme = f"""# {name}

Generated SF4 universal wizard skeleton proposal.

This package is not installed and not executable in live/runtime by itself.
Review `.wizard.config.php`, fill real payload data, define backup/rollback and
run `sf4_wizard_audit.py` before any controlled environment execution.

Master proposal:

```text
{master}
```
"""
    write_text(package_root / "README.md", readme)

    manifest: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": "sf4.wizard.skeleton",
        "mode": {
            "propose_only": True,
            "read_only_runtime": True,
            "writes": "source_output_only",
            "executes_php": False,
            "executes_wizard_actions": False,
        },
        "code": code,
        "storage_code": storage_code,
        "name": name,
        "profile": args.profile,
        "package_root": str(package_root),
        "master": str(master),
        "config": str(master / ".wizard.config.php"),
        "wrapper": str(wrapper_root) if wrapper_root else None,
        "visual_standard": {
            "primary": "#B4232E",
            "copyright": "© SIMAI, 2026",
            "wizard_template": str(wizard_template),
            "finish_icon": "inline_svg",
            "terminal_info_rule": "explicit_text_or_standard_finish",
        },
        "audit_hint": {
            "command": [
                "python3",
                "scripts/sf4_wizard_audit.py",
                "--site-root",
                args.audit_site_root,
                "--master",
                str(master),
                "--json",
                f"source/output/wizard-skeleton/{code}/audit.json",
            ]
        },
        "next_required_human_work": [
            "replace placeholder visual assets",
            "fill real config/data payloads",
            "choose exact action chain and branch conditions",
            "define backup/rollback per side effect",
            "audit in controlled environment before execution",
        ],
    }
    write_text(package_root / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest


def main() -> int:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Generate a propose-only SF4 universal wizard skeleton.")
    parser.add_argument("--code", required=True, help="Wizard/module code, for example simai.example")
    parser.add_argument("--name", help="Human-readable wizard name")
    parser.add_argument("--storage-code", help="description.code storage key. Defaults to code with dots/hyphens as underscores.")
    parser.add_argument(
        "--profile",
        choices=["minimal", "config", "iblock"],
        default="config",
        help="Generated action-chain profile.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(root / "source" / "output" / "wizard-skeleton"),
        help="Output directory. Must be inside source/output.",
    )
    parser.add_argument("--audit-site-root", default="/Users/rim/Sites/sf4.test", help="Read-only action library site root for audit hints.")
    parser.add_argument("--wrapper", action="store_true", help="Also generate Bitrix wrapper wizard skeleton.")
    parser.add_argument("--force", action="store_true", help="Allow overwriting files in an existing proposal directory.")
    parser.add_argument("--json", dest="json_only", action="store_true", help="Print machine-readable manifest only.")
    args = parser.parse_args()

    try:
        manifest = generate(args)
    except Exception as exc:  # noqa: BLE001 - CLI should report exact failure.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_only:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("SF4 Wizard Skeleton")
        print(f"Package: {manifest['package_root']}")
        print(f"Master: {manifest['master']}")
        print(f"Config: {manifest['config']}")
        print("Mode: propose-only, source/output writes only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
