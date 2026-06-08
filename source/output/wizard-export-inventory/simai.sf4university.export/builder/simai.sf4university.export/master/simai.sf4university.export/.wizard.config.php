<?php
\Bitrix\Main\Loader::includeSharewareModule("simai.framework");
\Bitrix\Main\Loader::includeSharewareModule("iblock");

use SIMAI\Wizard;

return array(
    "description" => array(
        "name" => "Мастер упаковки simai.sf4university.export",
        "code" => "simai_sf4university_export",
        "stage_renew" => "Y",
        "logo" => Wizard::getLocal(__DIR__) . "/image/logo.png",
        "copyright" => "© SIMAI",
        "background" => array(
            "color" => "#263238",
            "image" => Wizard::getLocal(__DIR__) . "/image/wizard_bg.jpg",
            "position" => "bottom",
            "repeat" => "no-repeat",
            "size" => "cover",
            "attachment" => "fixed",
        ),
        "color" => array(
            "primary" => "#E53935",
            "secondary" => "#2196F3",
        ),
        "modifier" => array(
            "page_body" => "theme-light bg-theme-50 p-md-5 py-4 py-lg-6",
            "wizard_wrap" => "r-2 w-80 wr-md-7 mx-auto",
            "wizard_area" => "p-4 bg-white",
            "wizard_nav" => "p-4 bg-white",
            "wizard_copyright" => "p-2 t-center t--1 c-white l-inherit l-underline",
        ),
    ),
    "action" => array(
        array(
            "name" => "Копируем файлы решения",
            "code" => "file.copy",

            "parameter" => array(
                array(
                    "source" => "/bitrix/components/simai",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/components/simai",
                    "name" => "Копирование компонентов SIMAI",
                ),
                array(
                    "source" => "/bitrix/templates/.default",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/templates/.default",
                    "name" => "Копирование шаблона .default",
                ),
                array(
                    "source" => "/upload/medialibrary",
                    "destination" => "/.last_version/simai.sf4university.export/install/ru/root/upload/medialibrary",
                    "name" => "Копирование медиабиблиотеки",
                ),
                array(
                    "source" => "/bitrix/modules/simai.sf4university",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/modules/simai.sf4university",
                    "name" => "Копирование модуля simai.sf4university",
                ),
                array(
                    "source" => "/bitrix/modules/simai.backup",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/modules/simai.backup",
                    "name" => "Копирование модуля simai.backup",
                ),
                array(
                    "source" => "/bitrix/modules/simai.property",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/modules/simai.property",
                    "name" => "Копирование модуля simai.property",
                ),
                array(
                    "source" => "/bitrix/modules/simai.property4iblock",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/modules/simai.property4iblock",
                    "name" => "Копирование модуля simai.property4iblock",
                ),
                array(
                    "source" => "/bitrix/modules/simai.bxeditor",
                    "destination" => "/.last_version/simai.sf4university.export/install/bitrix/modules/simai.bxeditor",
                    "name" => "Копирование модуля simai.bxeditor",
                )
            ),
        ),

        array(
            "name" => "Получаем данные настроек сайтов",
            "code" => "site.export.data",

            "data_output_code" => "site",
            "parameter" => array(),
        ),

        array(
            "name" => "Получаем настройки групп пользователей",
            "code" => "usergroup.export.data",

            "data_output_code" => "usergroup",
            "parameter" => array(
                "code" => array(
                    "user_editor"
                )
            ),
        ),

        array(
            "name" => "Получаем данные типов инфоблоков",
            "code" => "iblocktype.export.data",

            "data_output_code" => "iblocktype",
            "parameter" => array(),
        ),

        array(
            "name" => "Получаем настройки модулей",
            "code" => "option.export.data",

            "data_output_code" => "option",
            "parameter" => array(
                "main" => array(
                    "email_from",
                    "site_name",
                    "auth_components_template",
                    "map_top_menu_type",
                    "map_left_menu_type"
                ),
                "fileman" => array(
                    "menutypes"
                )
            ),
        ),

        array(
            "name" => "Копируем файлы публичной части",
            "code" => "file.copy",

            "parameter" => array(
                array(
                    "source" => "/ru",
                    "destination" => "/.last_version/simai.sf4university.export/install/ru/site",
                    "name" => "Копирование публичных файлов",
                ),
                array(
                    "source" => "/urlrewrite.php",
                    "destination" => "/.last_version/simai.sf4university.export/install/ru/config/urlrewrite.php",
                    "name" => "Копирование urlrewrite",
                )
            ),
        ),

        array(
            "name" => "Запаковка инфоблоков",
            "code" => "iblock.export.archive",

            "data_output_code" => "iblock_pack",
            "parameter" => array(
                "iblock" => array(
                    "sf-ru-doc-common"
                ),
                "destination" => "/.last_version/simai.sf4university.export/install/iblock",
            ),
        ),

        array(
            "name" => "Записываем данные site в файл",
            "code" => "data.export.file",

            "data_input_code" => "site",
            "parameter" => array(
                "file" => "/.last_version/simai.sf4university.export/install/ru/config/.site.config.php",
            ),
        ),

        array(
            "name" => "Записываем данные usergroup в файл",
            "code" => "data.export.file",

            "data_input_code" => "usergroup",
            "parameter" => array(
                "file" => "/.last_version/simai.sf4university.export/install/ru/config/.usergroup.config.php",
            ),
        ),

        array(
            "name" => "Записываем данные option в файл",
            "code" => "data.export.file",

            "data_input_code" => "option",
            "parameter" => array(
                "file" => "/.last_version/simai.sf4university.export/install/ru/config/.option.config.php",
            ),
        ),

        array(
            "name" => "Записываем данные iblocktype в файл",
            "code" => "data.export.file",

            "data_input_code" => "iblocktype",
            "parameter" => array(
                "file" => "/.last_version/simai.sf4university.export/install/ru/config/.iblocktype.config.php",
            ),
        ),

        array(
            "name" => "Создаём файлы php_interface",
            "code" => "file.create",

            "parameter" => array(
                array(
                    "dir" => "/.last_version/simai.sf4university.export/install/ru/php_interface",
                    "filename" => "dbconn.add.php",
                    "text" => "define(\"SF_SOLUTION\",\"simai.sf4university.export\");",
                )
            ),
        ),

        array(
            "name" => "Меняем кодировку у языковых файлов",
            "code" => "file.encode.win1251",

            "parameter" => array(
                    "/.last_version/simai.sf4university.export/"
            ),
        ),

        array(
            "name" => "Завершение упаковки",
            "code" => "info",

            "parameter" => array(
                "text" => "Упаковка решения успешно подготовлена",
            ),
        )
    ),
);
