<?php
/**
 * Layout: sh_login
 * Source: sales-hub-login / sales-hub-login (spec/fragments/sales-hub-login/00-sales-hub-login.html). JS hooks: none.
 *
 * Transplant notes:
 * - Logo: Site Settings image `m11_logo` via m11_get_setting() (plan static_content "logo";
 *   NOTE the plan names it `site_logo`, the real Site Settings group names it `m11_logo`).
 *   Above the fold -> not lazy. Alt = the attachment alt, else the site name.
 * - The .lg-form is the fragment's verbatim form wired to real WP auth: it POSTs log/pwd to
 *   wp-login.php (site_url 'login_post') with a hidden redirect_to = the Sales Hub
 *   dashboard. DEVIATIONS from the fragment: method get -> post (a GET would put the
 *   password in the URL) and action ../../sales-hub-dashboard/html/ -> wp-login.php; one
 *   hidden <input name="redirect_to"> added. The plan said wp_login_form(); its markup
 *   (p.login-username wrappers, #user_login ids) cannot match .lg-form, so the verbatim form
 *   is posted to the same endpoint instead.
 * - Form copy is NOT ACF per the plan's auth_note -- HARDCODED (translatable): "Email
 *   address", "Password", placeholders "rep_name@example.com" / "************",
 *   "Log in to Sales Hub".
 * - forgot_password_label: href = wp_lostpassword_url() (plan: real lost-password route).
 * - note (textarea): line breaks render as the fragment's <br>.
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

$m11_heading  = get_sub_field( 'heading' );
$m11_forgot   = get_sub_field( 'forgot_password_label' );
$m11_note     = get_sub_field( 'note' );
$m11_logo     = (int) m11_get_setting( 'm11_logo' );
$m11_logo_alt = $m11_logo ? (string) get_post_meta( $m11_logo, '_wp_attachment_image_alt', true ) : '';
$m11_redirect = m11_page_url( 'sales-hub/dashboard' );
?>
<section<?php echo m11_section_attrs( 'rs lg', 'sales-hub-login' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>>
            <div class="fx">
                <div class="lg-card"><?php echo m11_image( $m11_logo, array( 'class' => 'lg-logo', 'alt' => $m11_logo_alt ? $m11_logo_alt : get_bloginfo( 'name' ), 'loading' => false ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
                    <?php if ( $m11_heading ) : ?>
                    <h1 class="lg-h1"><?php echo esc_html( $m11_heading ); ?></h1>
                    <?php endif; ?>
                    <form class="lg-form" action="<?php echo esc_url( site_url( 'wp-login.php', 'login_post' ) ); ?>" method="post"><label class="lg-label" for="lg-email"><?php esc_html_e( 'Email address', 'module11' ); ?></label><input class="lg-in" id="lg-email" type="email" name="log" placeholder="<?php esc_attr_e( 'rep_name@example.com', 'module11' ); ?>" autocomplete="username" required><label class="lg-label" for="lg-pass"><?php esc_html_e( 'Password', 'module11' ); ?></label><input class="lg-in" id="lg-pass" type="password" name="pwd" placeholder="<?php esc_attr_e( '************', 'module11' ); ?>" autocomplete="current-password" required><?php if ( $m11_redirect ) : ?><input type="hidden" name="redirect_to" value="<?php echo esc_url( $m11_redirect ); ?>"><?php endif; ?><button class="lg-go" type="submit"><?php esc_html_e( 'Log in to Sales Hub', 'module11' ); ?></button></form><?php if ( $m11_forgot ) : ?><a class="lg-forgot" href="<?php echo esc_url( wp_lostpassword_url() ); ?>"><?php echo esc_html( $m11_forgot ); ?></a><?php endif; ?>
                    <hr class="lg-rule">
                    <?php if ( $m11_note ) : ?>
                    <p class="lg-note"><?php echo m11_multiline( $m11_note ); // phpcs:ignore WordPress.Security.EscapeOutput ?></p>
                    <?php endif; ?>
                </div>
            </div>
        </section>
