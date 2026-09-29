#!/usr/bin/env bash
# WP-CLI wrapper for this Local site (Local's PHP + site php.ini, DB port 10053).
# Git Bash rewrites any argument that looks like a POSIX path ("/%postname%/", "/products/") into a Windows path before a native
# .exe sees it: that silently stored "/C:/Users/…/Programs/Git/%postname%/" as the permalink structure (issues-log #67).
# So: convert our own paths ONCE with cygpath, then switch the conversion off for WP-CLI's arguments.
export PATH="/c/Users/Vansh Patel/AppData/Roaming/Local/lightning-services/mysql-8.4.0+2/bin/win64/bin:$PATH"
export MYSQL_HOST=127.0.0.1 MYSQL_TCP_PORT=10053
PHP="/c/Users/Vansh Patel/AppData/Roaming/Local/lightning-services/php-8.2.29+0/bin/win64/php.exe"
INI="$(cygpath -w "/c/Users/Vansh Patel/AppData/Roaming/Local/run/PXH8o8TpS/conf/php/php.ini")"
WPCLI="$(cygpath -w "/c/Users/Vansh Patel/AppData/Local/Programs/Local/resources/extraResources/bin/wp-cli/wp-cli.phar")"
cd "$(dirname "$0")/.." && MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" "$PHP" -c "$INI" -d display_startup_errors=0 -d error_reporting=0 "$WPCLI" "$@"
