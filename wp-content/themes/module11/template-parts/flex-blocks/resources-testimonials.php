<?php
/**
 * Layout: resources_testimonials
 * Source: resources / testimonials (spec/fragments/resources/02-testimonials.html). JS hooks: none.
 *
 * Structure (source CSS): .rt-row is a 4-column grid; each .rt-ex spans rt-ex--N columns
 * where N = its number of videos (subgrid); rows are separated by <hr class="rule">.
 * Transplant:
 * - expert_entries rows are collected (full have_rows loop, never broken early) and packed
 *   into .rt-row--K groups by column capacity (4) -- reproduces the drawn 3/3/1 grouping
 *   from the 7 source entries deterministically. Each entry's span = video count (1..4).
 * - bio (textarea) -> .tx-bio line block: line 1 <p class="ln lh30"><strong class="s15">,
 *   line 2 <p class="ln lh30"><span class="s12">, lines 3+ <p class="ln lh20 shn5"><span class="s12">
 *   (the fragment's dominant pattern). DEVIATION: the fragment splits some lines into
 *   several spans and the co-credited entry (rt-ex--shared) uses inline strong names with
 *   lh24/lh28 lines -- one textarea cannot carry that; it renders with the standard pattern.
 * - DROPPED: per-entry Figma width utilities on .tx-bio (w592/w303/w312/w281/w623/w304) --
 *   no field; .tx-bio spans its grid columns instead.
 * - videos: relationship to m11_resource -> template-parts/cards/resource-video.php.
 * - shared_caption set -> entry gets rt-ex--shared, videos render without their own
 *   caption and ONE <div class="tx-cap tx-cap--shared w616"> follows the list (line 1
 *   strong s14, further lines span s12, all lh22 -- fragment shape).
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

$m11_entries = array();
if ( have_rows( 'expert_entries' ) ) {
	while ( have_rows( 'expert_entries' ) ) {
		the_row();
		$m11_videos    = array_values( array_filter( array_map( 'absint', (array) get_sub_field( 'videos' ) ) ) );
		$m11_entries[] = array(
			'bio'    => (string) get_sub_field( 'bio' ),
			'videos' => $m11_videos,
			'shared' => (string) get_sub_field( 'shared_caption' ),
			'span'   => max( 1, min( 4, count( $m11_videos ) ) ),
		);
	}
}

// Pack entries into grid rows of 4 columns.
$m11_rows = array();
$m11_used = 4;
foreach ( $m11_entries as $m11_entry ) {
	if ( $m11_used + $m11_entry['span'] > 4 ) {
		$m11_rows[] = array();
		$m11_used   = 0;
	}
	$m11_rows[ count( $m11_rows ) - 1 ][] = $m11_entry;
	$m11_used                            += $m11_entry['span'];
}

$m11_bio_rules = array(
	array( 'ln lh30', 'strong', 's15' ),
	array( 'ln lh30', 'span', 's12' ),
	array( 'ln lh20 shn5', 'span', 's12' ),
);
$m11_cap_rules = array(
	array( 'ln lh22', 'strong', 's14' ),
	array( 'ln lh22', 'span', 's12' ),
);
?>
<section<?php echo m11_section_attrs( 'rs rt', 'testimonials' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <hr class="rule rule--top">
                <?php if ( $m11_heading ) : ?>
                <h2 class="sec-h2 rt-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php foreach ( $m11_rows as $m11_r => $m11_row ) : ?>
                <?php if ( $m11_r > 0 ) : ?>
                <hr class="rule">
                <?php endif; ?>
                <div class="rt-row rt-row--<?php echo esc_attr( $m11_r + 1 ); ?>">
                    <?php foreach ( $m11_row as $m11_entry ) : ?>
                    <?php $m11_has_shared = '' !== trim( $m11_entry['shared'] ); ?>
                    <article class="rt-ex rt-ex--<?php echo esc_attr( $m11_entry['span'] ); ?><?php echo $m11_has_shared ? ' rt-ex--shared' : ''; ?>">
                        <?php if ( '' !== trim( $m11_entry['bio'] ) ) : ?>
                        <div class="tx-bio">
                            <?php echo m11_line_block( $m11_entry['bio'], $m11_bio_rules ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                        </div>
                        <?php endif; ?>
                        <?php if ( $m11_entry['videos'] ) : ?>
                        <ul class="rt-vids">
                            <?php
                            foreach ( $m11_entry['videos'] as $m11_vid ) {
                                get_template_part(
                                    'template-parts/cards/resource-video',
                                    null,
                                    array(
                                        'resource_id'  => $m11_vid,
                                        'with_caption' => ! $m11_has_shared,
                                    )
                                );
                            }
                            ?>
                        </ul>
                        <?php endif; ?>
                        <?php if ( $m11_has_shared ) : ?>
                        <div class="tx-cap tx-cap--shared w616">
                            <?php echo m11_line_block( $m11_entry['shared'], $m11_cap_rules ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                        </div>
                        <?php endif; ?>
                    </article>
                    <?php endforeach; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </section>
