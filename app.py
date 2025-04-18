from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # A simple form to input data

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the data sent from the frontend
    x_values = [
        float(request.form['x1']),
        float(request.form['x2']),
        float(request.form['x3']),
        float(request.form['x4']),
        float(request.form['x5']),
        float(request.form['x6']),
        float(request.form['x7'])
    ]
    y_values = [
        float(request.form['y1']),
        float(request.form['y2']),
        float(request.form['y3']),
        float(request.form['y4']),
        float(request.form['y5']),
        float(request.form['y6']),
        float(request.form['y7'])
    ]

    # Perform linear regression (using np.polyfit to get slope and offset)
    try:
        slope, offset = np.polyfit(x_values, y_values, 1)
        
        # Round the slope and offset to 3 decimal places
        slope = round(slope, 3)
        offset = round(offset, 3)

        # Generate the plot
        img = generate_plot(x_values, y_values, slope, offset)

        # Pass slope, offset, and plot image to template
        return render_template('result.html', slope=slope, offset=offset, plot_img=img)

    except Exception as e:
        return str(e)

def generate_plot(x_values, y_values, slope, offset):
    # Create a plot with x and y values
    plt.figure(figsize=(6, 4))
    plt.scatter(x_values, y_values, color='blue', label='Data points')

    # Create a line using the slope and offset (y = slope * x + offset)
    x_line = np.linspace(min(x_values), max(x_values), 100)
    y_line = slope * x_line + offset
    plt.plot(x_line, y_line, color='red', label=f'Fit Line: y = {slope}x + {offset}')
    
    # Labels and title
    plt.title('Canvas Tension vs. Pressure Setpoint')
    plt.xlabel('Pressure Setpoint (kPa)')
    plt.ylabel('Canvas Tension (kN/m)')
    plt.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot as base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    # Close the plot to free up memory
    plt.close()

    return img_base64

if __name__ == '__main__':
    app.run(debug=True)
