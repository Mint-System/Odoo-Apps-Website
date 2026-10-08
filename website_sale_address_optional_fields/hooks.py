def post_init_hook(env):
    """Apply the default optional fields to existing websites."""
    websites = env["website"].search([])
    websites.address_optional_field_ids = websites._default_address_optional_field_ids()
