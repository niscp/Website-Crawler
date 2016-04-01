from restaurant import Restaurant


def get_restra(location, area, page):
    r = Restaurant(location=location, area=area, page=page)
    data = r.getAll()
    return data


