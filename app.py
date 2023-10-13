from flask import Flask, Response, render_template,request
import json
import time

app = Flask(__name__)

def read_json():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

def read_json2():
    with open('data2.json', 'r') as file2:
        data2 = json.load(file2)
    return data2

@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        filtered_data = {
            'results': [d for d in read_json2()['results'] if search in d['detected_on']]
        }
        return render_template('index.html', data=filtered_data, search=search)
    return render_template('index2.html', data=read_json2())


@app.route('/rekap')
def about():
    search = request.args.get('search')
    if search:
        filtered_data = {
            'results': [d for d in read_json2()['results'] if search in d['current_time']]
        }
        return render_template('rekap.html', data=filtered_data, search=search)
    return render_template('rekap.html', data=read_json2())
    


    # search = request.args.get('search')
    # if search:
    #     filtered_data = {
    #         'results': [d for d in read_json2()['results'] if search in d['detected_on']]
    #     }
    #     return render_template('index.html', data2=filtered_data, search=search)
    # return render_template('index.html', data=read_json2())


    # search = request.args.get('search')
    # if search:
    #     filtered_data = {
    #         'results': [d for d in data['results'] if search in d['detected_on']]
    #     }
    #     return render_template('index.html', data=filtered_data, search=search)
    # return render_template('index.html', data=data)


    # search = request.args.get('search')
    # if search:
    #     filtered_data = {
    #         'people': [person for person in data['people'] if search.lower() in person['name'].lower()]
    #     }
    #     return render_template('index.html', data=filtered_data, search=search)
    # return render_template('index.html', data=data)


@app.route('/data')
def data():
    def poll():
        last_modified = time.time()
        while True:
            time.sleep(1)  # polling setiap 1 detik
            data = read_json()
            if time.time() > last_modified:
                last_modified = time.time()
                yield f"data: {json.dumps(data)}\n\n"
    return Response(poll(), mimetype='text/event-stream')
    

if __name__ == '__main__':
    app.run(debug=True)



