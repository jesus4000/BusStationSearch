from flask import Flask, render_template, request
import parsingWeb


app = Flask(__name__)

global host
global port
global apikey
host = 'http://localhost'
port = '5300'


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/whois', methods=['POST'])
def who(popupFlag=None):
    popupFlag = request.form['aboutWho']
    # popupFlag = request.form.get('aboutWho', False)
    print(popupFlag)
    return render_template('layout.html', popupFlag=popupFlag)



@app.route('/search')
@app.route('/<string:keyword>')
def search(keyword='', x_Axis=None, y_Axis=None):
    return render_template('layout.html')



@app.route('/mapSearch', methods=['POST'])
def mapSearch(keyword=None):
    try:
        keyword = request.form['keyword']

        if keyword is None or len(keyword) < 2:
            placeListData = [[],[],[],[]]
            resultCNT = 0
        else:
            busList, selectFlag = parsingWeb.daumMapweb(keyword)
            placeList = []
            xList = []
            yList = []
            busNum = []


            for result in busList:
                placeList.append(result[0])
                xList.append(float(result[2]))
                yList.append(float(result[3]))
                busNum.append(result[1])
            placeListData = zip(placeList, xList, yList, busNum)
            resultCNT = len(busList)

            if resultCNT > 15:
                resultCNT = -1

        selectFlag = 'n'

        return render_template('layout.html', keyword=keyword, placeListData=placeListData
                               , resultCNT=resultCNT, selectFlag=selectFlag)
    except:
        popupFlag = 'e'
        return render_template('layout.html', popupFlag=popupFlag)



# Need DB connection

# Need Map screen


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=port, debug=True)

