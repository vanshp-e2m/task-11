<?php
/**
 * Layout: sh_account (rep-only)
 * Source: sales-hub-dashboard / account (spec/fragments/sales-hub-dashboard/02-account.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .db-btn prototype in have_rows('account_actions'); db-btn--N = 1-based
 *   row index (source modifier). Labels seeded as drawn, INCLUDING the flagged "Log in"
 *   defect (decision_record q7) -- not corrected here.
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

if ( m11_section_is_hidden() || ! m11_can_view_sales_hub() ) {
	return;
}

$m11_heading = get_sub_field( 'heading' );
?>
<section<?php echo m11_section_attrs( 'rs db-acc', 'account' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_heading ) : ?>
                <h2 class="db-acc-h"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php if ( have_rows( 'account_actions' ) ) : ?>
                <div class="db-acc-btns"><?php
                while ( have_rows( 'account_actions' ) ) :
                    the_row();
                    $m11_link  = m11_link( get_sub_field( 'url' ) );
                    $m11_label = get_sub_field( 'label' ) ? get_sub_field( 'label' ) : $m11_link['title'];
                    if ( ! $m11_link['url'] || ! $m11_label ) {
                        continue;
                    }
                    ?><a class="db-btn db-btn--<?php echo esc_attr( get_row_index() ); ?>"<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo esc_html( $m11_label ); ?></a><?php
                endwhile;
                ?></div>
                <?php endif; ?>
            </div>
        </section>
