<?php
/**
 * Video item (li.rt-vid) for the resources_testimonials layout -- one m11_resource post
 * (resource_type = video) from an expert entry's `videos` relationship.
 *
 * Source: spec/fragments/resources/02-testimonials.html (li.rt-vid prototype).
 * Data: post title, cover_image, excerpt, Media Block clone (video URL).
 *
 * Args: resource_id (int), with_caption (bool -- false when the expert entry uses its
 * shared_caption instead of per-video captions).
 *
 * Hardcoded (no field in the schema): the "Topic: " caption prefix, the "Read more" link
 * text, aria-label "Play video: %s" (all translatable). Deviation: the fragment's last
 * video caption reads just "Extended Version" (no "Topic:" prefix); this template always
 * renders "Topic: {post title}".
 * "Read more" + the thumbnail both point at the resource's video URL (no single-resource
 * template this phase); href="#" when the resource has no video URL, "Read more" omitted.
 * The .tx-cap width utility is the fragment's most common value (w281) -- the per-item
 * Figma widths (w293/w296) have no field.
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
		'resource_id'  => 0,
		'with_caption' => true,
	)
);

$m11_rid = (int) $m11_args['resource_id'];
if ( ! $m11_rid || 'm11_resource' !== get_post_type( $m11_rid ) ) {
	return;
}

$m11_title   = get_the_title( $m11_rid );
$m11_cover   = (int) get_field( 'cover_image', $m11_rid );
$m11_excerpt = (string) get_field( 'excerpt', $m11_rid );
$m11_url     = m11_resource_video_url( $m11_rid );
?>
                            <li class="rt-vid"><a class="vid rt-thumb" href="<?php echo $m11_url ? esc_url( $m11_url ) : '#'; ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: video title */ __( 'Play video: %s', 'module11' ), $m11_title ) ); ?>"><?php echo m11_image( $m11_cover, array( 'alt' => $m11_title ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><img class="play" src="<?php echo m11_icon_url( 'icon-play-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="53" height="53"></a><?php if ( $m11_args['with_caption'] ) : ?>
                                <div class="tx-cap w281">
                                    <p class="ln lh22"><strong class="s14"><?php echo esc_html( sprintf( /* translators: %s: video title */ __( 'Topic: %s', 'module11' ), $m11_title ) ); ?></strong></p>
                                    <?php if ( '' !== trim( $m11_excerpt ) ) : ?>
                                    <p class="ln lh20 shn1"><span class="s12"><?php echo esc_html( $m11_excerpt ); ?></span></p>
                                    <?php endif; ?>
                                    <?php if ( $m11_url ) : ?>
                                    <p class="ln lh20 shn1"><a class="more s12" href="<?php echo esc_url( $m11_url ); ?>"><?php esc_html_e( 'Read more', 'module11' ); ?></a></p>
                                    <?php endif; ?>
                                </div>
                            <?php endif; ?></li>
