<?php
/**
 * Dynamic tag: the logo from Site Settings.
 *
 * @package module11
 */

defined( 'ABSPATH' ) || exit;

/**
 * Image tag.
 */
class M11_Tag_Setting_Image extends \Elementor\Core\DynamicTags\Data_Tag {

	public function get_name() {
		return 'm11-setting-image';
	}

	public function get_title() {
		return __( 'Site Settings logo', 'module11' );
	}

	public function get_group() {
		return 'm11-site-settings';
	}

	public function get_categories() {
		return array( \Elementor\Modules\DynamicTags\Module::IMAGE_CATEGORY );
	}

	protected function register_controls() {
		$fields = m11_elementor_tag_fields();

		$this->add_control(
			'field',
			array(
				'label'   => __( 'Logo', 'module11' ),
				'type'    => \Elementor\Controls_Manager::SELECT,
				'options' => $fields['image'],
			)
		);
	}

	public function get_value( array $options = array() ) {
		$field = (string) $this->get_settings( 'field' );
		$id    = (int) m11_get_setting( $field );

		// The white footer logo falls back to the header logo when empty.
		if ( ! $id && 'm11_logo_reversed' === $field ) {
			$id = (int) m11_get_setting( 'm11_logo' );
		}

		if ( ! $id ) {
			return array();
		}

		return array(
			'id'  => $id,
			'url' => (string) wp_get_attachment_image_url( $id, 'full' ),
		);
	}
}
