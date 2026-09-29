<?php
/**
 * Layout: intro_statement
 * Source: home / intro-statement (spec/fragments/home/02-intro-statement.html). JS hooks: none.
 *
 * Reads (seamless clones): section_heading -> heading_tag, heading, content; own: cta_label.
 * Transplant notes:
 * - heading_tag: the fragment's verbatim <h2 class="intro-h2"> is kept when the tag is
 *   empty/h2; any other choice renders the same class on the chosen tag.
 * - cta_label href = cta_url; empty -> the fragment's '#testimonials'.
 * - <hr class="intro-rule"> is decorative, kept verbatim.
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

$m11_tag     = (string) get_sub_field( 'heading_tag' );
$m11_heading = get_sub_field( 'heading' );
$m11_content = get_sub_field( 'content' );
$m11_cta     = get_sub_field( 'cta_label' );
?>
<section<?php echo m11_section_attrs( 'intro rs', 'intro-statement' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_heading && in_array( $m11_tag, array( '', 'h2' ), true ) ) : ?>
                <h2 class="intro-h2"><?php echo m11_accent_kses( $m11_heading ); // phpcs:ignore WordPress.Security.EscapeOutput ?></h2>
                <?php elseif ( $m11_heading ) : ?>
                <?php echo m11_section_head( $m11_tag, $m11_heading, 'intro-h2' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                <?php endif; ?>
                <?php if ( $m11_content ) : ?>
                <p class="intro-p"><?php echo m11_multiline( $m11_content ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                <?php endif; ?>
                <?php if ( $m11_cta ) : ?>
                <a class="intro-btn" href="<?php echo esc_url( m11_href( get_sub_field( 'cta_url' ), '#testimonials' ) ); ?>"><?php echo esc_html( $m11_cta ); ?></a>
                <?php endif; ?>
                <hr class="intro-rule">
            </div>
        </section>
