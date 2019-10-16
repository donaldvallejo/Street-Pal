# sudo lsof -iTCP -sTCP:LISTEN -n -P
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cars')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
cars = db.cars
comments = db.comments

app = Flask(__name__)

@app.route('/')
def cars_index():
  """Show all cars"""
  return render_template('cars_index.html', cars=cars.find())

@app.route('/cars/new')
def cars_new():
  """Create cars"""
  return render_template('cars_new.html', car = {}, title='New Cars')

@app.route('/cars', methods=['POST'])
def cars_submit():
  """Submit cars to database"""
  car = {
    'Make': request.form.get('Make'),
    'Model': request.form.get('Model'),
    'Description': request.form.get('Description'),
    'Color': request.form.get('Color'),
    'Price': request.form.get('Price'),
    'Image': request.form.get('Image'),
    'created_at': datetime.now()
  }

  car_id = cars.insert_one(car).inserted_id
  print("Check to see if Data is even happening \n", car_id, car)
  return redirect(url_for('cars_show', car_id=car_id))

@app.route('/cars/<car_id>')
def cars_show(car_id):
    """Show a single car."""
    car = cars.find_one({'_id': ObjectId(car_id)})
    car_comments = comments.find({'car_id': ObjectId(car_id)})
    return render_template('cars_show.html', car=car, comments=car_comments)

@app.route('/cars/<car_id>/edit')
def cars_edit(car_id):
    """Show the edit form for a car."""
    car = cars.find_one({'_id': ObjectId(car_id)})
    return render_template('cars_edit.html', car=car, title='Edit Car')

@app.route('/search', methods=['POST'])
def search():
  searched_cars = cars.find()
  search = request.form.get('search')
  search_items = []
  for car in searched_cars:
    if search.lower() in car['Make'].lower():
      search_items.append(car)
    elif search.lower() in car['Model'].lower():
      search_items.append(car)
    elif search.lower() in car['Color'].lower():
      search_items.append(car)
    elif search.lower() in car['Price'].lower():
      search_items.append(car)
    else:
      print('how did you break this?')
  return render_template('cars_index.html', cars=search_items)

@app.route('/cars/<car_id>', methods=['POST'])
def cars_update(car_id):
  """Submit an edited cars"""
  updated_car = {
      'Make': request.form.get('Make'),
      'Model': request.form.get('Model'),
      'Description': request.form.get('Description'),
      'Color': request.form.get('Color'),
      'Price': request.form.get('Price'),
      'Image': request.form.get('Image'),
  }
  cars.update_one(
    {'_id': ObjectId(car_id)},
    {'$set': updated_car})
  return redirect(url_for('cars_show', car_id=car_id))

@app.route('/cars/<car_id>/delete', methods=['POST'])
def cars_delete(car_id):
    """Delete one car."""
    cars.delete_one({'_id': ObjectId(car_id)})
    return redirect(url_for('cars_index'))

@app.route('/cars/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'car_id': ObjectId(request.form.get('car_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('cars_show', car_id=request.form.get('car_id')))

@app.route('/cars/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('cars_show', car_id=comment.get('car_id')))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))