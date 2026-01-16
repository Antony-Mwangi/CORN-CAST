def predict_yield(rainfall, temperature, nitrogen, phosphorus, potassium, ph):
    
    # Base yield
    yield_est = 2.0  # tons/hectare

    # Adjust by nutrients
    yield_est += 0.05 * nitrogen
    yield_est += 0.03 * phosphorus
    yield_est += 0.02 * potassium

    # Adjust by rainfall (ideal 100-150mm)
    if 100 <= rainfall <= 150:
        yield_est += 1.0
    elif rainfall < 100:
        yield_est -= 0.5
    else:
        yield_est -= 0.3

    # Adjust by temperature (ideal 20-30°C)
    if 20 <= temperature <= 30:
        yield_est += 0.5
    else:
        yield_est -= 0.5

    # I Adjust by pH (ideal 6-7)
    if 6 <= ph <= 7:
        yield_est += 0.2
    else:
        yield_est -= 0.2

    # I Ensure yield is not negative
    yield_est = max(yield_est, 0)

    return round(yield_est, 2)


def generate_recommendations(nitrogen, phosphorus, potassium, ph):

    # Rule-based recommendations based on soil/nutrient levels
    
    recommendations = []

    if nitrogen < 30:
        recommendations.append("Nitrogen is low. Consider applying N fertilizer (e.g., Urea).")
    if phosphorus < 10:
        recommendations.append("Phosphorus is low. Consider adding DAP fertilizer.")
    if potassium < 10:
        recommendations.append("Potassium is low. Consider using Muriate of Potash (KCl).")
    if ph < 6:
        recommendations.append("Soil is acidic. Consider liming to raise pH.")
    if ph > 7.5:
        recommendations.append("Soil is alkaline. Consider sulfur-based treatment to lower pH.")

    if not recommendations:
        recommendations.append("All nutrient levels are within optimal range. Maintain current practices.")

    return recommendations
