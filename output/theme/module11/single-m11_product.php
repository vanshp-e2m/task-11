<?php
/**
 * Single product (m11_product) -- ONE template for the three drawn product pages
 * (base = Sugita II, variation A = LawtonElite + instruments table, variation B =
 * Feather Blades + size selector / size guide). Field group: group_m11_product_fields.
 *
 * Fixed section order (plan template_strategy.cpt_templates):
 *   product-overview -> [size-guide] -> [instruments-included] -> accessories ->
 *   testimonial -> related-products
 * Optional blocks render only when their true_false flag is on AND they have rows.
 * Each block is a transplanted fragment under template-parts/product/.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
<main id="content" class="site-main m11-product-page">
	<?php
	while ( have_posts() ) :
		the_post();
		$m11_part_args = array( 'product_id' => get_the_ID() );

		get_template_part( 'template-parts/product/overview', null, $m11_part_args );

		if ( get_field( 'has_size_guide' ) && get_field( 'size_rows' ) ) {
			get_template_part( 'template-parts/product/size-guide', null, $m11_part_args );
		}

		if ( get_field( 'has_instruments_table' ) && get_field( 'instrument_rows' ) ) {
			get_template_part( 'template-parts/product/instruments-included', null, $m11_part_args );
		}

		get_template_part( 'template-parts/product/tile-grid', null, $m11_part_args + array( 'block' => 'accessories' ) );
		get_template_part( 'template-parts/product/testimonial', null, $m11_part_args );
		get_template_part( 'template-parts/product/tile-grid', null, $m11_part_args + array( 'block' => 'related' ) );
	endwhile;
	?>
</main>
<?php
get_footer();
