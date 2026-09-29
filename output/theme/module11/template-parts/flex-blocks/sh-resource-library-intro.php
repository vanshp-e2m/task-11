<?php
/**
 * Layout: sh_resource_library_intro
 * Source: sales-hub-resource-library / resource-library-intro
 * (spec/fragments/sales-hub-resource-library/01-resource-library-intro.html). JS hooks: none.
 *
 * Pure transplant: heading -> h1.rlb-h1, body -> p.rlb-body. No hardcoded content.
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

$m11_heading = get_sub_field( 'heading' );
$m11_body    = get_sub_field( 'body' );
?>
<section<?php echo m11_section_attrs( 'rs rl-band', 'resource-library-intro' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="rlb-box">
                    <?php if ( $m11_heading ) : ?>
                    <h1 class="rlb-h1"><?php echo esc_html( $m11_heading ); ?></h1>
                    <?php endif; ?>
                    <?php if ( $m11_body ) : ?>
                    <p class="rlb-body"><?php echo m11_multiline( $m11_body ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                </div>
            </div>
        </section>
