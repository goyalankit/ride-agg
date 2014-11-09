class Route:
    def __init__(self, data):
        self.distance = data['distance']['value']
        self.distance_text = data['distance']['text']
        loc_creater = lambda x: {'lat': x['k'], 'lon': x['B']}
        self.start_location = loc_creater(data['start_location'])
        self.end_location = loc_creater(data['end_location'])
        self.start_address = data['start_address']
        self.end_address = data['end_address']
        self.duration = data['duration']['value']



