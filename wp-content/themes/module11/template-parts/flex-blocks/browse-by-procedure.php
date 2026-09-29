<?php
/**
 * Layout: browse_by_procedure
 * Source: products / browse-by-procedure (spec/fragments/products/02-browse-by-procedure.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .pr-item prototype in have_rows('procedure_items').
 * - Position modifiers pr-item--tumor-remo / --aneurysm / --endoscopic (source CSS keys
 *   icon size/offsets on them) are mapped from the row index; rows 4+ get none.
 *   HARDCODED class map -- report.
 * - view_link (link): label = the link's own title (fragment "View product →").
 * - more_label href = more_url; empty -> the fragment's '#browse-by-product'.
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
$m11_lead    = get_sub_field( 'lead' );
$m11_mods    = array( 1 => 'pr-item--tumor-remo', 2 => 'pr-item--aneurysm', 3 => 'pr-item--endoscopic' );
?>
<section<?php echo m11_section_attrs( 'rs pr', 'browse-by-procedure' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="pr-head">
                    <?php if ( $m11_heading ) : ?>
                    <h2 class="pr-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                    <?php endif; ?>
                    <?php if ( $m11_lead ) : ?>
                    <p class="pr-lead"><?php echo m11_multiline( $m11_lead ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                </div>
                <?php if ( have_rows( 'procedure_items' ) ) : ?>
                <div class="pr-items">
                    <?php
                    while ( have_rows( 'procedure_items' ) ) :
                        the_row();
                        $m11_i     = get_row_index();
                        $m11_class = trim( 'pr-item ' . ( isset( $m11_mods[ $m11_i ] ) ? $m11_mods[ $m11_i ] : '' ) );
                        $m11_title = get_sub_field( 'title' );
                        $m11_more  = get_sub_field( 'more_label' );
                        ?>
                    <article class="<?php echo esc_attr( $m11_class ); ?>"><?php echo m11_image( get_sub_field( 'icon' ), array( 'class' => 'pr-icon', 'alt' => '' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                        <div class="pr-text">
                            <?php if ( $m11_title ) : ?><h3 class="pr-title"><?php echo esc_html( $m11_title ); ?></h3><?php endif; ?><?php $m11_view = m11_link( get_sub_field( 'view_link' ) ); ?><?php if ( $m11_view['url'] && $m11_view['title'] ) : ?><a class="pr-view"<?php echo m11_link_attrs( $m11_view ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo esc_html( $m11_view['title'] ); ?></a><?php endif; ?><?php if ( $m11_more ) : ?><a class="pr-more" href="<?php echo esc_url( m11_href( get_sub_field( 'more_url' ), '#browse-by-product' ) ); ?>"><?php echo esc_html( $m11_more ); ?></a><?php endif; ?>
                        </div>
                    </article>
                        <?php
                    endwhile;
                    ?>
                </div>
                <?php endif; ?>
            </div>
        </section>
