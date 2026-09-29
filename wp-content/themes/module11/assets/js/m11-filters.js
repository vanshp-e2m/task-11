/**
 * Listing filters (browse_by_product / sh_resource_results).
 *
 * The transplanted filter forms have no submit control (as drawn), so:
 * - changing any input inside a .fl-form submits that form;
 * - changing #rl-sort / .pb-sort submits the closest form. The Resource Library sort
 *   select sits OUTSIDE both forms (as drawn), so it submits the section's search form,
 *   carrying its value as a hidden field (f_sort).
 * All filter state lives in the GET query (f_* args, see inc/catalogue.php), so this is
 * progressive enhancement only.
 *
 * Enqueue (main session, real theme inc/enqueue.php):
 *   wp_enqueue_script( 'm11-filters', M11_URI . '/assets/js/m11-filters.js', array(), M11_VERSION, true );
 */
( function () {
	'use strict';

	function submit( form ) {
		if ( ! form ) {
			return;
		}
		if ( typeof form.requestSubmit === 'function' ) {
			form.requestSubmit();
		} else {
			form.submit();
		}
	}

	function carry( form, name, value ) {
		var input = form.querySelector( 'input[type="hidden"][name="' + name + '"]' );
		if ( ! input ) {
			input = document.createElement( 'input' );
			input.type = 'hidden';
			input.name = name;
			form.appendChild( input );
		}
		input.value = value;
	}

	document.addEventListener( 'change', function ( event ) {
		var el = event.target;
		if ( ! el || ! el.closest ) {
			return;
		}

		if ( el.closest( '.fl-form' ) && el.matches( 'input, select' ) ) {
			submit( el.closest( 'form' ) );
			return;
		}

		if ( el.matches( '#rl-sort, .pb-sort' ) ) {
			var form = el.closest( 'form' );
			if ( ! form ) {
				var section = el.closest( 'section' );
				form = section ? section.querySelector( 'form.rl-search, form.pb-search' ) : null;
				if ( form && el.name ) {
					carry( form, el.name, el.value );
				}
			}
			submit( form );
		}
	} );
}() );
