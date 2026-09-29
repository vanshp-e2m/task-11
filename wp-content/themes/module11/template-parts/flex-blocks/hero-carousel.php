<?php
/**
 * Layout: hero_carousel
 * Source: home / hero-carousel (spec/fragments/home/01-hero-carousel.html). JS hooks: none.
 *
 * Transplant notes:
 * - hero-card--N / hero-btn--solid|--line are position modifiers the source CSS keys on;
 *   derived from the row index (1-based card number; first CTA solid, the rest line).
 * - First card image is the LCP image: no loading attr (fragment: card 1 has none, card 2
 *   has loading="lazy") -- house rule "not lazy on the hero".
 * - .hero-dots: one <i> per real hero card (decision_record q4 -- dots follow the real
 *   slide count), first gets .is-on. Source drew 3 dots for 2 cards.
 * - browse_link_label href = browse_link_url; empty -> the fragment's '#procedure-band'.
 * - Hardcoded a11y string: aria-label "View %s" on .hero-arrow (translatable).
 * - Decorative icons (arrow-circle-right, arrow-down) are theme assets, alt="".
 * - lint WARN/ERROR on <img>: images are emitted by wp_get_attachment_image() (house rule),
 *   which the static tag census cannot see.
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

$m11_headline    = get_sub_field( 'headline' );
$m11_browse      = get_sub_field( 'browse_link_label' );
$m11_cards       = get_sub_field( 'hero_cards' );
$m11_cards_count = is_array( $m11_cards ) ? count( $m11_cards ) : 0;
?>
<section<?php echo m11_section_attrs( 'hero rs', 'hero-carousel' ); // phpcs:ignore WordPress.Security.EscapeOutput -- escaped in helper. ?>>
            <div class="fx">
                <?php if ( $m11_headline ) : ?>
                <h1 class="hero-h1"><?php echo m11_accent_kses( $m11_headline ); // phpcs:ignore WordPress.Security.EscapeOutput ?></h1>
                <?php endif; ?>
                <?php
                if ( have_rows( 'hero_cards' ) ) :
                    while ( have_rows( 'hero_cards' ) ) :
                        the_row();
                        $m11_i     = get_row_index();
                        $m11_label = get_sub_field( 'label' );
                        $m11_link  = m11_link( get_sub_field( 'link' ) );
                        ?>
                <div class="hero-card hero-card--<?php echo esc_attr( $m11_i ); ?>"><?php echo m11_image( get_sub_field( 'image' ), array( 'class' => 'hero-img', 'loading' => 1 === $m11_i ? false : 'lazy' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><?php if ( $m11_label ) : ?><span class="hero-pill"><?php echo esc_html( $m11_label ); ?></span><?php endif; ?><?php if ( $m11_link['url'] ) : ?><a class="hero-arrow"<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?> aria-label="<?php echo esc_attr( sprintf( /* translators: %s: hero card label */ __( 'View %s', 'module11' ), $m11_label ? $m11_label : $m11_link['title'] ) ); ?>"><img src="<?php echo m11_icon_url( 'icon-arrow-circle-right.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="55" height="55"></a><?php endif; ?></div>
                        <?php
                    endwhile;
                endif;
                ?>
                <div class="hero-meta"><?php echo m11_text_link( m11_href( get_sub_field( 'browse_link_url' ), '#procedure-band' ), $m11_browse, 'hero-browse', '<img src="' . m11_icon_url( 'icon-arrow-down.svg' ) . '" alt="" width="12" height="14"><span>', '</span>' ); // phpcs:ignore WordPress.Security.EscapeOutput ?><?php if ( $m11_cards_count ) : ?><span class="hero-dots" aria-hidden="true"><?php for ( $m11_d = 1; $m11_d <= $m11_cards_count; $m11_d++ ) : ?><i<?php echo 1 === $m11_d ? ' class="is-on"' : ''; ?>></i><?php endfor; ?></span><?php endif; ?></div>
                <?php if ( have_rows( 'hero_ctas' ) ) : ?>
                <div class="hero-ctas"><?php
                while ( have_rows( 'hero_ctas' ) ) :
                    the_row();
                    $m11_link  = m11_link( get_sub_field( 'url' ) );
                    $m11_label = get_sub_field( 'label' ) ? get_sub_field( 'label' ) : $m11_link['title'];
                    if ( ! $m11_link['url'] || ! $m11_label ) {
                        continue;
                    }
                    ?><a class="<?php echo 1 === get_row_index() ? 'hero-btn hero-btn--solid' : 'hero-btn hero-btn--line'; ?>"<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo esc_html( $m11_label ); ?></a><?php
                endwhile;
                ?></div>
                <?php endif; ?>
            </div>
        </section>
