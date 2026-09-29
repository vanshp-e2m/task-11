<?php
/**
 * Layout: sh_resource_results (rep-only)
 * Source: sales-hub-resource-library / resource-results
 * (spec/fragments/sales-hub-resource-library/02-resource-results.html). JS hooks: none.
 *
 * The layout has NO content fields (plan: fields [], repeats []) -- everything is query
 * output from m11_resources_query() (plan static_content: result_count, resource_tiles.*).
 *
 * Transplant notes:
 * - Filter fieldsets: one verbatim .fl-group prototype per taxonomy (resource_type,
 *   product_category); legend = taxonomy singular label (CSS uppercases .fl-h); labels =
 *   term names; .fl-count = published m11_resource posts in the term; ids keep the
 *   fragment's "f-{slug}" pattern; names f_type[] / f_category[] (the fragment's
 *   resource_type / product_category collide with the taxonomies' query vars).
 *   DEVIATION: the fragment merges brochures + spec sheets into ONE checkbox
 *   ("Brochures & spec sheets"); rendered from the resource_type taxonomy it becomes one
 *   checkbox per term (Brochure, Spec Sheet, Video).
 * - Sort select: fragment options had no values; value="az|za|newest" added, name f_sort.
 *   The select sits outside both forms in the fragment (kept there); assets/js/m11-filters.js
 *   submits the search form with it (and submits .fl-form on checkbox change).
 * - Tiles: template-parts/tiles/resource-tile.php. No pager (none in the design).
 * - HARDCODED UI strings (no fields, translatable): "Clear all filters", "Search
 *   resources", search placeholder, "Search", "resource(s)", "Remove filter: %s",
 *   "Clear all", "Sort", "Sort: A-Z" / "Sort: Z-A" / "Sort: Newest", aria-label
 *   "Filter resources".
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

if ( m11_section_is_hidden() || ! m11_can_view_sales_hub() ) {
	return;
}

$m11_hash      = m11_section_hash();
$m11_action    = get_permalink() . $m11_hash;
$m11_query     = m11_resources_query();
$m11_found     = (int) $m11_query->found_posts;
$m11_active    = m11_filter_active_terms( 'resources' );
$m11_search    = m11_filter_text( 'f_q' );
$m11_sort      = m11_filter_text( 'f_sort' );
$m11_fieldsets = m11_filter_map( 'resources' );
$m11_sorts     = array(
	'az'     => __( 'Sort: A-Z', 'module11' ),
	'za'     => __( 'Sort: Z-A', 'module11' ),
	'newest' => __( 'Sort: Newest', 'module11' ),
);
?>
<section<?php echo m11_section_attrs( 'rs rl-main', 'resource-results' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="rl-layout">
                    <aside class="rl-filters" aria-label="<?php esc_attr_e( 'Filter resources', 'module11' ); ?>">
                        <form class="fl-form" action="<?php echo esc_url( $m11_action ); ?>">
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
                                    <li class="fl-row"><input class="fl-box" type="checkbox" id="<?php echo esc_attr( 'f-' . $m11_term->slug ); ?>" name="<?php echo esc_attr( $m11_key ); ?>[]" value="<?php echo esc_attr( $m11_term->slug ); ?>"<?php checked( in_array( $m11_term->slug, $m11_selected, true ) ); ?>><label class="fl-label" for="<?php echo esc_attr( 'f-' . $m11_term->slug ); ?>"><?php echo esc_html( $m11_term->name ); ?></label><span class="fl-count"><?php echo esc_html( number_format_i18n( m11_count_posts_in_terms( 'm11_resource', $m11_tax, $m11_term->slug ) ) ); ?></span></li>
                                    <?php endforeach; ?>
                                </ul>
                            </fieldset><?php endforeach; ?><?php if ( '' !== $m11_search ) : ?><input type="hidden" name="f_q" value="<?php echo esc_attr( $m11_search ); ?>"><?php endif; ?><?php if ( '' !== $m11_sort ) : ?><input type="hidden" name="f_sort" value="<?php echo esc_attr( $m11_sort ); ?>"><?php endif; ?><button class="fl-clear" type="reset"><?php esc_html_e( 'Clear all filters', 'module11' ); ?></button>
                        </form>
                    </aside>
                    <div class="rl-results">
                        <div class="rl-tools">
                            <form class="rl-search" role="search" action="<?php echo esc_url( $m11_action ); ?>"><label class="visually-hidden" for="rl-q"><?php esc_html_e( 'Search resources', 'module11' ); ?></label><input class="rl-q" id="rl-q" type="search" name="f_q" value="<?php echo esc_attr( $m11_search ); ?>" placeholder="<?php esc_attr_e( 'Search brochures, spec sheets, videos...', 'module11' ); ?>"><?php foreach ( $m11_fieldsets as $m11_key => $m11_tax ) : foreach ( m11_filter_values( $m11_key ) as $m11_slug ) : ?><input type="hidden" name="<?php echo esc_attr( $m11_key ); ?>[]" value="<?php echo esc_attr( $m11_slug ); ?>"><?php endforeach; endforeach; ?><?php if ( '' !== $m11_sort ) : ?><input type="hidden" name="f_sort" value="<?php echo esc_attr( $m11_sort ); ?>"><?php endif; ?><button class="rl-go" type="submit"><?php esc_html_e( 'Search', 'module11' ); ?></button></form>
                            <hr class="rl-line">
                            <div class="rl-meta">
                                <p class="rl-count" aria-live="polite"><strong class="s20"><?php echo esc_html( number_format_i18n( $m11_found ) . ' ' ); ?></strong><span class="s20"><?php echo esc_html( _n( 'resource', 'resources', $m11_found, 'module11' ) ); ?></span></p>
                                <?php if ( $m11_active ) : ?>
                                <div class="rl-active"><?php foreach ( $m11_active as $m11_term ) : ?><button class="chip" type="button" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: filter term */ __( 'Remove filter: %s', 'module11' ), $m11_term->name ) ); ?>"><?php echo esc_html( $m11_term->name ); ?><span class="chip-x" aria-hidden="true"></span></button><?php endforeach; ?><a class="rl-clear-all" href="<?php echo esc_url( get_permalink() . $m11_hash ); ?>"><?php esc_html_e( 'Clear all', 'module11' ); ?></a></div><?php endif; ?><label class="visually-hidden" for="rl-sort"><?php esc_html_e( 'Sort', 'module11' ); ?></label><select class="rl-sort selectish" id="rl-sort" name="f_sort">
                                    <?php foreach ( $m11_sorts as $m11_value => $m11_label ) : ?>
                                    <option value="<?php echo esc_attr( $m11_value ); ?>"<?php selected( $m11_sort, $m11_value ); ?>><?php echo esc_html( $m11_label ); ?></option>
                                    <?php endforeach; ?>
                                </select>
                            </div>
                        </div>
                        <?php if ( $m11_query->have_posts() ) : ?>
                        <ul class="tiles">
                            <?php
                            while ( $m11_query->have_posts() ) :
                                $m11_query->the_post();
                                get_template_part( 'template-parts/tiles/resource-tile', null, array( 'resource_id' => get_the_ID() ) );
                            endwhile;
                            wp_reset_postdata();
                            ?>
                        </ul>
                        <?php endif; ?>
                    </div>
                </div>
                <hr class="rule rl-end m-only">
            </div>
        </section>
