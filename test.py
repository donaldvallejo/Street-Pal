from app import app
from unittest import TestCase, main as unittest_main
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
# import MutableMapping
# import Mapping

sample_car_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_car = {
    'Make': 'Toyota',
    'Model': 'camry',
    'Description': 'an ok car',
    'Color': 'white',
    'Price': '25000'
}

sample_form_data = {
    'Make': sample_car['Make'],
    'Model': sample_car['Model'],
    'Description': sample_car['Description'],
    'Color': sample_car['Color'],
    'Price': sample_car['Price']
}

class carsTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
            """Test the cars homepage."""
            result = self.client.get('/')
            self.assertEqual(result.status, '200 OK')
            self.assertIn(b'car', result.data)
        
    def test_new(self):
            """Test the new car creation page."""
            result = self.client.get('/cars/new')
            self.assertEqual(result.status, '200 OK')
            self.assertIn(b'Cars for days', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_car(self, mock_find):
        """Test showing a single car."""
        mock_find.return_value = sample_car

        result = self.client.get(f'/cars/{sample_car_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cars for days', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_car(self, mock_find):
        """Test editing a single car."""
        mock_find.return_value = sample_car

        result = self.client.get(f'/cars/{sample_car_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cars for days', result.data)

if __name__ == '__main__':
    unittest_main()