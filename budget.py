from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('budget.html')


def calculate_seed_cost(crop_type, field_size):
    # Example: $10 per acre for corn, $15 per acre for wheat
    seed_cost_per_acre = {
        'Maize': 5000,
        'Wheat': 3623,
        'Sugarcane':4000,
        'Rice':3500,
        'Ragi':2000,
        'Cotton':5000,
        'Linseed':3000,
        'Sunflower':4500,
        'Citrus fruits':2500,
        'Jowar':2500,
        'Groundnut':3500,
        'Barley':3500,
        'Gram':4000,
        'Vegetables':1500,
        'Mustard':4000,
        'Carrot':2000,
        'Fenugreek':5000,
        'Turnip':2000,
        'Watermellon':1500,
        'Millets':3000}
    
    return seed_cost_per_acre.get(crop_type, 0) * field_size

def calculate_fertilizer_cost(soil_fertility, field_size):
    # Example: $20 per acre for low fertility, $15 per acre for medium, $10 per acre for high
    fertilizer_cost_per_acre = {
        'low': 10000,
        'medium': 7500,
        'high': 5000,
    }
    return fertilizer_cost_per_acre.get(soil_fertility, 0) * field_size

def calculate_labor_cost(labor_hours, labor_rate):
    return labor_hours * labor_rate


@app.route('/budget', methods=['POST'])
def budget():
    crop_type = request.form['crop_name']
    field_size = request.form['Field_size']
    soil_fertility = request.form['fertility']
    labor_hours = request.form['Labor_Hours']
    labor_rate = request.form['Labor_rate']

    seed_cost = calculate_seed_cost(crop_type, int(field_size))
    fertilizer_cost = calculate_fertilizer_cost(soil_fertility, int(field_size))
    labor_cost = calculate_labor_cost(int(labor_hours), int(labor_rate))

    print(seed_cost, fertilizer_cost, labor_cost)

    total_cost = seed_cost + fertilizer_cost + labor_cost

    return(f"<h1>Budget Calculation Results:</h1><br><br><h3>Seed Cost: {seed_cost}</h3><h3>Fertilizer Cost: {fertilizer_cost}</h3><h3>Labor Cost: ₹{labor_cost}</h3><h2>Estimated Total Cost for crop: ₹{total_cost}</h2>")
    
if __name__ == '__main__':
    app.run(debug=True, port = 4500)