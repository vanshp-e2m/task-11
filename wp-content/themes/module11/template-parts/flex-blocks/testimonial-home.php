<?php
/**
 * Layout: testimonial_home
 * Source: home / testimonials (spec/fragments/home/05-testimonials.html). JS hooks: none.
 *
 * Transplant notes:
 * - One verbatim .ts-card prototype in have_rows('testimonial_cards'); ts-card--N is the
 *   position modifier the source CSS keys on (1-based row index).
 * - featured_quote (textarea): line breaks render as the fragment's <br class="d-only">.
 * - rest (textarea): line breaks render as plain <br> (fragment shape).
 * - thumbnail alt = the attachment's alt (fragment: the expert's name).
 * - Links: mobile_cta_url (empty -> '#clinical-experts'), more_link_url (empty ->
 *   '#more-testimonials'); per-card watch_url drives BOTH the thumbnail link and
 *   "Watch now" (empty -> '#').
 * - Decorative .ts-play icon and the four <hr class="ts-rule…"> dividers kept verbatim.
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
$m11_intro   = get_sub_field( 'intro' );
$m11_mcta    = get_sub_field( 'mobile_cta_label' );
$m11_quote   = get_sub_field( 'featured_quote' );
$m11_attr    = get_sub_field( 'featured_quote_attribution' );
$m11_more    = get_sub_field( 'more_link_label' );
?>
<section<?php echo m11_section_attrs( 'ts rs', 'testimonials' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="ts-head">
                    <?php if ( $m11_heading ) : ?>
                    <h2 class="ts-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                    <?php endif; ?>
                    <?php if ( $m11_intro ) : ?>
                    <p class="ts-intro"><?php echo m11_multiline( $m11_intro ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                </div>
                <?php
                if ( have_rows( 'testimonial_cards' ) ) :
                    while ( have_rows( 'testimonial_cards' ) ) :
                        the_row();
                        $m11_name  = get_sub_field( 'name' );
                        $m11_role  = get_sub_field( 'role' );
                        $m11_rest  = get_sub_field( 'rest' );
                        $m11_watch = get_sub_field( 'watch_link_label' );
                        $m11_wurl  = m11_href( get_sub_field( 'watch_url' ), '#' );
                        ?>
                <article class="ts-card ts-card--<?php echo esc_attr( get_row_index() ); ?>"><a class="ts-thumb" href="<?php echo esc_url( $m11_wurl ); ?>"><?php echo m11_image( get_sub_field( 'thumbnail' ), array( 'class' => 'ts-img' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><img class="ts-play" src="<?php echo m11_icon_url( 'icon-play-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="53" height="53"></a>
                    <div class="ts-bio">
                        <?php if ( $m11_name ) : ?>
                        <p class="ts-name"><?php echo esc_html( $m11_name ); ?></p>
                        <?php endif; ?>
                        <?php if ( $m11_role ) : ?>
                        <p class="ts-role"><?php echo esc_html( $m11_role ); ?></p>
                        <?php endif; ?>
                        <?php if ( $m11_rest ) : ?>
                        <p class="ts-rest"><?php echo m11_multiline( $m11_rest ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p><?php endif; ?><?php if ( $m11_watch ) : ?><a class="ts-watch" href="<?php echo esc_url( $m11_wurl ); ?>"><?php echo esc_html( $m11_watch ); ?></a><?php endif; ?>
                    </div>
                </article><?php
                    endwhile;
                endif;
                ?><?php if ( $m11_mcta ) : ?><a class="ts-mcta m-only" href="<?php echo esc_url( m11_href( get_sub_field( 'mobile_cta_url' ), '#clinical-experts' ) ); ?>"><?php echo esc_html( $m11_mcta ); ?></a><?php endif; ?>
                <hr class="ts-rule ts-rule--top">
                <?php if ( $m11_quote ) : ?>
                <blockquote class="ts-quote">
                    <p><?php echo m11_multiline( $m11_quote, 'd-only' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                </blockquote>
                <?php endif; ?>
                <?php if ( $m11_attr ) : ?>
                <p class="ts-attr"><?php echo esc_html( $m11_attr ); ?></p>
                <?php endif; ?>
                <hr class="ts-rule ts-rule--l d-only">
                <hr class="ts-rule ts-rule--r d-only"><?php if ( $m11_more ) : ?><a class="ts-more" href="<?php echo esc_url( m11_href( get_sub_field( 'more_link_url' ), '#more-testimonials' ) ); ?>"><?php echo esc_html( $m11_more ); ?></a><?php endif; ?>
                <hr class="ts-rule ts-rule--bottom m-only">
            </div>
        </section>
