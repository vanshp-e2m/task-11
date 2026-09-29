<?php
/**
 * Brochure card (li.bc) for the resources_brochures layout -- one m11_resource post
 * (brochure / spec sheet) from a collaboration group's `brochure_cards` relationship.
 *
 * Source: spec/fragments/resources/04-brochures.html (li.bc prototypes: title variant in
 * grid groups, excerpt variant .bc-cap--excerpt in paired half groups).
 * Data: post title, cover_image, resource_file (PDF), excerpt, permalink.
 *
 * Args: resource_id (int), variant ('title' | 'excerpt'), mo (int|null mobile-order class).
 *
 * Links (fix for the fragment's BROKEN #download-/#brochure- anchors, per plan):
 * cover -> resource_file (href="#" until a PDF is attached), "Read description" -> the
 * resource permalink. Hardcoded (no field): "Read description", aria-label
 * "Download brochure: %s", alt fallback "%s brochure cover" (used only when the attachment
 * has no alt of its own) -- all translatable. Decorative download badge = theme asset.
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
		'resource_id' => 0,
		'variant'     => 'title',
		'mo'          => null,
	)
);

$m11_rid = (int) $m11_args['resource_id'];
if ( ! $m11_rid || 'm11_resource' !== get_post_type( $m11_rid ) ) {
	return;
}

$m11_title   = get_the_title( $m11_rid );
$m11_cover   = (int) get_field( 'cover_image', $m11_rid );
$m11_file    = (string) get_field( 'resource_file', $m11_rid );
$m11_excerpt = (string) get_field( 'excerpt', $m11_rid );
$m11_alt     = $m11_cover ? (string) get_post_meta( $m11_cover, '_wp_attachment_image_alt', true ) : '';
/* translators: %s: brochure title */
$m11_alt     = $m11_alt ? $m11_alt : sprintf( __( '%s brochure cover', 'module11' ), $m11_title );
$m11_class   = null !== $m11_args['mo'] ? 'bc mo-' . (int) $m11_args['mo'] : 'bc';
$m11_excerpt_variant = 'excerpt' === $m11_args['variant'] && '' !== trim( $m11_excerpt );
?>
                        <li class="<?php echo esc_attr( $m11_class ); ?>">
                            <div class="bc-cover"><a class="bc-link" href="<?php echo $m11_file ? esc_url( $m11_file ) : '#'; ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: brochure title */ __( 'Download brochure: %s', 'module11' ), $m11_title ) ); ?>"><?php echo m11_image( $m11_cover, array( 'class' => 'bc-img', 'alt' => $m11_alt ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?></a><img class="badge" src="<?php echo m11_icon_url( 'icon-download-badge.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="45" height="45"></div>
                            <?php if ( $m11_excerpt_variant ) : ?>
                            <div class="bc-cap bc-cap--excerpt">
                                <p class="ln lh22"><span class="s14"><?php echo esc_html( $m11_excerpt . ' ' ); ?></span><a class="more s14" href="<?php echo esc_url( get_permalink( $m11_rid ) ); ?>"><?php esc_html_e( 'Read description', 'module11' ); ?></a></p>
                            </div>
                            <?php else : ?>
                            <div class="bc-cap">
                                <p class="ln lh22"><strong class="s14"><?php echo esc_html( $m11_title ); ?></strong></p>
                                <p class="ln lh22"><a class="more s14" href="<?php echo esc_url( get_permalink( $m11_rid ) ); ?>"><?php esc_html_e( 'Read description', 'module11' ); ?></a></p>
                            </div>
                            <?php endif; ?>
                        </li>
