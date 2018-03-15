function showLoad(){
  document.getElementsByClassName("loader")[0].style.display = 'block';
}
function hideLoad(){
  document.getElementsByClassName("loader")[0].style.display = 'none';
}

function getData(){
  var firstname = document.getElementsByName("firstname")[0].value;
  var lastname = document.getElementsByName("lastname")[0].value;
  var phone = document.getElementsByName("phone")[0].value;
  var details = document.getElementsByName("details")[0].value;
  var address = document.getElementsByName("address")[0].value;
  var preimage = document.getElementsByName("preimage")[0].files[0];
  var formdata = new FormData();
  formdata.append('firstname',firstname);
  formdata.append('lastname',lastname);
  formdata.append('phone',phone);
  formdata.append('details',details);
  formdata.append('address',address);
  formdata.append('preimage',preimage);

  return formdata;
}


function RegisterPatient(){
  try{
    var xhttp = new XMLHttpRequest();
  }catch(e){
    console.log("Not Supported");
  }
  var alert = document.getElementsByClassName("alert")[0];
  var fd = new FormData();
  fd = getData()
  var form = document.forms["myForm"]
  xhttp.open("POST","/registerpatient",true);
  xhttp.send(fd);
  xhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status==200){
      console.log(this.responseText);
      alert.style.display = "block";
      alert.innerHTML = "Patient Registration Successful";
    }
  }

}

function checkPhotoshop(files){
  try{
    var xhttp = new XMLHttpRequest();
  }catch(e){
    console.log("Not Supported");
  }
  var resultssection = document.getElementsByClassName("resultssection")[0];
  showLoad();
  xhttp.open("POST","/eaglevisionrun",true);
  xhttp.send(files);
  xhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status==200){
      var obj = JSON.parse(this.responseText);
      for(var i =0;i<obj.files.length;i++){
        var url = "http://127.0.0.1:5000/static/photoshopped/"+obj.files[i].filename;
        var add = '<tr><td>'+obj.files[i].filename+'</td><td><span style="color:red;text-align:center;">Photoshopped</span></td><td><a style="color:blue;" href="'+url+'">View</a></td></tr>';
        resultssection.innerHTML += add;
      }
      hideLoad();
    }
  }

}


function eagleMode(){
  var images = document.getElementsByName("file")[0];
  var fd = new FormData();
  for(var i=0;i<images.files.length;i++){
    console.log('image'+i);
    fd.append('image'+i,images.files[i]);
  }
  fd.append('length',images.files.length);
  checkPhotoshop(fd);
}


function compare(){
  var fd = new FormData();
  var pre = document.getElementsByName('pre')[0].files[0];
  var post = document.getElementsByName('post')[0].files[0];
  var regenerate = document.getElementsByName("regenerate")[0];
  if(regenerate.checked){
    fd.append("regenerate","true");
  }
  else{
    fd.append("regenerate","false");
  }
  fd.append('pre',pre)
  fd.append('post',post)
  try{
    var xhttp = new XMLHttpRequest();
  }catch(e){
    console.log("Not Supported");
  }
  var resultssection = document.getElementsByClassName("resultssection")[0];
  resultssection.innerHTML = '<tr style="border:1px solid lightgrey"><th>File Name</th><th>Score</th></tr>';
  showLoad();
  xhttp.open("POST","/comparemoderun",true);
  xhttp.send(fd);
  xhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status==200){
      var obj = JSON.parse(this.responseText);
      for(var i =0;i<obj.scores.length;i++){
        var add = '<tr><td>'+obj.scores[i].filename+'</td><td style="color:blue;">'+obj.scores[i].score+'</td></tr>';
        resultssection.innerHTML += add;
      }
      resultssection.innerHTML += '<tr><td>Average Score</td><td style="color:red;font-weight:bold;">'+obj.avgScore+'</td></tr>';
      resultssection.innerHTML += '<tr><td>Status</td><td style="color:red;font-weight:bold;">'+obj.status+'</td></tr>';
      hideLoad();
    }
  }
}

function extremeCompare(fd){

  try{
    xhttp = new XMLHttpRequest();
  }catch(e){
    console.log("Not Supported");
  }
  var resultssection = document.getElementsByClassName("resultssection")[0];
  xhttp.open("POST","/extremerun",true);
  xhttp.send(fd)
  showLoad();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==200){
      console.log(this.responseText);
      var obj = JSON.parse(this.responseText);
      for(var i =0;i<obj.images.length;i++){
        var add = '<tr><td>'+obj.images[i].preimage+'</td><td>'+obj.images[i].postimage+'</td><td style="color:blue;">'+obj.images[i].score+'</td></tr>';
        resultssection.innerHTML += add;
      }
      hideLoad();
    }
  }

}

function extremeMode(){
  var pre = document.getElementsByName("predir")[0];
  var post = document.getElementsByName("postdir")[0]
  var fd = new FormData();
  for(var i=0;i<pre.files.length;i++){
    console.log('preimage'+i);
    fd.append('preimage'+i,pre.files[i]);
  }
  for(var i=0;i<post.files.length;i++){
    console.log('postimage'+i);
    fd.append('postimage'+i,post.files[i]);
  }
  fd.append('prelength',pre.files.length);
  fd.append('postlength',post.files.length);
  extremeCompare(fd);
}
