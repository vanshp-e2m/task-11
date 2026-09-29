<?php
/**
 * Layout: procedure_band
 * Source: home / procedure-band (spec/fragments/home/04-procedure-band.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .pb-item prototype in have_rows('procedure_items').
 * - Position modifiers: the source CSS keys icon size/offsets on pb-item--tumor /
 *   --aneurysm / --endo (1st/2nd/3rd item). No field carries them, so they are mapped from
 *   the row index (rows 4+ get no modifier). HARDCODED class map -- report.
 * - Links: closing_cta_url (empty -> '#supported-procedures'), per-row view_url / more_url
 *   (empty -> '#'; the fragment's per-row hashes were all BROKEN).
 * - .pb-btn keeps its trailing decorative arrow icon (theme asset, alt="").
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
$m11_closing = get_sub_field( 'closing_text' );
$m11_cta     = get_sub_field( 'closing_cta_label' );
$m11_mods    = array( 1 => 'pb-item--tumor', 2 => 'pb-item--aneurysm', 3 => 'pb-item--endo' );
?>
<section<?php echo m11_section_attrs( 'pb rs', 'procedure-band' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_heading ) : ?>
                <h2 class="pb-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php
                if ( have_rows( 'procedure_items' ) ) :
                    while ( have_rows( 'procedure_items' ) ) :
                        the_row();
                        $m11_i     = get_row_index();
                        $m11_class = trim( 'pb-item ' . ( isset( $m11_mods[ $m11_i ] ) ? $m11_mods[ $m11_i ] : '' ) );
                        $m11_title = get_sub_field( 'title' );
                        $m11_view  = get_sub_field( 'view_label' );
                        $m11_more  = get_sub_field( 'more_label' );
                        ?>
                <div class="<?php echo esc_attr( $m11_class ); ?>"><?php echo m11_image( get_sub_field( 'icon' ), array( 'class' => 'pb-icon', 'alt' => '' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                    <div class="pb-txt">
                        <?php if ( $m11_title ) : ?><h3><?php echo esc_html( $m11_title ); ?></h3><?php endif; ?><?php if ( $m11_view ) : ?><a class="pb-view" href="<?php echo esc_url( m11_href( get_sub_field( 'view_url' ), '#' ) ); ?>"><?php echo esc_html( $m11_view ); ?></a><?php endif; ?><?php if ( $m11_more ) : ?><a class="pb-more" href="<?php echo esc_url( m11_href( get_sub_field( 'more_url' ), '#' ) ); ?>"><?php echo esc_html( $m11_more ); ?></a><?php endif; ?>
                    </div>
                </div>
                        <?php
                    endwhile;
                endif;
                ?>
                <?php if ( $m11_closing ) : ?><p class="pb-closing"><?php echo esc_html( $m11_closing ); ?></p><?php endif; ?><?php if ( $m11_cta ) : ?><a class="pb-btn" href="<?php echo esc_url( m11_href( get_sub_field( 'closing_cta_url' ), '#supported-procedures' ) ); ?>"><span><?php echo esc_html( $m11_cta ); ?></span><img src="<?php echo m11_icon_url( 'icon-arrow-down.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="12" height="14"></a><?php endif; ?>
            </div>
        </section>
