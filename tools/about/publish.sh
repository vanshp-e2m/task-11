#!/usr/bin/env bash
# Rebuild About Us: theme CSS -> native tree via DevConnect set-page-data -> clear Elementor's element cache
# (set-page-data leaves _elementor_element_cache stale, so the old render keeps being served; see devconnect-conversion-issues D6).
set -e
cd "$(dirname "$0")/../.."
(cd wp-content/themes/module11 && npm run build >/dev/null 2>&1)
python tools/elementor/build_about.py --write
tools/wp.sh post meta delete 15 _elementor_element_cache >/dev/null 2>&1 || true
tools/wp.sh elementor flush-css >/dev/null
tools/wp.sh eval '$d=json_decode(get_post_meta(15,"_elementor_data",true),true); $c=0; $f=function($ns) use (&$f,&$c){foreach($ns as $n){$c++; $f($n["elements"]??[]);}}; $f($d); echo "stored nodes: $c\n";'
