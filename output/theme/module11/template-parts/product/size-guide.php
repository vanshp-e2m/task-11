<?php
/**
 * Product size guide (section#size-guide, variation B) -- transplanted from
 * spec/fragments/product-feather-blades/02-size-guide.html.
 * Rendered by single-m11_product.php only when has_size_guide is on and size_rows exist.
 *
 * - One verbatim <tr> prototype per size_rows row; is_selected -> class="is-selected" plus
 *   the fragment's <span class="sel-mark" aria-label="selected"></span> marker.
 * - Column headers = size_col_1..5; each empty one falls back to the drawn default
 *   ("Blade Width", "Part number", "Blade length", "Compatible handle", "Typical
 *   application"). Still hardcoded: the sel-mark aria-label "selected" (translatable).
 * - Section id is fixed ('size-guide') because the template-generated tab bar targets it.
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

$m11_pid     = isset( $args['product_id'] ) ? (int) $args['product_id'] : get_the_ID();
$m11_heading = (string) get_field( 'size_guide_heading', $m11_pid );
$m11_badge   = (string) get_field( 'size_guide_badge', $m11_pid );
$m11_rows    = get_field( 'size_rows', $m11_pid );
$m11_cols    = array();
foreach ( array( __( 'Blade Width', 'module11' ), __( 'Part number', 'module11' ), __( 'Blade length', 'module11' ), __( 'Compatible handle', 'module11' ), __( 'Typical application', 'module11' ) ) as $m11_c => $m11_default ) {
	$m11_value  = trim( (string) get_field( 'size_col_' . ( $m11_c + 1 ), $m11_pid ) );
	$m11_cols[] = '' !== $m11_value ? $m11_value : $m11_default;
}

if ( ! is_array( $m11_rows ) || ! $m11_rows ) {
	return;
}
?>
<section class="rs tb" id="size-guide">
            <div class="fx">
                <div class="tb-head">
                    <?php if ( '' !== trim( $m11_heading ) ) : ?>
                    <h2 class="sec-h"><?php echo esc_html( $m11_heading ); ?></h2>
                    <?php endif; ?>
                    <?php if ( '' !== trim( $m11_badge ) ) : ?>
                    <p class="tb-badge"><?php echo esc_html( $m11_badge ); ?></p>
                    <?php endif; ?>
                </div>
                <div class="tb-scroll">
                    <table class="tb-table">
                        <thead>
                            <tr>
                                <?php foreach ( $m11_cols as $m11_col ) : ?>
                                <th scope="col"><?php echo esc_html( $m11_col ); ?></th>
                                <?php endforeach; ?>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ( $m11_rows as $m11_row ) : ?>
                            <?php $m11_sel = ! empty( $m11_row['is_selected'] ); ?>
                            <tr<?php echo $m11_sel ? ' class="is-selected"' : ''; ?>>
                                <th scope="row"><?php echo esc_html( isset( $m11_row['width'] ) ? $m11_row['width'] : '' ); ?><?php if ( $m11_sel ) : ?><span class="sel-mark" aria-label="<?php esc_attr_e( 'selected', 'module11' ); ?>"></span><?php endif; ?></th>
                                <td class="is-part"><?php echo esc_html( isset( $m11_row['part_number'] ) ? $m11_row['part_number'] : '' ); ?></td>
                                <td><?php echo esc_html( isset( $m11_row['length'] ) ? $m11_row['length'] : '' ); ?></td>
                                <td><?php echo esc_html( isset( $m11_row['handle'] ) ? $m11_row['handle'] : '' ); ?></td>
                                <td><?php echo esc_html( isset( $m11_row['application'] ) ? $m11_row['application'] : '' ); ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <hr class="sec-rule">
            </div>
        </section>
