from flask import Flask,render_template, request
import os
import json
import register as rg
import ela
from compare import calculateScore, getScore, batchCompare
from regenerate import regenerateImg

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/patientimages/'

@app.route('/')
def index():
    return render_template('home.html',the_title="Vision | Home")

@app.route('/register')
def register():
    return render_template('register.html',the_title="Register Patient | Vision")

@app.route('/eagle-vision')
def eaglevision():
    return render_template('eaglevision.html',the_title="Eagle Vision | Vision")

@app.route('/compare')
def compare():
    return render_template('compare.html',the_title="Compare Mode | Vision")

@app.route('/extreme')
def extreme():
    return render_template('extreme.html',this_title="Extreme Mode | Vision")

@app.route('/extremerun',methods=['POST'])
def extremerun():
    matched = []
    prelength = request.form['prelength']
    postlength = request.form['postlength']
    postimagescores = []
    filenames = []
    for i in range(0,int(prelength)):
        oneround = []
        preimage = request.files['preimage'+str(i)]
        filename1 = preimage.filename.split('/')
        savepath = 'static/pre/'+filename1[1]
        preimage.save(savepath)
        prescore = getScore(savepath)
        if not postimagescores:
            for j in range(0,int(postlength)):
                postimage = request.files['postimage'+str(j)]
                filename2 = postimage.filename.split('/')
                savepath = 'static/post/'+filename2[1]
                postimage.save(savepath)
                postscore = getScore(savepath)
                postimagescores.append(postscore)
                filenames.append(filename2[1])
                score = batchCompare(prescore,postscore)
                oneround.append(score)


        else:
            i = 0
            for score in postimagescores:
                score = batchCompare(prescore,score)
                oneround.append(score)
                i+= 1

        for x in oneround:
            if x==0:
                oneround.remove(0)
        if(min(oneround) < 1):
            matched.append({'preimage':filename1[1],'postimage':filename2[1],'score':min(oneround)})

    return json.dumps({'images':matched})

@app.route('/comparemoderun',methods=['POST'])
def runcompare():
    avgScore = 0
    scores = []
    status = ''
    pre = request.files['pre']
    post = request.files['post']
    isRegenerated = request.form['regenerate']
    print(isRegenerated)
    path = os.path.join('static/compare/',pre.filename)
    path2 = os.path.join('static/compare/',post.filename)
    pre.save(path)
    post.save(path2)
    for images in os.listdir("regenerated-images"):
            if images.endswith(".jpg") or images.endswith(".png"):
                os.remove(os.path.join("regenerated-images",images))
    if(isRegenerated=="true"):
        regenerateImg(path2)
        for images in os.listdir("regenerated-images"):
            if images.endswith((".jpg",".jpeg",".png")):
                score = calculateScore(path,os.path.join("regenerated-images",images))
                dict = {'filename':images,'score':score}
                scores.append(dict)
                avgScore += score
        if(avgScore != 0):
                avgScore = avgScore/len(scores)
        if avgScore <= 0.9:
            status = 'Similar Faces'
        else:
            status = 'Not similar Faces'
        return json.dumps({'scores':scores, 'avgScore':avgScore, 'status':status})
    elif(isRegenerated=="false"):
        score = calculateScore(path,path2)
        print(score)
        if score <= 0.9:
            status = 'Similar Faces'
        else:
            status = 'Not similar Faces'
        return json.dumps({'scores':scores, 'avgScore':score, 'status':status})

    else:
        return json.dumps({})



@app.route('/eaglevisionrun',methods=['GET','POST'])
def run():
    files = []
    photoshopped = 0
    length = request.form['length']
    for i in range(0,int(length)):
        test = request.files['image'+str(i)]
        if(test.filename.endswith(('.jpg','.jpeg'))):
            max_diff  = ela.elaanalysis(test)
            print(test.filename+' : '+str(max_diff))
            if(max_diff > 40):
                absfilename = test.filename.split('/')
                dict = {'filename': absfilename[1], 'score':max_diff}
                files.append(dict)
    return json.dumps({'files':files})

@app.route('/registerpatient',methods=['POST'])
def regpatient():
    name = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    address = request.form['address']
    details = request.form['details']
    preimage = request.files['preimage']
    path = os.path.join(app.config['UPLOAD_FOLDER'],preimage.filename)
    preimage.save(path)
    score = getScore(path)
    isRegistered = rg.registerPat(name,lastname,phone,address,details,score)
    if isRegistered:
        return json.dumps({'status':'OK','firstname':name,'lastname':lastname, 'phone':phone, 'address':address, 'details':details})
    else:
        return json.dumps({})

app.run()
