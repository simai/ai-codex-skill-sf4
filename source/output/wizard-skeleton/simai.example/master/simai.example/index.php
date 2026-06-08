<?
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
