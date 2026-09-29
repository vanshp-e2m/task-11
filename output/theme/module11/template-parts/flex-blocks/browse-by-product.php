<?php
/**
 * Layout: browse_by_product
 * Source: products / browse-by-product (spec/fragments/products/03-browse-by-product.html). JS hooks: none.
 *
 * Editable (ACF): heading, lead, filters_heading, filters_subheading.
 * Query output (plan static_content): result count, active chips, product tiles
 * (template-parts/tiles/product-tile.php), pager -- from m11_products_query().
 *
 * Transplant notes:
 * - Filter fieldsets: one verbatim .fl-group prototype per taxonomy (product_category,
 *   product_configuration, procedure); legend = taxonomy singular label (CSS uppercases
 *   .fl-h), checkbox labels = term names, ids keep the fragment's "pf-{slug}" pattern.
 *   Input names are f_category[] / f_configuration[] / f_procedure[] (the fragment's
 *   category/configuration/procedure collide with WP query vars).
 * - The fragment's filter form has no submit control (decorative in the source); to apply
 *   checkbox changes assets/js/m11-filters.js submits .fl-form on change. The search form carries the current filters as hidden inputs.
 * - Pager: "<Prev" / numbers / "Next>" built from the query; disabled ends keep the
 *   fragment's aria-disabled="true" and point at the current page.
 * - Self-target form actions / "Clear all" use this row's sec_id hash (fragment:
 *   #browse-by-product) -- nothing when sec_id is empty.
 * - HARDCODED UI strings (no fields in the plan, translatable): "Clear all filters",
 *   "Search products" (sr label), search placeholder, "Search", "product(s) found",
 *   "Remove filter: %s", "Clear all", "<Prev", "Next>", aria-labels "Filter products" /
 *   "Product pages".
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

$m11_heading   = get_sub_field( 'heading' );
$m11_lead      = get_sub_field( 'lead' );
$m11_fheading  = get_sub_field( 'filters_heading' );
$m11_fsub      = get_sub_field( 'filters_subheading' );
$m11_hash      = m11_section_hash();
$m11_action    = get_permalink() . $m11_hash;
$m11_query     = m11_products_query();
$m11_found     = (int) $m11_query->found_posts;
$m11_pages     = max( 1, (int) $m11_query->max_num_pages );
$m11_current   = min( m11_filter_page(), $m11_pages );
$m11_active    = m11_filter_active_terms( 'products' );
$m11_search    = m11_filter_text( 'f_q' );
$m11_fieldsets = m11_filter_map( 'products' );
?>
<section<?php echo m11_section_attrs( 'rs pbp', 'browse-by-product' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="pbp-head">
                    <?php if ( $m11_heading ) : ?>
                    <h2 class="pbp-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                    <?php endif; ?>
                    <?php if ( $m11_lead ) : ?>
                    <p class="pbp-lead"><?php echo m11_multiline( $m11_lead ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                </div>
                <div class="pbp-layout">
                    <aside class="pb-filters" aria-label="<?php esc_attr_e( 'Filter products', 'module11' ); ?>">
                        <form class="fl-form" action="<?php echo esc_url( $m11_action ); ?>">
                            <div class="pbf-head">
                                <?php if ( $m11_fheading ) : ?>
                                <h3 class="pbf-h"><?php echo esc_html( $m11_fheading ); ?></h3>
                                <?php endif; ?>
                                <?php if ( $m11_fsub ) : ?>
                                <p class="pbf-sub"><?php echo esc_html( $m11_fsub ); ?></p><?php endif; ?><span class="pbf-chev m-only" aria-hidden="true"></span>
                            </div>
                            <?php
                            foreach ( $m11_fieldsets as $m11_key => $m11_tax ) :
                                $m11_terms = m11_filter_terms( $m11_tax );
                                if ( ! $m11_terms ) {
                                    continue;
                                }
                                $m11_selected = m11_filter_values( $m11_key );
                                ?>
                            <fieldset class="fl-group">
                                <legend class="fl-h"><?php echo esc_html( m11_filter_legend( $m11_tax ) ); ?></legend>
                                <ul class="fl-list">
                                    <?php foreach ( $m11_terms as $m11_term ) : ?>
                                    <li class="fl-row"><input class="fl-box" type="checkbox" id="<?php echo esc_attr( 'pf-' . $m11_term->slug ); ?>" name="<?php echo esc_attr( $m11_key ); ?>[]" value="<?php echo esc_attr( $m11_term->slug ); ?>"<?php checked( in_array( $m11_term->slug, $m11_selected, true ) ); ?>><label class="fl-label" for="<?php echo esc_attr( 'pf-' . $m11_term->slug ); ?>"><?php echo esc_html( $m11_term->name ); ?></label></li>
                                    <?php endforeach; ?>
                                </ul>
                            </fieldset><?php endforeach; ?><?php if ( '' !== $m11_search ) : ?><input type="hidden" name="f_q" value="<?php echo esc_attr( $m11_search ); ?>"><?php endif; ?><button class="fl-clear" type="reset"><?php esc_html_e( 'Clear all filters', 'module11' ); ?></button>
                        </form>
                    </aside>
                    <div class="pbp-results">
                        <div class="pb-tools">
                            <form class="pb-search" role="search" action="<?php echo esc_url( $m11_action ); ?>"><label class="visually-hidden" for="pb-q"><?php esc_html_e( 'Search products', 'module11' ); ?></label><input class="pb-q" id="pb-q" type="search" name="f_q" value="<?php echo esc_attr( $m11_search ); ?>" placeholder="<?php esc_attr_e( 'Search products, part numbers, or instrument names', 'module11' ); ?>"><?php foreach ( $m11_fieldsets as $m11_key => $m11_tax ) : foreach ( m11_filter_values( $m11_key ) as $m11_slug ) : ?><input type="hidden" name="<?php echo esc_attr( $m11_key ); ?>[]" value="<?php echo esc_attr( $m11_slug ); ?>"><?php endforeach; endforeach; ?><button class="pb-go" type="submit"><?php esc_html_e( 'Search', 'module11' ); ?></button></form>
                            <hr class="pb-line">
                            <p class="pb-count" aria-live="polite"><strong class="s20"><?php echo esc_html( number_format_i18n( $m11_found ) . ' ' ); ?></strong><span class="s20"><?php echo esc_html( _n( 'product found', 'products found', $m11_found, 'module11' ) ); ?></span></p>
                            <?php if ( $m11_active ) : ?>
                            <div class="pb-active"><?php foreach ( $m11_active as $m11_term ) : ?><button class="chip" type="button" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: filter term */ __( 'Remove filter: %s', 'module11' ), $m11_term->name ) ); ?>"><?php echo esc_html( $m11_term->name ); ?><span class="chip-x" aria-hidden="true"></span></button><?php endforeach; ?><a class="pb-clear-all" href="<?php echo esc_url( get_permalink() . $m11_hash ); ?>"><?php esc_html_e( 'Clear all', 'module11' ); ?></a></div>
                            <?php endif; ?>
                        </div>
                        <?php if ( $m11_query->have_posts() ) : ?>
                        <ul class="tiles">
                            <?php
                            while ( $m11_query->have_posts() ) :
                                $m11_query->the_post();
                                get_template_part(
                                    'template-parts/tiles/product-tile',
                                    null,
                                    array(
                                        'product_id' => get_the_ID(),
                                        'context'    => 'browse',
                                    )
                                );
                            endwhile;
                            wp_reset_postdata();
                            ?>
                        </ul>
                        <nav class="pager" aria-label="<?php esc_attr_e( 'Product pages', 'module11' ); ?>">
                            <ul class="pager-list">
                                <li><a class="pg pg--nav" href="<?php echo esc_url( m11_listing_url( array( 'f_page' => $m11_current > 1 ? $m11_current - 1 : null ), $m11_hash ) ); ?>"<?php echo $m11_current <= 1 ? ' aria-disabled="true"' : ''; ?>><?php esc_html_e( '<Prev', 'module11' ); ?></a></li>
                                <?php for ( $m11_n = 1; $m11_n <= $m11_pages; $m11_n++ ) : ?>
                                <li><a class="pg pg--num" href="<?php echo esc_url( m11_listing_url( array( 'f_page' => $m11_n > 1 ? $m11_n : null ), $m11_hash ) ); ?>"<?php echo $m11_n === $m11_current ? ' aria-current="page"' : ''; ?>><?php echo esc_html( number_format_i18n( $m11_n ) ); ?></a></li>
                                <?php endfor; ?>
                                <li><a class="pg pg--nav" href="<?php echo esc_url( m11_listing_url( array( 'f_page' => $m11_current < $m11_pages ? $m11_current + 1 : ( $m11_current > 1 ? $m11_current : null ) ), $m11_hash ) ); ?>"<?php echo $m11_current >= $m11_pages ? ' aria-disabled="true"' : ''; ?>><?php esc_html_e( 'Next>', 'module11' ); ?></a></li>
                            </ul>
                        </nav>
                        <?php endif; ?>
                    </div>
                </div>
                <hr class="rule pbp-end m-only">
            </div>
        </section>
