<?
\Bitrix\Main\Loader::includeSharewareModule("simai.framework");

use Bitrix\Main\Localization\Loc;
use SIMAI\Wizard;

Loc::loadMessages(__FILE__);

return array(
    "description" => array(
        "name" => Loc::getMessage("WIZARD_SOLUTION"),
        "code" => "simai_example",
        "stage_renew" => "Y",
        "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
        "author" => "SIMAI",
        "copyright" => "© SIMAI",
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
    ),
    "action" => array(
        array(
            "name" => Loc::getMessage("SITE_CHOICE"),
            "code" => "site.choice.sveden",
            "data_output_code" => "site_config",
            "parameter" => array(),
        ),

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
        ),

        array(
            "name" => Loc::getMessage("ADD_URLREWRITE"),
            "code" => "urlrewrite.add",
            "autocomplete" => "Y",
            "data_input_code" => "site_config",
            "parameter" => array(
                "source" => Wizard::getLocal(__DIR__) . "/data/config/urlrewrite.php",
            ),
        ),

        array(
            "name" => Loc::getMessage("FINISH"),
            "code" => "info",
            "autocomplete" => "Y",
            "parameter" => array(
                "message" => Loc::getMessage("FINISH_MESSAGE"),
            ),
        )
    ),
);
