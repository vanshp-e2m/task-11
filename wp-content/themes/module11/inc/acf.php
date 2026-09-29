<?php
/**
 * ACF integration: Local JSON (committed to the repo) and the Site Settings options page.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Save field groups into the theme's acf-json/ folder.
 *
 * @return string
 */
function m11_acf_json_save_point() {
	return M11_DIR . '/acf-json';
}
add_filter( 'acf/settings/save_json', 'm11_acf_json_save_point' );

/**
 * Load field groups from the theme's acf-json/ folder.
 *
 * @param array $paths Existing load paths.
 * @return array
 */
function m11_acf_json_load_point( $paths ) {
	$paths[] = M11_DIR . '/acf-json';
	return $paths;
}
add_filter( 'acf/settings/load_json', 'm11_acf_json_load_point' );

/**
 * Register the Site Settings options page (global header/footer/brand values live here).
 */
function m11_register_options_page() {
	if ( ! function_exists( 'acf_add_options_page' ) ) {
		return;
	}

	acf_add_options_page(
		array(
			'page_title' => __( 'Site Settings', 'module11' ),
			'menu_title' => __( 'Site Settings', 'module11' ),
			'menu_slug'  => 'm11-site-settings',
			'post_id'    => 'options',
			'capability' => 'edit_theme_options',
			'icon_url'   => 'dashicons-admin-settings',
			'redirect'   => false,
		)
	);
}
add_action( 'acf/init', 'm11_register_options_page' );

/**
 * Flexible Content pages are edited through their ACF sections only: open them in the classic screen (the block editor
 * showed an empty "Type / to choose a block" canvas and tucked the sections into a collapsed Meta Boxes drawer), and drop
 * the unused content editor. Every other page/post keeps the block editor.
 *
 * @param bool    $use  Whether to use the block editor.
 * @param WP_Post $post Post being edited.
 * @return bool
 */
function m11_classic_screen_for_flexible_pages( $use, $post ) {
	if ( $post && 'page' === $post->post_type && 'templates/page-flexible.php' === get_page_template_slug( $post ) ) {
		return false;
	}
	return $use;
}
add_filter( 'use_block_editor_for_post', 'm11_classic_screen_for_flexible_pages', 10, 2 );

/**
 * Hide the (unused) main content editor on Flexible Content pages; the sections render the page.
 */
function m11_hide_editor_on_flexible_pages() {
	$post_id = isset( $_GET['post'] ) ? absint( $_GET['post'] ) : 0; // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only admin screen check.
	if ( $post_id && 'templates/page-flexible.php' === get_page_template_slug( $post_id ) ) {
		remove_post_type_support( 'page', 'editor' );
	}
}
add_action( 'admin_init', 'm11_hide_editor_on_flexible_pages' );
