<?php
/**
 * Layout: value_columns
 * Source: home / value-columns (spec/fragments/home/03-value-columns.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .vc-card prototype inside have_rows('value_cards'); vc-card--N is the
 *   position modifier the source CSS keys on (1-based row index).
 * - lead: restricted kses so the editor's <br class="d-only"> survives.
 * - icon: decorative in the fragment (alt=""), class vc-icon, lazy.
 * - closing_cta_label href = closing_cta_url; empty -> the fragment's '#downloadable-brochures'
 *   (flagged BROKEN in the spec -- the editor should set resources#brochures).
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

$m11_cta = get_sub_field( 'closing_cta_label' );
?>
<section<?php echo m11_section_attrs( 'vc rs', 'value-columns' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php
                if ( have_rows( 'value_cards' ) ) :
                    while ( have_rows( 'value_cards' ) ) :
                        the_row();
                        $m11_title = get_sub_field( 'title' );
                        $m11_lead  = get_sub_field( 'lead' );
                        $m11_body  = get_sub_field( 'body' );
                        ?>
                <article class="vc-card vc-card--<?php echo esc_attr( get_row_index() ); ?>">
                    <?php if ( $m11_title ) : ?><h3 class="vc-title"><?php echo esc_html( $m11_title ); ?></h3><?php endif; ?><?php echo m11_image( get_sub_field( 'icon' ), array( 'class' => 'vc-icon', 'alt' => '' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                    <div class="vc-text">
                        <?php if ( $m11_lead ) : ?>
                        <p class="vc-lead"><?php echo m11_accent_kses( $m11_lead ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                        <?php endif; ?>
                        <?php if ( $m11_body ) : ?>
                        <p class="vc-body"><?php echo m11_multiline( $m11_body ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                        <?php endif; ?>
                    </div>
                </article><?php
                    endwhile;
                endif;
                ?><?php if ( $m11_cta ) : ?><a class="vc-btn" href="<?php echo esc_url( m11_href( get_sub_field( 'closing_cta_url' ), '#downloadable-brochures' ) ); ?>"><?php echo esc_html( $m11_cta ); ?></a><?php endif; ?>
            </div>
        </section>
