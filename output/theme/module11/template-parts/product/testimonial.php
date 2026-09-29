<?php
/**
 * Product testimonial (section#testimonial) -- transplanted from
 * spec/fragments/product-feather-blades/04-testimonial.html (identical shape on all 3).
 *
 * - testimonial_quote (textarea) -> .tq-quote p (line breaks as <br>).
 * - testimonial_name / testimonial_dept -> .tq-name / .tq-dept (placeholder copy seeded
 *   verbatim, per plan).
 * - .tq-ctas: the SAME `buttons` rows as the overview (plan: one field rendered twice).
 * - No quote, name, dept and buttons -> no section.
 *
 * Args: product_id (int).
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

$m11_pid   = isset( $args['product_id'] ) ? (int) $args['product_id'] : get_the_ID();
$m11_quote = (string) get_field( 'testimonial_quote', $m11_pid );
$m11_name  = (string) get_field( 'testimonial_name', $m11_pid );
$m11_dept  = (string) get_field( 'testimonial_dept', $m11_pid );
$m11_ctas  = m11_product_ctas_html( $m11_pid );

if ( '' === trim( $m11_quote . $m11_name . $m11_dept ) && '' === $m11_ctas ) {
	return;
}
?>
<section class="rs tq" id="testimonial">
            <div class="fx">
                <?php if ( '' !== trim( $m11_quote . $m11_name . $m11_dept ) ) : ?>
                <figure class="tq-fig">
                    <?php if ( '' !== trim( $m11_quote ) ) : ?>
                    <blockquote class="tq-quote">
                        <p><?php echo m11_multiline( $m11_quote ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    </blockquote>
                    <?php endif; ?>
                    <?php if ( '' !== trim( $m11_name . $m11_dept ) ) : ?>
                    <figcaption class="tq-cite"><?php if ( '' !== trim( $m11_name ) ) : ?><span class="tq-name"><?php echo esc_html( $m11_name ); ?></span><?php endif; ?><?php if ( '' !== trim( $m11_dept ) ) : ?><span class="tq-dept"><?php echo esc_html( $m11_dept ); ?></span><?php endif; ?></figcaption>
                    <?php endif; ?>
                </figure>
                <?php endif; ?>
                <?php if ( $m11_ctas ) : ?>
                <div class="tq-ctas"><?php echo $m11_ctas; // phpcs:ignore WordPress.Security.EscapeOutput -- escaped in m11_button(). ?></div>
                <?php endif; ?>
            </div>
        </section>
