<?php
/**
 * Layout: products_intro
 * Source: products / products-intro (spec/fragments/products/01-products-intro.html). JS hooks: none.
 *
 * Reads: page_title; page_heading clone (seamless) -> heading_tag, heading; subheading;
 * body; cta_label.
 * Transplant notes:
 * - heading: restricted kses (keeps the editor's <br>); the verbatim <h2 class="pbh-h2">
 *   is kept when heading_tag is empty/h2, any other tag keeps the class.
 * - cta_label href = cta_url; empty -> the fragment's '#browse-by-product'.
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

if ( m11_section_is_hidden() ) {
	return;
}

$m11_title   = get_sub_field( 'page_title' );
$m11_tag     = (string) get_sub_field( 'heading_tag' );
$m11_heading = get_sub_field( 'heading' );
$m11_sub     = get_sub_field( 'subheading' );
$m11_body    = get_sub_field( 'body' );
$m11_cta     = get_sub_field( 'cta_label' );
?>
<section<?php echo m11_section_attrs( 'rs pbh', 'products-intro' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_title ) : ?>
                <h1 class="pbh-h1"><?php echo esc_html( $m11_title ); ?></h1>
                <?php endif; ?>
                <div class="pbh-panel">
                    <?php if ( $m11_heading && in_array( $m11_tag, array( '', 'h2' ), true ) ) : ?>
                    <h2 class="pbh-h2"><?php echo m11_accent_kses( $m11_heading ); // phpcs:ignore WordPress.Security.EscapeOutput ?></h2>
                    <?php elseif ( $m11_heading ) : ?>
                    <?php echo m11_section_head( $m11_tag, $m11_heading, 'pbh-h2' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                    <?php endif; ?>
                    <?php if ( $m11_sub ) : ?>
                    <p class="pbh-sub"><?php echo esc_html( $m11_sub ); ?></p>
                    <?php endif; ?>
                    <?php if ( $m11_body ) : ?>
                    <p class="pbh-body"><?php echo m11_multiline( $m11_body ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p><?php endif; ?><?php if ( $m11_cta ) : ?><a class="pbh-link" href="<?php echo esc_url( m11_href( get_sub_field( 'cta_url' ), '#browse-by-product' ) ); ?>"><?php echo esc_html( $m11_cta ); ?></a><?php endif; ?>
                </div>
            </div>
        </section>
