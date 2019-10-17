# https://streetpal.herokuapp.com/ | https://git.heroku.com/streetpal.git
# Maps API KEY : AIzaSyChhJt9bRZvlbMol6VvdQNKwR1BrvV9kx8
# sudo lsof -iTCP -sTCP:LISTEN -n -P
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_googlemaps import GoogleMaps

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/streetPal')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
services = db.services
comments = db.comments
app = Flask(__name__)

GoogleMaps(app, key="AIzaSyChhJt9bRZvlbMol6VvdQNKwR1BrvV9kx8")

@app.route('/')
def services_index():
  """Show all services"""
  return render_template('services_index.html', services=services.find())

@app.route('/services/new')
def services_new():
  """Create services"""
  return render_template('services_new.html', service = {}, title='New services')

@app.route('/services', methods=['POST'])
def services_submit():
  """Submit services to database"""
  '''
  service = {
    'Make': request.form.get('Make'),
    'Model': request.form.get('Model'),
    'Description': request.form.get('Description'),
    'Color': request.form.get('Color'),
    'Price': request.form.get('Price'),
    'Image': request.form.get('Image'),
    'created_at': datetime.now()
  }
  '''

  service_id = services.insert_one(service).inserted_id
  print("Check to see if Data is even happening \n", service_id, service)
  return redirect(url_for('services_show', service_id=service_id))

@app.route('/services/<service_id>')
def services_show(car_id):
    """Show a single service."""
    service = services.find_one({'_id': ObjectId(service_id)})
    service_comments = comments.find({'service_id': ObjectId(service_id)})
    return render_template('services_show.html', service=service, comments=service_comments)

@app.route('/services/<service_id>/edit')
def services_edit(service_id):
    """Show the edit form for a service."""
    service = services.find_one({'_id': ObjectId(service_id)})
    return render_template('services_edit.html', service=service, title='Edit service')

'''
@app.route('/search', methods=['POST'])
def search():
  searched_services = services.find()
  search = request.form.get('search')
  search_items = []
  for car in searched_cars:
    if search.lower() in car['Pit Stop']['Tenderloin'].lower():
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
'''

@app.route('/services/<service_id>', methods=['POST'])
def services_update(service_id):
  """Submit an edited services"""
  updated_service = {
      'Make': request.form.get('Make'),
      'Model': request.form.get('Model'),
      'Description': request.form.get('Description'),
      'Color': request.form.get('Color'),
      'Price': request.form.get('Price'),
      'Image': request.form.get('Image'),
  }
  services.update_one(
    {'_id': ObjectId(service_id)},
    {'$set': updated_service})
  return redirect(url_for('services_show', service_id=service_id))

@app.route('/services/<service_id>/delete', methods=['POST'])
def services_delete(service_id):
    """Delete one service."""
    services.delete_one({'_id': ObjectId(service_id)})
    return redirect(url_for('services_index'))

@app.route('/services/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'car_id': ObjectId(request.form.get('car_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('services_show', service_id=request.form.get('service_id')))

@app.route('/services/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('services_show', service_id=comment.get('service_id')))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))