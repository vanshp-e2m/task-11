// Module 11 front-end scripts.

// Nested Accordion: Elementor can only open the FIRST item by default. Contact Us draws the 2nd FAQ open, so the widget carries
// an editor-set custom attribute `data-m11-open="<n>"` (Advanced → Attributes) and the n-th item is opened on load.
document.querySelectorAll( '[data-m11-open]' ).forEach( ( widget ) => {
	const n = parseInt( widget.getAttribute( 'data-m11-open' ), 10 );
	const item = widget.querySelectorAll( 'details.e-n-accordion-item' )[ n - 1 ];
	if ( item ) {
		item.open = true;
		const title = item.querySelector( 'summary' );
		if ( title ) {
			title.setAttribute( 'aria-expanded', 'true' );
		}
	}
} );
