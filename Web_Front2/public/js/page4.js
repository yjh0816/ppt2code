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
const storageRef = firebase.storage().ref();
var target_id = getParameterByName('name');
var click_id = 0;
function getParameterByName(name) { 
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]"); 
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search); 
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " ")); 
}

$(document).ready(function(){
  
  // var origin_img_html = '<img src = "https://firebasestorage.googleapis.com/v0/b/img2code-326013.appspot.com/o/Web_images%2F' + target_id + '.png?alt=media"/>';
  // $("#origin_img").append(origin_img_html);

  storageRef.child('tmp2/tree.html').getDownloadURL().then(function(url){
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.onload = function() {
      var a = document.getElementById('code_download');
      a.href = window.URL.createObjectURL(xhr.response);
      a.download = "result.html"; // Name the file anything you'd like.
    };
    
    xhr.open('GET', url);
    xhr.send();

    $(".target-box").load(url, function(){
      var result_code = $(".target-box").html();
      console.log(html_beautify(result_code));
      // window.html_beautify = function(html_source) {
      //   return style_html(html_source);
      // };
      $("#target_text").text(html_beautify(result_code));
    });

  }).catch(function(error) {
    console.log(error.code);
    switch (error.code) {
      case 'storage/object-not-found':
        // File doesn't exist
        break;
  
      case 'storage/unauthorized':
        // User doesn't have permission to access the object
        break;
  
      case 'storage/canceled':
        // User canceled the upload
        break;
  
      case 'storage/unknown':
        // Unknown error occurred, inspect the server response
        break;
    }
  });
});

{/* <script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify-css.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify-html.min.js"></script>
<script src="/tools/js/sql-formatter.js"></script>
  */}
// $(document).ready(function(){
//   // 변환 버튼
//     var source = $("#target_text").val();
//     var output = "";
    
//     if(source == ""){
//       alert("원본 코드를 입력해주세요.");
//       return;
//     }
    
//     if (looks_like_html(source)){
//       output = html_beautify(source);
//     }
//     $("#beautifyText").text(output);
    
// });

// function looks_like_html(source) {
//   var trimmed = source.replace(/^[ \t\n\r]+/, '');
//   return trimmed && (trimmed.substring(0, 1) === '<');
// }
