<?php
/**
 * Layout: fast_facts
 * Source: resources / fast-facts (spec/fragments/resources/03-fast-facts.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .ff-item prototype in have_rows('fact_items').
 * - title: restricted kses (keeps the editor's <br>); aria-label / alt use the plain text.
 * - Width utilities (w303/w281/w207) are per-item line-wrap widths from the Figma frame; no
 *   field carries them, so the source values are mapped from the row index (items 4+ get
 *   none). HARDCODED class map -- report.
 * - Video link href = video_url (empty -> '#'). Hardcoded a11y string "Play video: %s".
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

$m11_heading  = get_sub_field( 'heading' );
$m11_title_w  = array( 1 => 'w303', 2 => 'w281', 3 => 'w303' );
$m11_cap_w    = array( 1 => 'w281', 2 => 'w281', 3 => 'w207' );
?>
<section<?php echo m11_section_attrs( 'rs ff', 'fast-facts' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_heading ) : ?>
                <h2 class="sec-h2 ff-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php if ( have_rows( 'fact_items' ) ) : ?>
                <div class="ff-grid">
                    <?php
                    while ( have_rows( 'fact_items' ) ) :
                        the_row();
                        $m11_i     = get_row_index();
                        $m11_title = (string) get_sub_field( 'title' );
                        $m11_plain = trim( wp_strip_all_tags( preg_replace( '#<br\s*/?>#i', ' ', $m11_title ) ) );
                        $m11_thumb = get_sub_field( 'video_thumbnail' );
                        $m11_cap   = get_sub_field( 'caption' );
                        ?>
                    <article class="ff-item">
                        <?php if ( $m11_title ) : ?><h3 class="<?php echo esc_attr( trim( 'ff-title ' . ( isset( $m11_title_w[ $m11_i ] ) ? $m11_title_w[ $m11_i ] : '' ) ) ); ?>"><?php echo m11_accent_kses( $m11_title ); // phpcs:ignore WordPress.Security.EscapeOutput ?></h3><?php endif; ?><?php if ( $m11_thumb ) : ?><a class="vid ff-thumb" href="<?php echo esc_url( m11_href( get_sub_field( 'video_url' ), '#' ) ); ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: video title */ __( 'Play video: %s', 'module11' ), $m11_plain ) ); ?>"><?php echo m11_image( $m11_thumb, $m11_plain ? array( 'alt' => $m11_plain ) : array() ); // phpcs:ignore WordPress.Security.EscapeOutput ?><img class="play" src="<?php echo m11_icon_url( 'icon-play-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="53" height="53"></a><?php endif; ?>
                        <?php if ( $m11_cap ) : ?>
                        <p class="<?php echo esc_attr( trim( 'ff-cap ' . ( isset( $m11_cap_w[ $m11_i ] ) ? $m11_cap_w[ $m11_i ] : '' ) ) ); ?>"><?php echo m11_multiline( $m11_cap ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                        <?php endif; ?>
                    </article>
                        <?php
                    endwhile;
                    ?>
                </div>
                <?php endif; ?>
            </div>
        </section>
