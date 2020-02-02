from flask import Flask, render_template
app = Flask(__name__)

name="Guido van Rossum"

@app.route('/hello')
def hello():
	return ("Hello. "+name+"!")
	
	
@app.route('/bootstrap')
def bootstrap():
	return render_template('bootstrap.html', nick=name) 

    

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
