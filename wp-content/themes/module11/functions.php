<?php
/**
 * Module 11 theme bootstrap.
 *
 * All functions are prefixed m11_. Each concern lives in its own file under inc/.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

define( 'M11_VERSION', '0.1.0' );
define( 'M11_DIR', get_stylesheet_directory() );
define( 'M11_URI', get_stylesheet_directory_uri() );

require_once M11_DIR . '/inc/setup.php';
require_once M11_DIR . '/inc/enqueue.php';
require_once M11_DIR . '/inc/post-types.php';
require_once M11_DIR . '/inc/acf.php';
require_once M11_DIR . '/inc/global-settings.php';
require_once M11_DIR . '/inc/template-helpers.php';
require_once M11_DIR . '/inc/catalogue.php';
require_once M11_DIR . '/inc/sales-hub.php';
require_once M11_DIR . '/inc/elementor-tags.php';
