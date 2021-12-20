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
var target_id = getParameterByName('name');
var click_id = 0;
function getParameterByName(name) { 
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]"); 
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search); 
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " ")); 
}

$(document).ready(function(){
  //20211020043157를 target_id 로 변경
  db.collection('trainingCollection').doc("trainingImage").collection(target_id).get().then((snapshot) => {
    snapshot.forEach((target_doc) => {
      var target_top = target_doc.data().position[2];
      var target_left = target_doc.data().position[0];
      var target_width = target_doc.data().position[1] - target_doc.data().position[0];
      var target_height = target_doc.data().position[3] - target_doc.data().position[2];
      var target_url = target_doc.data().image_url;

      var target_html = '<button class = "target" id = "' + target_doc.id + '" style = "top : ' + target_top + 'px; left : ' + target_left + 'px; width : ' + target_width  + 'px; height : ' + target_height + 'px; background-image : url('
      + target_url + ');">'+  target_doc.id + '</button>';
      $('.target-box').append(target_html);
    })
  });
  var origin_img_html = '<img src = "https://firebasestorage.googleapis.com/v0/b/img2code-326013.appspot.com/o/Web_images%2F' + target_id + '.png?alt=media"/>';
  $("#origin_img").append(origin_img_html);
});

$(document).on('click','.target',function(){
  click_id = $(this).attr('id');
  $(".popup_box").show();
  
  // 팝업 중앙 정렬
  var $layerPopup = $(".popup_box");
  var left = ($(window).width() - $layerPopup.width()) - 200  ;
  var top = ($(window).scrollTop() + ($(window).height() - $layerPopup.height()) / 2 );
  $layerPopup.css({ "left": left, "top":top, "position": "absolute" });
  $("body").css("position", "relative").append($layerPopup);

  //태그 샐랙트
  $('.p_title').text(click_id);
  $(this).css("border", "3px solid red");
});

$(document).on('click','.btn_close',function(){
  $("#" + click_id).css("border", "1px solid black");
  $(".popup_box").hide();
});

$(document).on('click','.btn_submit',function(){
  var target_tag = $('#popup_tag').val();
  db.collection('trainingCollection').doc("trainingImage").collection(target_id).doc(click_id).update({ tag : target_tag });
  $(".popup_box").hide();
  $("#" + click_id).css("display", "none");
});
