<?php
/**
 * Dynamic tag: a Site Settings value as text (phone, email, hours, address, portal name).
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Text tag.
 */
class M11_Tag_Setting_Text extends \Elementor\Core\DynamicTags\Tag {

	public function get_name() {
		return 'm11-setting-text';
	}

	public function get_title() {
		return __( 'Site Settings value', 'module11' );
	}

	public function get_group() {
		return 'm11-site-settings';
	}

	public function get_categories() {
		return array( \Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY );
	}

	protected function register_controls() {
		$fields = m11_elementor_tag_fields();

		$this->add_control(
			'field',
			array(
				'label'   => __( 'Field', 'module11' ),
				'type'    => \Elementor\Controls_Manager::SELECT,
				'options' => $fields['text'],
			)
		);
	}

	public function render() {
		$field  = (string) $this->get_settings( 'field' );
		$fields = m11_elementor_tag_fields();

		if ( ! isset( $fields['text'][ $field ] ) ) {
			return;
		}

		// Address is stored with <br> line breaks; allow only that.
		echo wp_kses( (string) m11_get_setting( $field ), array( 'br' => array() ) );
	}
}
