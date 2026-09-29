<?php
/**
 * Layout: bottom_links_band
 * Source: resources / continue-your-visit (spec/fragments/resources/05-continue-your-visit.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .bl-btn prototype in have_rows('links'); bl-btn--N (1-based) is the
 *   modifier the source CSS keys on (--2/--3 get the outline border).
 * - Label = row label, else the link's title. Source hrefs (#bottom-link-1/2/3) were BROKEN
 *   placeholders -- now the editor's link field.
 * - Decorative <hr class="rule bl-rule m-only"> kept verbatim.
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
?>
<section<?php echo m11_section_attrs( 'rs bl', 'continue-your-visit' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <hr class="rule bl-rule m-only">
                <?php if ( $m11_heading ) : ?>
                <h2 class="bl-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php if ( have_rows( 'links' ) ) : ?>
                <div class="bl-btns"><?php
                while ( have_rows( 'links' ) ) :
                    the_row();
                    $m11_link  = m11_link( get_sub_field( 'url' ) );
                    $m11_label = get_sub_field( 'label' ) ? get_sub_field( 'label' ) : $m11_link['title'];
                    if ( ! $m11_link['url'] || ! $m11_label ) {
                        continue;
                    }
                    ?><a class="bl-btn bl-btn--<?php echo esc_attr( get_row_index() ); ?>"<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo esc_html( $m11_label ); ?></a><?php
                endwhile;
                ?></div>
                <?php endif; ?>
            </div>
        </section>
