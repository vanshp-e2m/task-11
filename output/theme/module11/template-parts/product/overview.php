<?php
/**
 * Product overview (section#product-overview) -- transplanted from the RICHEST variant,
 * spec/fragments/product-feather-blades/01-product-overview.html (pill + size selector +
 * table caption). Variant deltas are field-driven: no pill when family_pill is empty
 * (Sugita), no .pd-select unless has_size_guide + size_rows (Feather Blades only), no
 * <caption> when spec_caption is empty (LawtonElite), thumbnails typed image / video /
 * placeholder (LawtonElite real thumbs vs FPO buttons).
 *
 * Sources of each node:
 * - h1.pd-h1: Site Settings `product_page_kicker` (plan static_content page_kicker).
 * - .crumbs: generated (plan static_content breadcrumbs): Products page -> product_category
 *   term ancestry -> current title. DROPPED: the fragment's intermediate "By Category" and
 *   "Product Families" / "Instrumentation Sets" crumbs have no data source (not terms, not
 *   pages) -- only real terms render. Term crumbs link to the Products page filtered by
 *   that category.
 * - .pd-gallery img: gallery_image (above the fold -> not lazy).
 * - .pd-thumbs: gallery_thumbnails rows; placeholder rows render the fragment's
 *   "FPO IMAGE" button (plan static_content fallback label); video rows render the play
 *   button, video_url exposed as data-video-url (no player in the design); image rows are
 *   "Show image N" buttons. HARDCODED a11y: "Show image %d", "Play product video".
 * - .pd-facts / .pd-model / .pd-part: m11_strong_runs() -- the editor marks the bold run
 *   with <strong> (e.g. "<strong>Quick Facts: </strong>35+ years…",
 *   "Part no.: <strong>FB-0480</strong> • Available in 6 sizes"); every run gets the
 *   fragment's s12/s14 class. Seed content must carry those <strong> markers.
 * - .pd-tags: procedure terms (plan static_content tags.label).
 * - .pd-size options: derived from size_rows widths; `selected` = the is_selected row
 *   (plan static_content size_options.label).
 * - .pd-ctas: shared `buttons` (m11_product_ctas_html()).
 * - .pd-tabs: m11_product_tabs() (plan static_content product_tabs). The design marks the
 *   SECOND tab .is-current / aria-current="true" on every variant -- reproduced by
 *   position. Overview target fixed to #product-overview.
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

$m11_pid = isset( $args['product_id'] ) ? (int) $args['product_id'] : get_the_ID();

$m11_kicker   = m11_get_setting( 'product_page_kicker' );
$m11_title    = get_the_title( $m11_pid );
$m11_gallery  = (int) get_field( 'gallery_image', $m11_pid );
$m11_thumbs   = get_field( 'gallery_thumbnails', $m11_pid );
$m11_facts    = (string) get_field( 'quick_facts', $m11_pid );
$m11_pill     = (string) get_field( 'family_pill', $m11_pid );
$m11_model    = (string) get_field( 'model_line', $m11_pid );
$m11_desc     = (string) get_field( 'description', $m11_pid );
$m11_caption  = (string) get_field( 'spec_caption', $m11_pid );
$m11_specs    = get_field( 'spec_rows', $m11_pid );
$m11_has_size = get_field( 'has_size_guide', $m11_pid ) && get_field( 'size_rows', $m11_pid );
$m11_sizes    = $m11_has_size ? get_field( 'size_rows', $m11_pid ) : array();
$m11_sel_h    = (string) get_field( 'size_selector_label', $m11_pid );
$m11_part     = (string) get_field( 'size_selector_part_no', $m11_pid );
$m11_procs    = get_the_terms( $m11_pid, 'procedure' );
$m11_procs    = ( $m11_procs && ! is_wp_error( $m11_procs ) ) ? $m11_procs : array();
$m11_ctas     = m11_product_ctas_html( $m11_pid );
$m11_tabs     = m11_product_tabs( $m11_pid );

// Breadcrumb trail.
$m11_products_url = m11_page_url( 'products' );
$m11_crumbs       = array();
if ( $m11_products_url ) {
	$m11_crumbs[] = array( get_the_title( get_page_by_path( 'products' ) ), $m11_products_url );
}
$m11_cat = m11_first_term( $m11_pid, 'product_category' );
if ( $m11_cat ) {
	$m11_chain = array_reverse( get_ancestors( $m11_cat->term_id, 'product_category', 'taxonomy' ) );
	$m11_chain[] = $m11_cat->term_id;
	foreach ( $m11_chain as $m11_term_id ) {
		$m11_term = get_term( $m11_term_id, 'product_category' );
		if ( $m11_term && ! is_wp_error( $m11_term ) ) {
			$m11_crumbs[] = array(
				$m11_term->name,
				$m11_products_url ? add_query_arg( 'f_category[]', $m11_term->slug, $m11_products_url ) : get_term_link( $m11_term ),
			);
		}
	}
}
?>
<section class="rs pd" id="product-overview">
            <div class="fx">
                <?php if ( $m11_kicker ) : ?>
                <h1 class="pd-h1"><?php echo esc_html( $m11_kicker ); ?></h1>
                <?php endif; ?>
                <div class="pd-panel">
                    <nav class="crumbs" aria-label="<?php esc_attr_e( 'Breadcrumb', 'module11' ); ?>">
                        <ol>
                            <?php foreach ( $m11_crumbs as $m11_crumb ) : ?>
                            <?php if ( ! is_wp_error( $m11_crumb[1] ) ) : ?>
                            <li><a href="<?php echo esc_url( $m11_crumb[1] ); ?>"><?php echo esc_html( $m11_crumb[0] ); ?></a></li>
                            <?php endif; ?>
                            <?php endforeach; ?>
                            <li aria-current="page"><?php echo esc_html( $m11_title ); ?></li>
                        </ol>
                    </nav>
                    <div class="pd-cols">
                        <div class="pd-media">
                            <?php if ( $m11_gallery ) : ?>
                            <div class="pd-gallery"><?php echo m11_image( $m11_gallery, array( 'loading' => false ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?></div>
                            <?php endif; ?>
                            <?php if ( is_array( $m11_thumbs ) && $m11_thumbs ) : ?>
                            <ul class="pd-thumbs">
                                <?php
                                $m11_img_n = 0;
                                foreach ( $m11_thumbs as $m11_thumb ) :
                                    $m11_type = isset( $m11_thumb['type'] ) ? $m11_thumb['type'] : 'placeholder';
                                    if ( 'image' === $m11_type && ! empty( $m11_thumb['image'] ) ) :
                                        ++$m11_img_n;
                                        ?>
                                <li><button class="thumb" type="button" aria-label="<?php echo esc_attr( sprintf( /* translators: %d: image number */ __( 'Show image %d', 'module11' ), $m11_img_n ) ); ?>"><?php echo m11_image( $m11_thumb['image'], array( 'alt' => '', 'loading' => false ), 'medium' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></button></li>
                                    <?php elseif ( 'video' === $m11_type ) : ?>
                                <li><button class="thumb thumb--video" type="button" aria-label="<?php esc_attr_e( 'Play product video', 'module11' ); ?>"<?php echo ! empty( $m11_thumb['video_url'] ) ? ' data-video-url="' . esc_url( $m11_thumb['video_url'] ) . '"' : ''; ?>><img src="<?php echo m11_icon_url( 'icon-play-circle.svg' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>" alt="" width="28" height="28"></button></li>
                                    <?php else : ?>
                                <li><button class="thumb thumb--fpo" type="button"><?php esc_html_e( 'FPO IMAGE', 'module11' ); ?></button></li>
                                        <?php
                                    endif;
                                endforeach;
                                ?>
                            </ul>
                            <?php endif; ?>
                            <hr class="pd-rule">
                            <?php if ( '' !== trim( $m11_facts ) ) : ?>
                            <p class="pd-facts"><?php echo m11_strong_runs( $m11_facts, 's12' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                            <?php endif; ?>
                        </div>
                        <div class="pd-info">
                            <?php if ( '' !== trim( $m11_pill ) ) : ?>
                            <p class="pd-pill"><?php echo esc_html( $m11_pill ); ?></p>
                            <?php endif; ?>
                            <h2 class="pd-title"><?php echo esc_html( $m11_title ); ?></h2>
                            <?php if ( '' !== trim( $m11_model ) ) : ?>
                            <p class="pd-model"><?php echo m11_strong_runs( $m11_model, 's14' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                            <?php endif; ?>
                            <?php if ( $m11_procs ) : ?>
                            <ul class="pd-tags">
                                <?php foreach ( $m11_procs as $m11_proc ) : ?>
                                <li><?php echo esc_html( $m11_proc->name ); ?></li>
                                <?php endforeach; ?>
                            </ul>
                            <?php endif; ?>
                            <?php if ( '' !== trim( $m11_desc ) ) : ?>
                            <p class="pd-desc"><?php echo m11_multiline( $m11_desc ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                            <?php endif; ?>
                            <?php if ( $m11_has_size ) : ?>
                            <div class="pd-select"><?php if ( '' !== trim( $m11_sel_h ) ) : ?><label class="pd-select-h" for="b-size"><?php echo esc_html( $m11_sel_h ); ?></label><?php endif; ?>
                                <div class="pd-select-row"><select class="pd-size selectish" id="b-size" name="size">
                                        <?php foreach ( $m11_sizes as $m11_size ) : ?>
                                        <?php if ( ! empty( $m11_size['width'] ) ) : ?>
                                        <option<?php echo ! empty( $m11_size['is_selected'] ) ? ' selected' : ''; ?>><?php echo esc_html( $m11_size['width'] ); ?></option>
                                        <?php endif; ?>
                                        <?php endforeach; ?>
                                    </select>
                                    <?php if ( '' !== trim( $m11_part ) ) : ?>
                                    <p class="pd-part"><?php echo m11_strong_runs( $m11_part, 's14' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                                    <?php endif; ?>
                                </div>
                            </div>
                            <?php endif; ?>
                            <?php if ( is_array( $m11_specs ) && $m11_specs ) : ?>
                            <div class="pd-chart">
                                <table class="pd-spec">
                                    <?php if ( '' !== trim( $m11_caption ) ) : ?>
                                    <caption><?php echo esc_html( $m11_caption ); ?></caption>
                                    <?php endif; ?>
                                    <tbody>
                                        <?php foreach ( $m11_specs as $m11_spec ) : ?>
                                        <tr>
                                            <th scope="row"><?php echo esc_html( isset( $m11_spec['label'] ) ? $m11_spec['label'] : '' ); ?></th>
                                            <td><?php echo esc_html( isset( $m11_spec['value'] ) ? $m11_spec['value'] : '' ); ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                            <?php endif; ?>
                            <?php if ( $m11_ctas ) : ?>
                            <div class="pd-ctas"><?php echo $m11_ctas; // phpcs:ignore WordPress.Security.EscapeOutput -- escaped in m11_button(). ?></div>
                            <?php endif; ?>
                        </div>
                    </div>
                </div>
                <?php if ( count( $m11_tabs ) > 1 ) : ?>
                <nav class="pd-tabs" aria-label="<?php esc_attr_e( 'Product sections', 'module11' ); ?>">
                    <ul>
                        <?php foreach ( $m11_tabs as $m11_t => $m11_tab ) : ?>
                        <?php if ( 1 === $m11_t ) : ?>
                        <li><a class="tab is-current" href="<?php echo esc_attr( $m11_tab['href'] ); ?>" aria-current="true"><?php echo esc_html( $m11_tab['label'] ); ?></a></li>
                        <?php else : ?>
                        <li><a class="tab" href="<?php echo esc_attr( $m11_tab['href'] ); ?>"><?php echo esc_html( $m11_tab['label'] ); ?></a></li>
                        <?php endif; ?>
                        <?php endforeach; ?>
                    </ul>
                </nav>
                <?php endif; ?>
            </div>
        </section>
