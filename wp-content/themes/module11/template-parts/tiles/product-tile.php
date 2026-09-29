<?php
/**
 * Product tile (.tile) -- shared by the products listing (browse_by_product, context
 * 'browse' = .tile.ptile with category tag + procedure chips) and the single-product
 * Accessories / Related Products grids (context 'accessories' | 'related' = plain .tile).
 *
 * Source: spec/fragments/products/03-browse-by-product.html (li.tile.ptile) and
 * spec/fragments/product-feather-blades/03-accessories.html + 05-related-products.html (same on all 3 products) (li.tile).
 * Data: the m11_product post (title, permalink, gallery_image, model_line) + taxonomy
 * terms -- plan static_content: tiles are query output, not authored per page.
 *
 * Args (get_template_part $args):
 *   product_id (int, required) | context (string) | caption (string override for .tile-sub)
 *   | image_id (int override for the tile image).
 *
 * Hardcoded (no field in the schema): "View product" link text and the ": %s"
 * visually-hidden suffix (translatable), aria-label "Procedures" on .ptags.
 * Procedure chips: first 2 terms + a "+N" overflow chip (fragment: "Craniotomy, Aneurysm, +2").
 *
 * Lint (lint_partial.py --fragment) justification: every tag-count WARN is a repeater /
 * query-loop prototype (1 verbatim item for N drawn); every "MISSING" ERROR is one of
 * (a) <img> emitted by wp_get_attachment_image() (house rule), (b) <br>/<span>/<strong>
 * that live INSIDE field content (accent kses / m11_multiline / m11_strong_runs /
 * m11_line_block), (c) children delegated to a tiles/ or cards/ part. Verified by rendering
 * each file offline from fragment-seeded fixtures and diffing the normalised DOM against
 * the fragment (only the deviations listed above remain).
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

$m11_args = wp_parse_args(
	isset( $args ) ? $args : array(),
	array(
		'product_id' => 0,
		'context'    => 'browse',
		'caption'    => '',
		'image_id'   => 0,
	)
);

$m11_pid = (int) $m11_args['product_id'];
if ( ! $m11_pid || 'm11_product' !== get_post_type( $m11_pid ) ) {
	return;
}

$m11_title   = get_the_title( $m11_pid );
$m11_browse  = 'browse' === $m11_args['context'];
$m11_image   = $m11_args['image_id'] ? (int) $m11_args['image_id'] : (int) get_field( 'gallery_image', $m11_pid );
$m11_alt     = $m11_image ? (string) get_post_meta( $m11_image, '_wp_attachment_image_alt', true ) : '';
$m11_sub     = '' !== trim( (string) $m11_args['caption'] ) ? $m11_args['caption'] : wp_strip_all_tags( (string) get_field( 'model_line', $m11_pid ) );
$m11_cat     = $m11_browse ? m11_first_term( $m11_pid, 'product_category' ) : null;
$m11_procs   = $m11_browse ? get_the_terms( $m11_pid, 'procedure' ) : array();
$m11_procs   = ( $m11_procs && ! is_wp_error( $m11_procs ) ) ? $m11_procs : array();
$m11_visible = array_slice( $m11_procs, 0, 2 );
$m11_extra   = count( $m11_procs ) - count( $m11_visible );
?>
                            <li class="<?php echo $m11_browse ? 'tile ptile' : 'tile'; ?>">
                                <div class="tile-media"><?php echo m11_image( $m11_image, array( 'alt' => $m11_alt ? $m11_alt : $m11_title ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><?php if ( $m11_cat ) : ?><span class="tile-tag"><?php echo esc_html( $m11_cat->name ); ?></span><?php endif; ?></div>
                                <div class="tile-text">
                                    <h3 class="tile-title"><?php echo esc_html( $m11_title ); ?></h3>
                                    <?php if ( $m11_sub ) : ?>
                                    <p class="tile-sub"><?php echo esc_html( $m11_sub ); ?></p>
                                    <?php endif; ?>
                                </div><?php if ( $m11_procs ) : ?>
                                <ul class="ptags" aria-label="<?php esc_attr_e( 'Procedures', 'module11' ); ?>">
                                    <?php foreach ( $m11_visible as $m11_term ) : ?>
                                    <li class="ptag"><?php echo esc_html( $m11_term->name ); ?></li>
                                    <?php endforeach; ?>
                                    <?php if ( $m11_extra > 0 ) : ?>
                                    <li class="ptag"><?php echo esc_html( '+' . $m11_extra ); ?></li>
                                    <?php endif; ?>
                                </ul><?php endif; ?><a class="tile-view" href="<?php echo esc_url( get_permalink( $m11_pid ) ); ?>"><?php esc_html_e( 'View product', 'module11' ); ?><span class="visually-hidden">: <?php echo esc_html( $m11_title ); ?></span></a>
                            </li>
