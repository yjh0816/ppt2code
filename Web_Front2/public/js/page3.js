var burger = $('#menu-trigger');

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

// 파이어스토어
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
const storage = firebase.storage()


$(document).ready(function(){
  // 20211009210629.png를 timestamp와 fileExt 로 변경해야 함
  // index.js에서 가져와야합니다
  // var pathRef = storage.ref('Web_images/20211009210629.png');
  // var gsRef = storage.refFromURL('gs://img2code-326013.appspot.com/Web_images/' + '20211009210629.png');
  // var httpsRef = storage.refFromURL('https://https://firebasestorage.googleapis.com/v0/b/img2code-326013.appspot.com/o/Web_images%2F20211009210629?');

});