<?php
/**
 * Dynamic tag: a tel:/mailto: link built from a Site Settings value.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * URL tag.
 */
class M11_Tag_Setting_Link extends \Elementor\Core\DynamicTags\Data_Tag {

	public function get_name() {
		return 'm11-setting-link';
	}

	public function get_title() {
		return __( 'Site Settings link', 'module11' );
	}

	public function get_group() {
		return 'm11-site-settings';
	}

	public function get_categories() {
		return array( \Elementor\Modules\DynamicTags\Module::URL_CATEGORY );
	}

	protected function register_controls() {
		$fields = m11_elementor_tag_fields();

		$this->add_control(
			'field',
			array(
				'label'   => __( 'Field', 'module11' ),
				'type'    => \Elementor\Controls_Manager::SELECT,
				'options' => $fields['link'],
			)
		);
	}

	public function get_value( array $options = array() ) {
		$field  = (string) $this->get_settings( 'field' );
		$fields = m11_elementor_tag_fields();

		return isset( $fields['link'][ $field ] ) ? esc_url_raw( m11_setting_link_url( $field ), array( 'tel', 'mailto' ) ) : '';
	}
}
