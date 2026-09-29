<?php
/**
 * Resource tile (li.tile) for the Sales Hub Resource Library (sh_resource_results).
 *
 * Source: spec/fragments/sales-hub-resource-library/02-resource-results.html (li.tile).
 * Data (plan static_content): post title, cover_image, first product_category term (used
 * for BOTH .tile-tag and .tile-sub, per plan), resource_type (PDF badge), resource_file.
 *
 * Args: resource_id (int).
 *
 * - .tile-pdf badge: only for non-video resources (brochure / spec sheet); videos get none.
 * - .tile-dl: resource_file URL; rendered only when a file is attached (videos without a
 *   file render no download link -- no "watch" label exists in the design).
 * - Hardcoded (no field, translatable): "Download", aria-label "Download: %s", badge alt
 *   "PDF". Title stays <h2> exactly as drawn (spec flags the h2-vs-h3 inconsistency).
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

$m11_args = wp_parse_args( isset( $args ) ? $args : array(), array( 'resource_id' => 0 ) );
$m11_rid  = (int) $m11_args['resource_id'];
if ( ! $m11_rid || 'm11_resource' !== get_post_type( $m11_rid ) ) {
	return;
}

$m11_title = get_the_title( $m11_rid );
$m11_cover = (int) get_field( 'cover_image', $m11_rid );
$m11_alt   = $m11_cover ? (string) get_post_meta( $m11_cover, '_wp_attachment_image_alt', true ) : '';
$m11_file  = (string) get_field( 'resource_file', $m11_rid );
$m11_cat   = m11_first_term( $m11_rid, 'product_category' );
$m11_video = m11_resource_is_video( $m11_rid );
?>
                            <li class="tile">
                                <div class="tile-media"><?php echo m11_image( $m11_cover, array( 'alt' => $m11_alt ? $m11_alt : $m11_title ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><?php if ( $m11_cat ) : ?><span class="tile-tag"><?php echo esc_html( $m11_cat->name ); ?></span><?php endif; ?><?php if ( ! $m11_video ) : ?><span class="tile-pdf"><img src="<?php echo m11_icon_url( 'icon-pdf.png' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="<?php esc_attr_e( 'PDF', 'module11' ); ?>" width="36" height="50"></span><?php endif; ?></div>
                                <div class="tile-text">
                                    <h2 class="tile-title"><?php echo esc_html( $m11_title ); ?></h2>
                                    <?php if ( $m11_cat ) : ?>
                                    <p class="tile-sub"><?php echo esc_html( $m11_cat->name ); ?></p>
                                    <?php endif; ?>
                                </div><?php if ( $m11_file ) : ?><a class="tile-dl" href="<?php echo esc_url( $m11_file ); ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: resource title */ __( 'Download: %s', 'module11' ), $m11_title ) ); ?>"><img src="<?php echo m11_icon_url( 'icon-download-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="30" height="30"><?php esc_html_e( 'Download', 'module11' ); ?></a><?php endif; ?>
                            </li>
