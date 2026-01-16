def predict_yield(rainfall, temperature, nitrogen, phosphorus, potassium, ph):
    yield_est = 2.0  


    yield_est += 0.05 * nitrogen
    yield_est += 0.03 * phosphorus
    yield_est += 0.02 * potassium

    if 100 <= rainfall <= 150:
        yield_est += 1.0
    elif rainfall < 100:
        yield_est -= 0.5
    else:
        yield_est -= 0.3

    
    if 20 <= temperature <= 30:
        yield_est += 0.5
    else:
        yield_est -= 0.5

    
    if 6 <= ph <= 7:
        yield_est += 0.2
    else:
        yield_est -= 0.2

    
    if yield_est < 0:
        yield_est = 0

    return round(yield_est, 2)
