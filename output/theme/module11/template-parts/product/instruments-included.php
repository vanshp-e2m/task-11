<?php
/**
 * Product instruments table (section#instruments-included, variation A) -- transplanted
 * from spec/fragments/product-lawtonelite-skull-base-set/02-instruments-included.html.
 * Rendered by single-m11_product.php only when has_instruments_table is on and
 * instrument_rows exist.
 *
 * - One verbatim <tr> prototype per instrument_rows row; notes_col renders an empty <td>
 *   when blank (fragment rows 03/04/06/11/13/14).
 * - Download link href = instruments_file (PDF); empty -> '#download-parts-list'.
 * - Column headers = instruments_col_1..5; each empty one falls back to the drawn
 *   default ("#", "Instrument", "Part number", "Qty", "Notes", translatable).
 * - Section id fixed ('instruments-included') -- tab bar target.
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
$m11_heading = (string) get_field( 'instruments_heading', $m11_pid );
$m11_badge   = (string) get_field( 'instruments_badge', $m11_pid );
$m11_dl      = (string) get_field( 'instruments_download_label', $m11_pid );
$m11_rows    = get_field( 'instrument_rows', $m11_pid );
$m11_file    = (string) get_field( 'instruments_file', $m11_pid );
$m11_cols    = array();
foreach ( array( __( '#', 'module11' ), __( 'Instrument', 'module11' ), __( 'Part number', 'module11' ), __( 'Qty', 'module11' ), __( 'Notes', 'module11' ) ) as $m11_c => $m11_default ) {
	$m11_value  = trim( (string) get_field( 'instruments_col_' . ( $m11_c + 1 ), $m11_pid ) );
	$m11_cols[] = '' !== $m11_value ? $m11_value : $m11_default;
}

if ( ! is_array( $m11_rows ) || ! $m11_rows ) {
	return;
}
?>
<section class="rs tb" id="instruments-included">
            <div class="fx">
                <div class="tb-head">
                    <?php if ( '' !== trim( $m11_heading ) ) : ?>
                    <h2 class="sec-h"><?php echo esc_html( $m11_heading ); ?></h2>
                    <?php endif; ?>
                    <?php if ( '' !== trim( $m11_badge ) ) : ?>
                    <p class="tb-badge"><?php echo esc_html( $m11_badge ); ?></p><?php endif; ?><?php if ( '' !== trim( $m11_dl ) ) : ?><a class="pbtn pbtn--line tb-dl" href="<?php echo esc_url( $m11_file ? $m11_file : '#download-parts-list' ); ?>"><span class="dl-arrow" aria-hidden="true"></span><?php echo esc_html( $m11_dl ); ?></a><?php endif; ?>
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
                            <tr>
                                <th scope="row"><?php echo esc_html( isset( $m11_row['number'] ) ? $m11_row['number'] : '' ); ?></th>
                                <td><?php echo esc_html( isset( $m11_row['instrument'] ) ? $m11_row['instrument'] : '' ); ?></td>
                                <td class="is-part"><?php echo esc_html( isset( $m11_row['part_number'] ) ? $m11_row['part_number'] : '' ); ?></td>
                                <td><?php echo esc_html( isset( $m11_row['qty'] ) ? $m11_row['qty'] : '' ); ?></td>
                                <td><?php echo esc_html( isset( $m11_row['notes_col'] ) ? $m11_row['notes_col'] : '' ); ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <hr class="sec-rule">
            </div>
        </section>
