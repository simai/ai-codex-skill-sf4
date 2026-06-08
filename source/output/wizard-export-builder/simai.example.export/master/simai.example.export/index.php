<?php
require($_SERVER["DOCUMENT_ROOT"] . "/bitrix/modules/main/include/prolog_before.php");

\Bitrix\Main\Loader::includeSharewareModule("simai.framework");

use SIMAI\Wizard;

$dirWizard = Wizard::getLocal(__DIR__);

$APPLICATION->IncludeComponent(
    "simai:sf.wizard",
    ".default",
    array(
        "COMPONENT_TEMPLATE" => ".default",
        "WIZARD_DIR" => $dirWizard,
        "WIZARD_TEMP_DIR" => $dirWizard . "/temp",
        "WIZARD_CONFIG_FILE" => $dirWizard . "/.wizard.config.php",
        "AJAX_TIME_STEP" => 5,
        "AJAX_TIME_INTERVAL" => 2,
        "AJAX_MODE" => "Y",
        "AJAX_OPTION_JUMP" => "N",
        "AJAX_OPTION_STYLE" => "N",
        "AJAX_OPTION_HISTORY" => "N",
        "AJAX_OPTION_ADDITIONAL" => "",
        "COMPOSITE_FRAME_MODE" => "N",
        "COMPOSITE_FRAME_TYPE" => "AUTO",
        "CACHE_TYPE" => "N",
    ),
    false
);
