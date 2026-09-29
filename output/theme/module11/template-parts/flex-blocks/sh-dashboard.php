<?php
/**
 * Layout: sh_dashboard (rep-only; page gate in inc/sales-hub.php, re-checked here)
 * Source: sales-hub-dashboard / dashboard (spec/fragments/sales-hub-dashboard/01-dashboard.html). JS hooks: none.
 *
 * Transplant notes:
 * - h1 greeting = the logged-in user's display name (plan static_content: the spec's
 *   "Hello, John Q." is a demo persona). HARDCODED string "Hello, %s" (translatable).
 * - stats: label is ACF; .db-num is computed by m11_dashboard_stat( row index ) per
 *   decision_record q6 (row 1 categories, row 2 brochures+spec sheets, row 3 videos). Rows
 *   4+ have no mapped query and render the label alone.
 * - tools: one verbatim .db-tool prototype; title is wrapped in the row's link field.
 *   Icons are above the fold (fragment has no loading attr) -> not lazy; alt="" as drawn.
 * - HARDCODED a11y string: aria-label "At a glance" on .db-stats.
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

$m11_user = wp_get_current_user();
$m11_lead = get_sub_field( 'lead' );
?>
<section<?php echo m11_section_attrs( 'rs db', 'dashboard' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="db-panel">
                    <?php if ( $m11_user->exists() ) : ?>
                    <h1 class="db-h1"><?php echo esc_html( sprintf( /* translators: %s: user display name */ __( 'Hello, %s', 'module11' ), $m11_user->display_name ) ); ?></h1>
                    <?php endif; ?>
                    <?php if ( $m11_lead ) : ?>
                    <p class="db-lead"><?php echo m11_multiline( $m11_lead ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                    <div class="db-grid">
                        <?php if ( have_rows( 'stats' ) ) : ?>
                        <ul class="db-stats" aria-label="<?php esc_attr_e( 'At a glance', 'module11' ); ?>">
                            <?php
                            while ( have_rows( 'stats' ) ) :
                                the_row();
                                $m11_num   = m11_dashboard_stat( get_row_index() - 1 );
                                $m11_label = get_sub_field( 'label' );
                                ?>
                            <li class="db-stat"><?php if ( null !== $m11_num ) : ?><span class="db-num"><?php echo esc_html( number_format_i18n( $m11_num ) ); ?></span><?php endif; ?><?php if ( $m11_label ) : ?><span class="db-label"><?php echo esc_html( $m11_label ); ?></span><?php endif; ?></li>
                            <?php endwhile; ?>
                        </ul>
                        <?php endif; ?>
                        <?php if ( have_rows( 'tools' ) ) : ?>
                        <ul class="db-tools">
                            <?php
                            while ( have_rows( 'tools' ) ) :
                                the_row();
                                $m11_title = get_sub_field( 'title' );
                                $m11_link  = get_sub_field( 'link' );
                                $m11_desc  = get_sub_field( 'description' );
                                ?>
                            <li class="db-tool"><span class="db-icon"><?php echo m11_image( get_sub_field( 'icon' ), array( 'alt' => '', 'loading' => false ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?></span>
                                <div class="db-tool-text">
                                    <?php if ( $m11_title ) : ?>
                                    <h2 class="db-tool-h"><?php if ( m11_link( $m11_link )['url'] ) : ?><a<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo esc_html( $m11_title ); ?></a><?php else : ?><?php echo esc_html( $m11_title ); ?><?php endif; ?></h2>
                                    <?php endif; ?>
                                    <?php if ( $m11_desc ) : ?>
                                    <p class="db-tool-p"><?php echo m11_multiline( $m11_desc ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                                    <?php endif; ?>
                                </div>
                            </li>
                            <?php endwhile; ?>
                        </ul>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </section>
