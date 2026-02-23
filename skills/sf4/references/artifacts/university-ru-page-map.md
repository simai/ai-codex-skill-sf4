# Page Map Snapshot: `/ru`

Generated from:

```bash
python3 scripts/sf4_site_map.py --site-root <project_root> --site-dir /ru --json-out references/artifacts/university-ru-site-map.json --json
```

## Active `grid_view_*`

- `grid_view_header=005`
- `grid_view_footer=default`
- `grid_view_home=default`
- `grid_view_main_top=default`
- `grid_view_main_bottom=default`
- `grid_view_sidebar_left=default`
- `grid_view_sidebar_right=default`

## Active View Templates And Key Blocks

- header: `ru/simai.data/grid/view/header/005/template.php`
  - key blocks (18): `banner.single`, `menu.header`, `menu.main`, `org.logo`, `org.name`, `org.address`, `org.phone`, `org.email`, `org.social`, `search`, `display.special`, `user.auth`, `translate.google`, `nav.breadcrumb`, `social.share`, `page.title`, `custom.text`, `custom.include.file`
- footer: `ru/simai.data/grid/view/footer/default/template.php`
  - key blocks (14): `org.contact`, `menu.footer`, `org.social`, `org.copyright`, `org.address`, `org.phone`, `org.email`, `feedback.error`, `other.composite`, `simai.solution`, `informer.sputnik`, `banner.single`, `custom.text`, `custom.include.file`
- home: `ru/simai.data/grid/view/home/default/template.php`
  - key blocks (27): `banner.main`, `banner.slider`, `banner.slider.multi`, `banner.list`, `activity`, `chief`, `news.slider`, `news.card`, `announce.card`, `announce.list`, `event.card`, `event.calendar`, `photo.list`, `video`, `video.card`, `social`, `weather`, `welcome`, `nav.link.icon`, `milestone.counter`, `branch.card`, `org.map`, `org.contact`, `org.chief`, `shedule`, `custom.section.title`, `custom.include.file`
- main/top: `ru/simai.data/grid/view/main/top/default/template.php`
  - key blocks (4): `page.title`, `banner.single`, `include.top.section`, `include.top.file`
- main/bottom: `ru/simai.data/grid/view/main/bottom/default/template.php`
  - key blocks (10): `doc.list`, `relation.doc`, `relation.photo`, `relation.video`, `relation.news`, `relation.event`, `relation.announce`, `banner.single`, `include.bottom.file`, `include.bottom.section`
- sidebar/left: `ru/simai.data/grid/view/sidebar/left/default/template.php`
  - key blocks (4): `menu.sidebar`, `banner.list`, `include.left.section`, `include.left.file`
- sidebar/right: `ru/simai.data/grid/view/sidebar/right/default/template.php`
  - key blocks (4): `menu.sidebar`, `banner.list`, `include.left.section`, `include.left.file`

## Top-Level `index.php` Component Signals

`simai:sf.*` counters:

- `simai:sf.iblock.list`: 27
- `simai:sf.iblock.section`: 2
- `simai:sf.feedback`: 1
- `simai:sf.feedback.vote`: 1
- `simai:sf.iblock.table`: 1

`bitrix:*` counters:

- `bitrix:main.include`: 7
- `bitrix:news`: 2
- `bitrix:map.yandex.view`: 1
- `bitrix:learning.course.list`: 1
- `bitrix:main.profile`: 1
- `bitrix:catalog`: 1
- `bitrix:search.page`: 1

## `.property.php` Override Hotspots

- `ru/.property.php`: `sidebar_show=none`, `show_title=N`, `show_breadcrumb=N`
- `ru/404/.property.php`: all main `grid_view_*` switched to `empty`, `sidebar_show=none`
- `ru/auth/.property.php`: all main `grid_view_*` switched to `empty`, `sidebar_show=none`
- `ru/students/service/.property.php`: `sidebar_show=none`, `show_title=N`, `show_breadcrumb=N`
- `ru/abitur/.property.php`: `sidebar_show=none`
- `ru/tenders/.property.php`: `show_title=N`
- `ru/personal/learn/courses/.property.php`: `sidebar_show=left`
- `ru/press-center/presentation/.property.php`: `show_title=Y`
- `ru/press-center/video/add/.property.php`: `show_title=Y`, `show_breadcrumb=Y`

## Direct `simai:sf.grid` Pages Outside `simai.data`

- `ru/students/service/detail.php`
