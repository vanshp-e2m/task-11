<?php
/**
 * Layout: about_stats
 * Source: home / about-stats (spec/fragments/home/06-about-stats.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .ab-stat prototype in have_rows('stats'); ab-stat--N (1-based index) is
 *   the position modifier the source CSS keys on; the card colour alternates by index
 *   exactly as drawn (odd = ab-card--blue, even = ab-card--sky).
 * - label (textarea): line breaks render as the fragment's plain <br>.
 * - Decorative <span class="ab-panel" aria-hidden="true"></span> kept verbatim.
 * - cta_label href = cta_url; empty -> home_url( '/about-us/' ) (the Elementor About page).
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
$m11_cta     = get_sub_field( 'cta_label' );
?>
<section<?php echo m11_section_attrs( 'ab rs', 'about-stats' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_heading ) : ?>
                <h2 class="ab-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php if ( $m11_body ) : ?>
                <p class="ab-p"><?php echo m11_multiline( $m11_body ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                <?php endif; ?>
                <?php if ( have_rows( 'stats' ) ) : ?>
                <div class="ab-stats">
                    <?php
                    while ( have_rows( 'stats' ) ) :
                        the_row();
                        $m11_i      = get_row_index();
                        $m11_number = get_sub_field( 'number' );
                        $m11_label  = get_sub_field( 'label' );
                        ?>
                    <div class="ab-stat ab-stat--<?php echo esc_attr( $m11_i ); ?>">
                        <div class="ab-card <?php echo 0 === $m11_i % 2 ? 'ab-card--sky' : 'ab-card--blue'; ?>"><?php if ( $m11_number ) : ?><span class="ab-num"><?php echo esc_html( $m11_number ); ?></span><?php endif; ?><?php if ( $m11_label ) : ?><span class="ab-label"><?php echo m11_multiline( $m11_label ); // phpcs:ignore WordPress.Security.EscapeOutput ?></span><?php endif; ?></div><span class="ab-panel" aria-hidden="true"></span>
                    </div>
                        <?php
                    endwhile;
                    ?>
                </div><?php endif; ?><?php if ( $m11_cta ) : ?><a class="ab-btn" href="<?php echo esc_url( m11_href( get_sub_field( 'cta_url' ), home_url( '/about-us/' ) ) ); ?>"><?php echo esc_html( $m11_cta ); ?></a><?php endif; ?>
            </div>
        </section>
