<?php
/**
 * Layout: resources_intro
 * Source: resources / resources-intro (spec/fragments/resources/01-resources-intro.html). JS hooks: none.
 *
 * Transplant notes:
 * - intro_ctas: one verbatim .ri-btn prototype; first row = ri-btn--solid, the rest
 *   ri-btn--line (index-derived, as drawn). Label = the row's label field (restricted kses so
 *   the fragment's "downloadable<br>product brochures" break survives), else the link title.
 * - featured_video_thumbnail is above the fold: no lazy loading (fragment has none).
 * - Featured video link href = featured_video_url (empty -> '#'). Hardcoded a11y string
 *   "Play video: %s" (uses featured_quote_attribution).
 * - Decorative .play icon is a theme asset (alt="").
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

$m11_title   = get_sub_field( 'page_title' );
$m11_heading = get_sub_field( 'heading' );
$m11_body    = get_sub_field( 'body' );
$m11_thumb   = get_sub_field( 'featured_video_thumbnail' );
$m11_vurl    = m11_href( get_sub_field( 'featured_video_url' ), '#' );
$m11_quote   = get_sub_field( 'featured_quote' );
$m11_cite    = get_sub_field( 'featured_quote_attribution' );
?>
<section<?php echo m11_section_attrs( 'rs ri', 'resources-intro' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <?php if ( $m11_title ) : ?>
                <h1 class="ri-h1"><?php echo esc_html( $m11_title ); ?></h1>
                <?php endif; ?>
                <div class="ri-card">
                    <div class="ri-copy">
                        <?php if ( $m11_heading ) : ?>
                        <h2 class="ri-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                        <?php endif; ?>
                        <?php if ( $m11_body ) : ?>
                        <p class="ri-body"><?php echo m11_multiline( $m11_body ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                        <?php endif; ?>
                        <?php if ( have_rows( 'intro_ctas' ) ) : ?>
                        <div class="ri-btns"><?php
                        while ( have_rows( 'intro_ctas' ) ) :
                            the_row();
                            $m11_link  = m11_link( get_sub_field( 'url' ) );
                            $m11_label = get_sub_field( 'label' ) ? get_sub_field( 'label' ) : $m11_link['title'];
                            if ( ! $m11_link['url'] || ! $m11_label ) {
                                continue;
                            }
                            ?><a class="<?php echo 1 === get_row_index() ? 'ri-btn ri-btn--solid' : 'ri-btn ri-btn--line'; ?>"<?php echo m11_link_attrs( $m11_link ); // phpcs:ignore WordPress.Security.EscapeOutput ?>><?php echo m11_accent_kses( $m11_label ); // phpcs:ignore WordPress.Security.EscapeOutput ?></a><?php
                        endwhile;
                        ?></div>
                        <?php endif; ?>
                    </div>
                    <?php if ( $m11_thumb || $m11_quote || $m11_cite ) : ?>
                    <figure class="ri-media"><?php if ( $m11_thumb ) : ?><a class="vid ri-vid" href="<?php echo esc_url( $m11_vurl ); ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: video subject */ __( 'Play video: %s', 'module11' ), $m11_cite ) ); ?>"><?php echo m11_image( $m11_thumb, array( 'loading' => false ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?><img class="play" src="<?php echo m11_icon_url( 'icon-play-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="53" height="53"></a><?php endif; ?>
                        <?php if ( $m11_quote ) : ?>
                        <blockquote class="ri-quote">
                            <p><?php echo m11_multiline( $m11_quote ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                        </blockquote>
                        <?php endif; ?>
                        <?php if ( $m11_cite ) : ?>
                        <figcaption class="ri-cite"><?php echo esc_html( $m11_cite ); ?></figcaption>
                        <?php endif; ?>
                    </figure>
                    <?php endif; ?>
                </div>
            </div>
        </section>
