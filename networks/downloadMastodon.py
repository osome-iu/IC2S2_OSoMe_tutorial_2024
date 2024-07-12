from mastodon import Mastodon


# Mastodon.create_app(
#     'ic2s2tutorial',
#     api_base_url = 'https://mastodon.social',
#     to_file = 'ic2s2tutorial_clientcred.secret'
# )
mastodon = Mastodon(access_token="CleVf2DFvXbm_dJaRHnTgfylO6lZUxB09AGL6jhLnPg", api_base_url = 'https://mastodon.social')
mastodon.timeline("@filsilva")