<?php
/**
 * Layout: resources_brochures
 * Source: resources / brochures (spec/fragments/resources/04-brochures.html). JS hooks: none.
 *
 * Structure (source): 9 .bg blocks for 12 collaborations -- blocks 4, 5, 8 are
 * .bg--pair blocks holding TWO single-brochure collaborations side by side (.bg-half),
 * the rest are .bg--grid blocks; the last block has no copy. The source CSS styles each
 * block by position (.bg-1 … .bg-9).
 * Transplant:
 * - collaboration_groups rows are collected (full have_rows loop) and packed into blocks:
 *   consecutive groups with exactly ONE brochure card pair up into a .bg--pair block
 *   (verbatim .bg-halves/.bg-half prototype, excerpt card variant); every other group is a
 *   .bg--grid block (title card variant). This reproduces the drawn 9 blocks from the 12
 *   source groups deterministically. bg-N = 1-based block index.
 * - Modifiers: pair blocks = 'bg--pair bg--m-stack bg--inset' (as drawn); grid blocks =
 *   bg--m-stack when <= 2 cards, else bg--m-grid (matches all 6 drawn grid blocks).
 *   HARDCODED positional maps (no field carries them -- report): bg--inset on grid blocks
 *   3 and 6; .bg-text line-wrap widths (w934/w1106/w1054/w1054/w934 for grid blocks 1/2/3/6/7,
 *   w534/w567 for the two halves of a pair); mobile-order classes mo-1,3,5,6,7,2,4 on the
 *   cards of block 9 (the source's mobile re-ordering of the copy-less group).
 * - collaborator_text (textarea, optional) -> .bg-copy line block: line 1
 *   <p class="ln lh26"><strong class="s16">, further lines <p class="ln lh26"><span class="s16">.
 *   Empty -> no .bg-text at all (group 9 shape).
 * - brochure_cards: relationship to m11_resource -> template-parts/cards/brochure-card.php.
 * - Each block ends with the fragment's <hr class="rule">.
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

$m11_groups = array();
if ( have_rows( 'collaboration_groups' ) ) {
	while ( have_rows( 'collaboration_groups' ) ) {
		the_row();
		$m11_groups[] = array(
			'text'  => (string) get_sub_field( 'collaborator_text' ),
			'cards' => array_values( array_filter( array_map( 'absint', (array) get_sub_field( 'brochure_cards' ) ) ) ),
		);
	}
}

// Pack groups into .bg blocks.
$m11_blocks = array();
$m11_count  = count( $m11_groups );
for ( $m11_g = 0; $m11_g < $m11_count; $m11_g++ ) {
	$m11_group = $m11_groups[ $m11_g ];
	if ( 1 === count( $m11_group['cards'] ) ) {
		$m11_halves = array( $m11_group );
		if ( $m11_g + 1 < $m11_count && 1 === count( $m11_groups[ $m11_g + 1 ]['cards'] ) ) {
			$m11_halves[] = $m11_groups[ ++$m11_g ];
		}
		$m11_blocks[] = array(
			'type'   => 'pair',
			'halves' => $m11_halves,
		);
	} else {
		$m11_blocks[] = array(
			'type'  => 'grid',
			'group' => $m11_group,
		);
	}
}

$m11_inset    = array( 3, 6 );
$m11_grid_w   = array( 1 => 'w934', 2 => 'w1106', 3 => 'w1054', 6 => 'w1054', 7 => 'w934' );
$m11_half_w   = array( 'w534', 'w567' );
$m11_mo_block = 9;
$m11_mo_map   = array( 1, 3, 5, 6, 7, 2, 4 );
$m11_copy     = array(
	array( 'ln lh26', 'strong', 's16' ),
	array( 'ln lh26', 'span', 's16' ),
);
?>
<section<?php echo m11_section_attrs( 'rs br', 'brochures' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <hr class="rule rule--top">
                <?php if ( $m11_heading ) : ?>
                <h2 class="sec-h2 br-h2"><?php echo esc_html( $m11_heading ); ?></h2>
                <?php endif; ?>
                <?php
                foreach ( $m11_blocks as $m11_b => $m11_block ) :
                    $m11_n = $m11_b + 1;
                    if ( 'pair' === $m11_block['type'] ) :
                        ?>
                <div class="<?php echo esc_attr( 'bg bg--pair bg--m-stack bg--inset bg-' . $m11_n ); ?>">
                    <div class="bg-halves">
                        <?php foreach ( $m11_block['halves'] as $m11_h => $m11_half ) : ?>
                        <div class="bg-half">
                            <?php if ( '' !== trim( $m11_half['text'] ) ) : ?>
                            <div class="<?php echo esc_attr( 'bg-text ' . $m11_half_w[ $m11_h ] ); ?>">
                                <div class="bg-copy">
                                    <?php echo m11_line_block( $m11_half['text'], $m11_copy ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                                </div>
                            </div>
                            <?php endif; ?>
                            <ul class="bg-cards">
                                <?php
                                foreach ( $m11_half['cards'] as $m11_card ) {
                                    get_template_part(
                                        'template-parts/cards/brochure-card',
                                        null,
                                        array(
                                            'resource_id' => $m11_card,
                                            'variant'     => 'excerpt',
                                        )
                                    );
                                }
                                ?>
                            </ul>
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <hr class="rule">
                </div>
                        <?php
                    else :
                        $m11_group   = $m11_block['group'];
                        $m11_classes = 'bg bg--grid ' . ( count( $m11_group['cards'] ) <= 2 ? 'bg--m-stack' : 'bg--m-grid' )
                            . ( in_array( $m11_n, $m11_inset, true ) ? ' bg--inset' : '' ) . ' bg-' . $m11_n;
                        ?>
                <div class="<?php echo esc_attr( $m11_classes ); ?>">
                    <?php if ( '' !== trim( $m11_group['text'] ) ) : ?>
                    <div class="<?php echo esc_attr( trim( 'bg-text ' . ( isset( $m11_grid_w[ $m11_n ] ) ? $m11_grid_w[ $m11_n ] : '' ) ) ); ?>">
                        <div class="bg-copy">
                            <?php echo m11_line_block( $m11_group['text'], $m11_copy ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                        </div>
                    </div>
                    <?php endif; ?>
                    <?php if ( $m11_group['cards'] ) : ?>
                    <ul class="bg-cards">
                        <?php
                        foreach ( $m11_group['cards'] as $m11_c => $m11_card ) {
                            get_template_part(
                                'template-parts/cards/brochure-card',
                                null,
                                array(
                                    'resource_id' => $m11_card,
                                    'variant'     => 'title',
                                    'mo'          => ( $m11_mo_block === $m11_n && isset( $m11_mo_map[ $m11_c ] ) ) ? $m11_mo_map[ $m11_c ] : null,
                                )
                            );
                        }
                        ?>
                    </ul>
                    <?php endif; ?>
                    <hr class="rule">
                </div>
                        <?php
                    endif;
                endforeach;
                ?>
            </div>
        </section>
