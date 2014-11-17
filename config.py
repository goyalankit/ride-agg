import os
#this is the place your app's configuration is specified
#e.g.
#   Third party api keys/secrets
#
app_config = {
        'uber' : {
            'products_url' : 'https://api.uber.com/v1/products',
            'time_url' : 'https://api.uber.com/v1/estimates/time',
            'price_url' : 'https://api.uber.com/v1/estimates/price',
            'server_token': '2lyiFYdz8I6fFOTapHRXi_GsJphpBXFadq4rWLZL',
            },
        'meru' : {
            'data_file' : os.path.abspath('data/meru.yaml')
            },
        'debug': True 
        }
