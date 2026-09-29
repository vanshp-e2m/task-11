<?php
/**
 * Template Name: Flexible Content
 *
 * Flexible Content page. The field group group_m11_page_sections is located on
 * page_template == templates/page-flexible.php, so this file MUST stay at this path.
 * Each `sections` row renders template-parts/flex-blocks/{kebab-case layout}.php via
 * m11_render_sections() (have_rows('sections') -> get_row_layout() dispatch).
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>
<main id="content" class="site-main m11-flex-page m11-page-<?php echo esc_attr( get_post_field( 'post_name', get_queried_object_id() ) ); ?>">
	<?php
	while ( have_posts() ) :
		the_post();
		m11_render_sections( 'sections' );
	endwhile;
	?>
</main>
<?php
get_footer();
