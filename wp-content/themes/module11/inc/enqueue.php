<?php
/**
 * Front-end assets. Cache-busted by file mtime so SCSS rebuilds show immediately.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Enqueue compiled theme CSS and JS after the parent theme.
 */
function m11_enqueue_assets() {
	$css = '/assets/css/main.css';
	$js  = '/assets/js/main.js';

	// One font request for the whole site (Elementor's own Google Fonts loading is switched off so fonts load once).
	wp_enqueue_style(
		'm11-fonts',
		'https://fonts.googleapis.com/css2?family=Freeman&family=Fraunces:opsz,wght@9..144,700&family=Montserrat:wght@300;500;700&family=Mukta:wght@700&family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,600&display=swap',
		array(),
		null
	);

	if ( file_exists( M11_DIR . $css ) ) {
		wp_enqueue_style( 'm11-main', M11_URI . $css, array( 'hello-elementor' ), filemtime( M11_DIR . $css ) );
	}

	// Archive / Resource Library filters submit on change (the design has no submit button).
	wp_enqueue_script( 'm11-filters', M11_URI . '/assets/js/m11-filters.js', array(), filemtime( M11_DIR . '/assets/js/m11-filters.js' ), array( 'strategy' => 'defer' ) );

	if ( file_exists( M11_DIR . $js ) ) {
		wp_enqueue_script( 'm11-main', M11_URI . $js, array(), filemtime( M11_DIR . $js ), array( 'strategy' => 'defer' ) );
	}
}
add_action( 'wp_enqueue_scripts', 'm11_enqueue_assets', 20 );
