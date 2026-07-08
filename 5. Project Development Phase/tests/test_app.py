import unittest
import os
import sys
import json

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

class CropPredictionTests(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def test_predict_crop_returns_string(self):
        prediction = app.predict_crop(90, 42, 43, 20.9, 82.0, 6.5, 202.9)
        self.assertIsInstance(prediction, str)
        self.assertTrue(len(prediction) > 0)

    def test_predict_endpoint_success(self):
        # Send POST request to predict
        payload = {
            'nitrogen': 90,
            'phosphorus': 42,
            'potassium': 43,
            'temperature': 20.9,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('crop', data)
        self.assertIn('label', data)
        self.assertIn('description', data)
        self.assertIn('top3', data)
        self.assertIn('radar_labels', data)
        self.assertIn('radar_user', data)
        self.assertIn('radar_ideal', data)
        self.assertIn('match_status', data)
        self.assertIn('param_advice', data)
        self.assertIn('inputs', data)

    def test_predict_endpoint_invalid_values(self):
        # Send POST request with invalid parameter
        payload = {
            'nitrogen': 'invalid_string',
            'phosphorus': 42,
            'potassium': 43,
            'temperature': 20.9,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_predict_endpoint_negative_values(self):
        # Send POST request with negative parameter
        payload = {
            'nitrogen': -10,
            'phosphorus': 42,
            'potassium': 43,
            'temperature': 20.9,
            'humidity': 82.0,
            'ph': 6.5,
            'rainfall': 202.9
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OptiCrop', response.data)

if __name__ == "__main__":
    unittest.main()
