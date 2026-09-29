<?php
/**
 * Content model for the ACF-built pages (approved plan spec/acf-plan.json):
 * m11_product (one single template for every product) and m11_resource (brochures, spec sheets, videos shown on
 * both the public Resources page and the Sales Hub Resource Library), their taxonomies, and the sales_rep role.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Build a label set from a singular/plural pair.
 *
 * @param string $singular Singular label.
 * @param string $plural   Plural label.
 * @return array
 */
function m11_labels( $singular, $plural ) {
	return array(
		'name'          => $plural,
		'singular_name' => $singular,
		/* translators: %s: singular label. */
		'add_new_item'  => sprintf( __( 'Add new %s', 'module11' ), $singular ),
		/* translators: %s: singular label. */
		'edit_item'     => sprintf( __( 'Edit %s', 'module11' ), $singular ),
		/* translators: %s: plural label. */
		'search_items'  => sprintf( __( 'Search %s', 'module11' ), $plural ),
		'menu_name'     => $plural,
	);
}

/**
 * Register the post types and taxonomies.
 */
function m11_register_content_model() {
	// Products: has_archive false — the WP page "products" (Flexible Content) is the browse experience; singles live at /products/<slug>/.
	register_post_type(
		'm11_product',
		array(
			'labels'       => m11_labels( __( 'Product', 'module11' ), __( 'Products', 'module11' ) ),
			'public'       => true,
			'has_archive'  => false,
			'rewrite'      => array( 'slug' => 'products', 'with_front' => false ),
			'supports'     => array( 'title', 'thumbnail' ),
			'show_in_rest' => true,
			'menu_icon'    => 'dashicons-products',
		)
	);

	// Resources: no single template (they are downloads / videos); surfaced through relationship fields and queries.
	register_post_type(
		'm11_resource',
		array(
			'labels'             => m11_labels( __( 'Resource', 'module11' ), __( 'Resources', 'module11' ) ),
			'public'             => false,
			'show_ui'            => true,
			'publicly_queryable' => false,
			'has_archive'        => false,
			'supports'           => array( 'title', 'thumbnail' ),
			'show_in_rest'       => true,
			'menu_icon'          => 'dashicons-media-document',
		)
	);

	$taxonomies = array(
		'product_category'      => array( __( 'Product category', 'module11' ), __( 'Product categories', 'module11' ), array( 'm11_product', 'm11_resource' ), true ),
		'procedure'             => array( __( 'Procedure', 'module11' ), __( 'Procedures', 'module11' ), array( 'm11_product' ), false ),
		'product_configuration' => array( __( 'Product configuration', 'module11' ), __( 'Product configurations', 'module11' ), array( 'm11_product' ), false ),
		'resource_type'         => array( __( 'Resource type', 'module11' ), __( 'Resource types', 'module11' ), array( 'm11_resource' ), false ),
	);
	foreach ( $taxonomies as $tax => $def ) {
		register_taxonomy(
			$tax,
			$def[2],
			array(
				'labels'            => m11_labels( $def[0], $def[1] ),
				'hierarchical'      => $def[3],
				'public'            => true,
				'show_admin_column' => true,
				'show_in_rest'      => true,
				'rewrite'           => array( 'slug' => str_replace( '_', '-', $tax ) ),
			)
		);
	}
}
add_action( 'init', 'm11_register_content_model' );

/**
 * Sales Hub role: reps can read the portal and nothing else.
 */
function m11_register_roles() {
	if ( ! get_role( 'sales_rep' ) ) {
		add_role( 'sales_rep', __( 'Sales rep', 'module11' ), array( 'read' => true ) );
	}
}
add_action( 'init', 'm11_register_roles' );
