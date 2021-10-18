var burger = $('#menu-trigger');
var submit_button = $('#call-bot-btn');
var upload_img = $('#upload_img');

burger.each(function (index) {
  var $this = $(this);

  $this.on('click', function (e) {
    e.preventDefault();
    $(this).toggleClass('active-' + (index + 1));
  })
});

burger.click(function () {
  var small_navbar = $('#small-navbar');
  if (small_navbar.css("display") == "none") {
    small_navbar.show();
  }
  else {
    small_navbar.hide();
  }
});

function click(v){
  if(frogueReadyFlag){
    if(v === 'chathospital'){
      froguePushEvent('clickEvent',{'name':'chathospital'});
    }else if(v === 'chatselftest'){
      froguePushEvent('clickEvent',{'name':'chatselftest'});
    }else{
      alert("여기 오면 안됩니다");
    }
  }
  return false;
}

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB5M-Svyk4D9E_TI8-AyUwgODkWb9s9gX8",
  authDomain: "img2code-326013.firebaseapp.com",
  databaseURL: "https://img2code-326013-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "img2code-326013",
  storageBucket: "img2code-326013.appspot.com",
  messagingSenderId: "585361370835",
  appId: "1:585361370835:web:d24e84715cef9eef706e26",
  measurementId: "G-HFRH590GDL"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const storageRef = firebase.storage().ref();

document.addEventListener('DOMContentLoaded', function () {
  let selectedFile;
  var selectedFile_Ext;

  // File 선택
  document.querySelector('#upload_img').addEventListener('change', e => {
    selectedFile = e.target.files[0];
    var selectedFile_split = selectedFile.name.split('.');
    selectedFile_Ext = selectedFile_split[1];
  });

  // File 업로드
  var today = new Date();
  var year = today.getFullYear();
  var month = ('0' + (today.getMonth() + 1)).slice(-2);
  var day = ('0' + today.getDate()).slice(-2);
  var hours = ('0' + today.getHours()).slice(-2); 
  var minutes = ('0' + today.getMinutes()).slice(-2);
  var seconds = ('0' + today.getSeconds()).slice(-2);
  var timestamp = year + month + day + hours + minutes + seconds;
  document.querySelector('#call-bot-btn').addEventListener('click', () => {
    storageRef
        .child(`Web_images/${timestamp}.${selectedFile_Ext}`)
        .put(selectedFile)
        .on('state_changed', snapshot => {
            console.log(snapshot);
          }, error => {
            console.log(error);
          }, () => {
            console.log('성공');
            alert("등록되었습니다");
            document.getElementById("name").value = timestamp;
        }
    );

    db.collection('trainingCollection').doc('trainingImage').collection(timestamp).doc('0').set({
      img :"gs://img2code-326013.appspot.com/Web_images/" +  timestamp + '.' + selectedFile_Ext
    });
  });
  // save_return_timestamp(timestamp);
});

function save_return_timestamp(timestamp){
  var _timestamp = timestamp
  return _timestamp
}

