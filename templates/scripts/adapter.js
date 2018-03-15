function getData(){
  var firstname = document.getElementsByName("firstname")[0].value;
  var lastname = document.getElementsByName("lastname")[0].value;
  var formdata = new FormData();
  formdata.append('firstname',firstname);
  formdata.append('lastname',lastname);

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
      alert.innerHTML = "Success";
    }
  }

}
