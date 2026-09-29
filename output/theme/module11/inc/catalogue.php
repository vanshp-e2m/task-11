<?php
/**
 * Catalogue helpers: m11_product / m11_resource queries, GET filter state, per-record
 * field lookups and the Sales Hub dashboard counts.
 *
 * Filter query args are prefixed `f_` on purpose: the fragments used name="category" /
 * "procedure" / "product_category" / "resource_type", but those collide with WordPress
 * public query vars (taxonomy query_var defaults) and would turn the page request into a
 * taxonomy archive (404 on the flexible page). Read-only GET filters: no nonce needed.
 *
 * Requires: taxonomies product_category, procedure, product_configuration, resource_type
 * and CPTs m11_product / m11_resource (registered elsewhere, build step B2).
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/* -------------------------------------------------------------------------
 * GET filter state
 * ---------------------------------------------------------------------- */

/**
 * Selected term slugs for a filter key (?f_category[]=instruments…).
 *
 * @param string $key Query arg.
 * @return string[]
 */
function m11_filter_values( $key ) {
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only listing filter.
	$raw = isset( $_GET[ $key ] ) ? wp_unslash( $_GET[ $key ] ) : array();

	return array_values( array_filter( array_map( 'sanitize_title', (array) $raw ) ) );
}

/**
 * Scalar GET value (search term / sort key).
 *
 * @param string $key Query arg.
 * @return string
 */
function m11_filter_text( $key ) {
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- read-only listing filter.
	return isset( $_GET[ $key ] ) ? sanitize_text_field( wp_unslash( $_GET[ $key ] ) ) : '';
}

/**
 * Current listing page number (?f_page=2).
 *
 * @return int
 */
function m11_filter_page() {
	return max( 1, absint( m11_filter_text( 'f_page' ) ) );
}

/**
 * Filter map for a listing: GET key => taxonomy.
 *
 * @param string $listing 'products' | 'resources'.
 * @return array
 */
function m11_filter_map( $listing ) {
	if ( 'resources' === $listing ) {
		return array(
			'f_type'     => 'resource_type',
			'f_category' => 'product_category',
		);
	}

	return array(
		'f_category'      => 'product_category',
		'f_configuration' => 'product_configuration',
		'f_procedure'     => 'procedure',
	);
}

/**
 * tax_query for the current GET state.
 *
 * @param string $listing 'products' | 'resources'.
 * @return array
 */
function m11_filter_tax_query( $listing ) {
	$tax_query = array();

	foreach ( m11_filter_map( $listing ) as $key => $taxonomy ) {
		$terms = m11_filter_values( $key );
		if ( $terms ) {
			$tax_query[] = array(
				'taxonomy' => $taxonomy,
				'field'    => 'slug',
				'terms'    => $terms,
			);
		}
	}

	if ( count( $tax_query ) > 1 ) {
		$tax_query['relation'] = 'AND';
	}

	return $tax_query;
}

/**
 * Active filter chips for the current GET state: list of term objects.
 *
 * @param string $listing 'products' | 'resources'.
 * @return WP_Term[]
 */
function m11_filter_active_terms( $listing ) {
	$active = array();

	foreach ( m11_filter_map( $listing ) as $key => $taxonomy ) {
		foreach ( m11_filter_values( $key ) as $slug ) {
			$term = get_term_by( 'slug', $slug, $taxonomy );
			if ( $term && ! is_wp_error( $term ) ) {
				$active[] = $term;
			}
		}
	}

	return $active;
}

/**
 * Terms for one filter fieldset (all terms, empty ones included so the list is stable).
 *
 * @param string $taxonomy Taxonomy.
 * @return WP_Term[]
 */
function m11_filter_terms( $taxonomy ) {
	if ( ! taxonomy_exists( $taxonomy ) ) {
		return array();
	}

	$terms = get_terms(
		array(
			'taxonomy'   => $taxonomy,
			'hide_empty' => false,
		)
	);

	return is_wp_error( $terms ) ? array() : $terms;
}

/**
 * Fieldset legend for a taxonomy: its singular label (CSS uppercases .fl-h).
 *
 * @param string $taxonomy Taxonomy.
 * @return string
 */
function m11_filter_legend( $taxonomy ) {
	$tax = get_taxonomy( $taxonomy );

	return $tax ? (string) $tax->labels->singular_name : '';
}

/**
 * Published posts of a type in a term (resource filter counts, dashboard stats).
 *
 * @param string       $post_type Post type.
 * @param string       $taxonomy  Taxonomy ('' for no term restriction).
 * @param string|array $terms     Term slug(s).
 * @return int
 */
function m11_count_posts_in_terms( $post_type, $taxonomy = '', $terms = array() ) {
	$args = array(
		'post_type'      => $post_type,
		'post_status'    => 'publish',
		'posts_per_page' => 1,
		'fields'         => 'ids',
	);

	if ( $taxonomy ) {
		$args['tax_query'] = array( // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_tax_query
			array(
				'taxonomy' => $taxonomy,
				'field'    => 'slug',
				'terms'    => (array) $terms,
			),
		);
	}

	$query = new WP_Query( $args );

	return (int) $query->found_posts;
}

/**
 * URL of the current page with the given GET args replaced (others kept), plus a hash.
 *
 * @param array  $args Args to set (null removes).
 * @param string $hash '#anchor' or ''.
 * @return string Unescaped URL.
 */
function m11_listing_url( $args, $hash = '' ) {
	// phpcs:ignore WordPress.Security.NonceVerification.Recommended -- rebuilding read-only filter URL.
	$current = array_map( 'wp_unslash', $_GET );
	$query   = array_merge( $current, $args );
	$query   = array_filter(
		$query,
		static function ( $v ) {
			return null !== $v && '' !== $v && array() !== $v;
		}
	);

	return add_query_arg( $query, get_permalink() ) . $hash;
}

/* -------------------------------------------------------------------------
 * Queries
 * ---------------------------------------------------------------------- */

/**
 * Products listing query for the browse_by_product layout.
 *
 * @return WP_Query
 */
function m11_products_query() {
	$args = array(
		'post_type'      => 'm11_product',
		'post_status'    => 'publish',
		'posts_per_page' => (int) apply_filters( 'm11_products_per_page', 12 ),
		'paged'          => m11_filter_page(),
		'orderby'        => 'title',
		'order'          => 'ASC',
	);

	$tax_query = m11_filter_tax_query( 'products' );
	if ( $tax_query ) {
		$args['tax_query'] = $tax_query; // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_tax_query
	}

	$search = m11_filter_text( 'f_q' );
	if ( '' !== $search ) {
		$args['s'] = $search;
	}

	return new WP_Query( apply_filters( 'm11_products_query_args', $args ) );
}

/**
 * Resource Library query for the sh_resource_results layout.
 *
 * @return WP_Query
 */
function m11_resources_query() {
	$sorts = array(
		'az'     => array( 'title', 'ASC' ),
		'za'     => array( 'title', 'DESC' ),
		'newest' => array( 'date', 'DESC' ),
	);
	$sort  = m11_filter_text( 'f_sort' );
	$sort  = isset( $sorts[ $sort ] ) ? $sorts[ $sort ] : $sorts['az'];

	$args = array(
		'post_type'      => 'm11_resource',
		'post_status'    => 'publish',
		// The Resource Library design has no pager: show every match.
		'posts_per_page' => (int) apply_filters( 'm11_resources_per_page', -1 ),
		'orderby'        => $sort[0],
		'order'          => $sort[1],
	);

	$tax_query = m11_filter_tax_query( 'resources' );
	if ( $tax_query ) {
		$args['tax_query'] = $tax_query; // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_tax_query
	}

	$search = m11_filter_text( 'f_q' );
	if ( '' !== $search ) {
		$args['s'] = $search;
	}

	return new WP_Query( apply_filters( 'm11_resources_query_args', $args ) );
}

/* -------------------------------------------------------------------------
 * Per-record lookups
 * ---------------------------------------------------------------------- */

/**
 * First assigned term of a taxonomy (primary category for tiles / breadcrumbs).
 *
 * @param int    $post_id  Post ID.
 * @param string $taxonomy Taxonomy.
 * @return WP_Term|null
 */
function m11_first_term( $post_id, $taxonomy ) {
	$terms = get_the_terms( $post_id, $taxonomy );

	return ( $terms && ! is_wp_error( $terms ) ) ? $terms[0] : null;
}

/**
 * Is this m11_resource a video (resource_type = video)?
 *
 * @param int $resource_id Resource ID.
 * @return bool
 */
function m11_resource_is_video( $resource_id ) {
	return has_term( 'video', 'resource_type', $resource_id );
}

/**
 * Playable URL for a video resource from its seamless Media Block clone
 * (third_party_url, else custom_video). '' when none.
 *
 * @param int $resource_id Resource ID.
 * @return string Unescaped URL.
 */
function m11_resource_video_url( $resource_id ) {
	if ( ! function_exists( 'get_field' ) ) {
		return '';
	}

	if ( 'third_party' === get_field( 'video_type', $resource_id ) ) {
		return (string) get_field( 'third_party_url', $resource_id );
	}

	$url = (string) get_field( 'custom_video', $resource_id );

	return $url ? $url : (string) get_field( 'third_party_url', $resource_id );
}

/* -------------------------------------------------------------------------
 * Single product helpers
 * ---------------------------------------------------------------------- */

/**
 * The product's CTA buttons (button_group clone `buttons` -> rows with `cta` link), shared
 * by the overview (.pd-ctas) and testimonial (.tq-ctas) positions. First button solid,
 * the rest outline with the fragment's decorative arrow span. Uses get_field() + foreach
 * (no shared have_rows cursor -- it is rendered twice per request).
 *
 * @param int $product_id Product ID.
 * @return string Escaped HTML ('' when no buttons).
 */
function m11_product_ctas_html( $product_id ) {
	$rows = get_field( 'buttons', $product_id );
	$out  = '';

	if ( ! is_array( $rows ) ) {
		return '';
	}

	foreach ( array_values( $rows ) as $i => $row ) {
		$link = isset( $row['cta'] ) ? $row['cta'] : '';
		$out .= 0 === $i
			? m11_button( $link, '', 'pbtn pbtn--solid' )
			: m11_button( $link, '', 'pbtn pbtn--line', '<span class="dl-arrow" aria-hidden="true"></span>' );
	}

	return $out;
}

/**
 * Product section tabs (plan static_content product_tabs: template-generated, fixed
 * logic). Overview always (target fixed to #product-overview -- the fragment's #overview
 * never resolved), Size Guide / Instruments Included when that block renders, Accessories
 * when the accessories block renders.
 *
 * @param int $product_id Product ID.
 * @return array[] { label, href }
 */
function m11_product_tabs( $product_id ) {
	$tabs = array(
		array(
			'label' => __( 'Overview', 'module11' ),
			'href'  => '#product-overview',
		),
	);

	if ( get_field( 'has_size_guide', $product_id ) && get_field( 'size_rows', $product_id ) ) {
		$tabs[] = array(
			'label' => __( 'Size Guide', 'module11' ),
			'href'  => '#size-guide',
		);
	}

	if ( get_field( 'has_instruments_table', $product_id ) && get_field( 'instrument_rows', $product_id ) ) {
		$tabs[] = array(
			'label' => __( 'Instruments Included', 'module11' ),
			'href'  => '#instruments-included',
		);
	}

	if ( m11_product_tile_rows( $product_id, 'accessories' ) ) {
		$tabs[] = array(
			'label' => __( 'Accessories', 'module11' ),
			'href'  => '#accessories',
		);
	}

	return $tabs;
}

/**
 * Resolved tile rows for the accessories / related_products repeaters: rows whose
 * post_object points at a published m11_product (empty rows are skipped -- plan: the
 * field stays empty until that product exists).
 *
 * @param int    $product_id Product ID.
 * @param string $block      'accessories' | 'related'.
 * @return array[] { product_id, caption, image_id }
 */
function m11_product_tile_rows( $product_id, $block ) {
	$field = 'accessories' === $block ? 'accessories' : 'related_products';
	$rows  = get_field( $field, $product_id );
	$tiles = array();

	if ( ! is_array( $rows ) ) {
		return $tiles;
	}

	foreach ( $rows as $row ) {
		$target = isset( $row['product'] ) ? $row['product'] : null;
		$tid    = $target instanceof WP_Post ? $target->ID : absint( $target );
		if ( ! $tid || 'publish' !== get_post_status( $tid ) ) {
			continue;
		}
		$tiles[] = array(
			'product_id' => $tid,
			'caption'    => isset( $row['caption'] ) ? (string) $row['caption'] : '',
			'image_id'   => isset( $row['image_override'] ) ? absint( $row['image_override'] ) : 0,
		);
	}

	return $tiles;
}

/* -------------------------------------------------------------------------
 * Sales Hub dashboard counts (decision_record q6 -- keyed by stats row index)
 * ---------------------------------------------------------------------- */

/**
 * Computed number for dashboard stat row $index (0-based). null when the row has no
 * mapped query (rows 4+), so the partial renders the label alone.
 *
 * 0 = non-empty product_category terms (>= 1 published m11_product)
 * 1 = published m11_resource with resource_type in (brochure, spec-sheet)
 * 2 = published m11_resource with resource_type = video
 *
 * @param int $index Row index.
 * @return int|null
 */
function m11_dashboard_stat( $index ) {
	switch ( (int) $index ) {
		case 0:
			$count = 0;
			foreach ( m11_filter_terms( 'product_category' ) as $term ) {
				if ( m11_count_posts_in_terms( 'm11_product', 'product_category', $term->slug ) > 0 ) {
					++$count;
				}
			}
			return $count;
		case 1:
			return m11_count_posts_in_terms( 'm11_resource', 'resource_type', array( 'brochure', 'spec-sheet' ) );
		case 2:
			return m11_count_posts_in_terms( 'm11_resource', 'resource_type', 'video' );
	}

	return null;
}
