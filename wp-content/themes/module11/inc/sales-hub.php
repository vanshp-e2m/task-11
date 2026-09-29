<?php
/**
 * Sales Hub access: pages whose `sections` contain a rep-only layout (sh_dashboard,
 * sh_account, sh_resource_results) require a logged-in sales rep; everyone else is sent to
 * the Sales Hub login page (WP page path 'sales-hub', page 18).
 *
 * "Sales rep" = role `sales_rep` (project fact) or any user who can manage_options
 * (so admins can QA the portal). Filterable via 'm11_can_view_sales_hub'.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Layouts that only sales reps may see.
 *
 * @return string[]
 */
function m11_sales_hub_layouts() {
	return array( 'sh_dashboard', 'sh_account', 'sh_resource_results' );
}

/**
 * Can the current visitor view rep-only Sales Hub content?
 *
 * @return bool
 */
function m11_can_view_sales_hub() {
	$user    = wp_get_current_user();
	$allowed = is_user_logged_in()
		// Editors must be able to preview the portal pages they edit (issues-log #64); reps see it by role.
		&& ( in_array( 'sales_rep', (array) $user->roles, true ) || current_user_can( 'edit_pages' ) );

	return (bool) apply_filters( 'm11_can_view_sales_hub', $allowed, $user );
}

/**
 * Does the given page use any rep-only layout?
 *
 * @param int $post_id Page ID.
 * @return bool
 */
function m11_page_is_sales_hub_gated( $post_id ) {
	if ( ! function_exists( 'get_field' ) ) {
		return false;
	}

	$rows = get_field( 'sections', $post_id, false );
	if ( ! is_array( $rows ) ) {
		return false;
	}

	foreach ( $rows as $row ) {
		if ( isset( $row['acf_fc_layout'] ) && in_array( $row['acf_fc_layout'], m11_sales_hub_layouts(), true ) ) {
			return true;
		}
	}

	return false;
}

/**
 * Redirect visitors without Sales Hub access away from gated pages.
 */
function m11_sales_hub_gate() {
	if ( ! is_page() || m11_can_view_sales_hub() ) {
		return;
	}

	$page_id = get_queried_object_id();
	if ( ! m11_page_is_sales_hub_gated( $page_id ) ) {
		return;
	}

	$login = m11_page_url( 'sales-hub' );
	$login = $login ? $login : wp_login_url( get_permalink( $page_id ) );

	wp_safe_redirect( $login );
	exit;
}
add_action( 'template_redirect', 'm11_sales_hub_gate' );

/**
 * Sales reps never see the WordPress admin bar on the front end (they have no wp-admin access to go to).
 *
 * @param bool $show Whether to show the admin bar.
 * @return bool
 */
function m11_hide_admin_bar_for_reps( $show ) {
	$user = wp_get_current_user();
	return ( $user && in_array( 'sales_rep', (array) $user->roles, true ) ) ? false : $show;
}
add_filter( 'show_admin_bar', 'm11_hide_admin_bar_for_reps' );
