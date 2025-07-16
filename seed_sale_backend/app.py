from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import logging
from predict import pred

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


model = None
model_info = {
    'loaded': False,
    'model_type': None,
    'features': [],
    'last_loaded': None
}

# For online service, we can load the model from a specified path
# def load_model(model_path):
#     """Load the ML model from file"""
#     global model, model_info
    
#     try:
#         if os.path.exists(model_path):
#             model = joblib.load(model_path)
#             model_info['loaded'] = True
#             model_info['last_loaded'] = datetime.now().isoformat()
            
#             # Try to get feature names if available
#             if hasattr(model, 'feature_names_in_'):
#                 model_info['features'] = model.feature_names_in_.tolist()
            
#             # Determine model type
#             model_type = str(type(model)).lower()
#             if 'regressor' in model_type or 'regression' in model_type:
#                 model_info['model_type'] = 'regression'
#             elif 'classifier' in model_type or 'classification' in model_type:
#                 model_info['model_type'] = 'classification'
#             else:
#                 model_info['model_type'] = 'unknown'
            
#             logger.info(f"Model loaded successfully: {model_type}")
#             return True
#         else:
#             logger.error(f"Model file not found: {model_path}")
#             return False
#     except Exception as e:
#         logger.error(f"Error loading model: {str(e)}")
#         return False

## For online service

# @app.route('/model/load', methods=['POST'])
# def load_model_endpoint():
#     """Load a model from file"""
#     data = request.get_json()
#     model_path = data.get('model_path')
    
#     if not model_path:
#         return jsonify({'error': 'model_path is required'}), 400
    
#     success = load_model(model_path)
    
#     if success:
#         return jsonify({
#             'message': 'Model loaded successfully',
#             'model_info': model_info
#         })
#     else:
#         return jsonify({'error': 'Failed to load model'}), 500
    
def preprocess_data(data):
    """Preprocess the input data for prediction"""
    df = pd.DataFrame(data)
    
    return df

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model_info['loaded']
    })

@app.route('/model/info', methods=['GET'])
def model_info_endpoint():
    """Get model information"""
    return jsonify(model_info)


@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:

        request_data = request.get_json()
        print(f"Request data: {request_data}")
        
        if not request_data or 'data' not in request_data:
            return jsonify({'error': 'No data provided'}), 400
        
        input_data = request_data['data']
        
        if not input_data:
            return jsonify({'error': 'Empty data provided'}), 400
        
        # Preprocess the data
        df = preprocess_data(input_data)

        predictions = pred(df)
        print(predictions)
        
       
        response = {
            'predictions': predictions.tolist(),
            # 'model_type': model_info['model_type'],
            # 'timestamp': datetime.now().isoformat(),
            # 'data_points': len(input_data)
        }
        
        logger.info(f"Generated {len(predictions)} predictions")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':

    ###  Try to load model on startup: Improve later 
    # model_path = os.environ.get('./', 'best_model.pkl')
    
    # if os.path.exists(model_path):
    #     load_model(model_path)
    # else:
    #     logger.warning(f"Model file not found at {model_path}")
    
    # Run the Flask app
    # app.run(debug=True, host='0.0.0.0', port=5000)
    #Use port 5001 if it has conflicts
    app.run(debug=True, host='0.0.0.0', port=5001) 

