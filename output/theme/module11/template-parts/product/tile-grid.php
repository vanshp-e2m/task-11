<?php
/**
 * Product tile grid -- section#accessories (.ts--accessories, ends with <hr class="sec-rule">)
 * and section#related-products (.ts--related-products, no rule). Transplanted from
 * spec/fragments/product-feather-blades/03-accessories.html and 05-related-products.html
 * (identical shape across all 3 products). Tiles: template-parts/tiles/product-tile.php.
 *
 * - Rows come from m11_product_tile_rows(): only rows whose post_object points at a
 *   published m11_product render (plan: accessory targets stay empty until the product
 *   exists). No rows -> no section.
 * - Heading = accessories_heading / related_heading; empty -> the drawn default
 *   "ACCESSORIES" / "RELATED PRODUCTS" (translatable).
 * - Section ids fixed ('accessories' is the tab-bar target).
 *
 * Args: product_id (int), block ('accessories' | 'related').
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

$m11_pid   = isset( $args['product_id'] ) ? (int) $args['product_id'] : get_the_ID();
$m11_block = ( isset( $args['block'] ) && 'related' === $args['block'] ) ? 'related' : 'accessories';
$m11_tiles = m11_product_tile_rows( $m11_pid, $m11_block );

if ( ! $m11_tiles ) {
	return;
}

$m11_is_acc  = 'accessories' === $m11_block;
$m11_heading = trim( (string) get_field( $m11_is_acc ? 'accessories_heading' : 'related_heading', $m11_pid ) );
if ( '' === $m11_heading ) {
	$m11_heading = $m11_is_acc ? __( 'ACCESSORIES', 'module11' ) : __( 'RELATED PRODUCTS', 'module11' );
}
?>
<section class="<?php echo $m11_is_acc ? 'rs ts ts--accessories' : 'rs ts ts--related-products'; ?>" id="<?php echo $m11_is_acc ? 'accessories' : 'related-products'; ?>">
            <div class="fx">
                <h2 class="sec-h"><?php echo esc_html( $m11_heading ); ?></h2>
                <ul class="tiles">
                    <?php
                    foreach ( $m11_tiles as $m11_tile ) {
                        get_template_part( 'template-parts/tiles/product-tile', null, $m11_tile + array( 'context' => $m11_block ) );
                    }
                    ?>
                </ul>
                <?php if ( $m11_is_acc ) : ?>
                <hr class="sec-rule">
                <?php endif; ?>
            </div>
        </section>
