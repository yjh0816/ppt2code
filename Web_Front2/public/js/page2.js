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
var firebaseConfig = {
  apiKey: "AIzaSyAtPYuQ_fwUYqHODqaAL-Gm914JWaXAS1g",
  authDomain: "corokinatior.firebaseapp.com",
  projectId: "corokinatior",
  storageBucket: "corokinatior.appspot.com",
  messagingSenderId: "880560377780",
  appId: "1:880560377780:web:32a70cfdc6d58b8ec26ce1",
  measurementId: "G-YGXFC15397"
};
firebase.initializeApp(firebaseConfig);

const db = firebase.firestore();

const tmplist = [];

const getData = async () => {
  await db.collection("statusByRegion").get().then(function (querySnapshot) {
    querySnapshot.forEach(function (doc) {
      // console.log(doc.id, " => ", doc.data());
      tmplist.push(doc.data());
    });
  });

  let regionName = $("#local #local-container #map #main_maplayout button .name");
  let rankNum = $("#local #local-container #map #main_maplayout button .num");
  for (var i = 0; i < regionName.length; i++) {
    // console.log(regionName[i].innerText);
    for (var j = 0; j < tmplist.length; j++) {
      if (regionName[i].innerText === tmplist[j].location) {
        rankNum[i].innerText = tmplist[j].step;
      }
    }
  }
}
getData();

function changecolor() {
  var btn = $("#local #local-container #map #main_maplayout button");
  // var btnname = $("#local #local-container #map #main_maplayout button data-city");
  // var targetRegion = $("#local #local-container #table #targetRegion");
  // var targetStep = $("#local #local-container #table #targetStep");

  btn.click(function () {
    btn.removeClass('local-select');
    $(this).addClass('local-select');

  });
}
changecolor();

function changeData(data) {
  //넣을 위치
  var targetRegion = $("#local #local-container #table #targetRegion");
  var targetStep = $("#local #local-container #table #targetStep");

  //선택내용
  var selectRegion = $("#local #local-container #map #main_maplayout button .name");
  var selectStep = $("#local #local-container #map #main_maplayout button .num");
  // console.log(selectRegion[data].innerText);

  targetRegion.text(selectRegion[data].innerText);
  targetStep.text(selectStep[data].innerText);

  getGuideline(selectStep[data].innerText);
}

//지침 내용 컬렉션 가져오기
const wherelist = [];
// const firstGuide = [];
// const secondGuide = [];
// const thirdGuide = [];

const firstStep = db.collection('guidelineByStep').doc('capital').collection('1.5');
const secondStep = db.collection('guidelineByStep').doc('capital').collection('2.0');
const thirdStep = db.collection('guidelineByStep').doc('capital').collection('2.5');

const getGuideline = async (step) => {
  var guide = [];

  if(step==='1.5'){
    // console.log("1.5단계");
    await firstStep.get().then(function (querySnapshot) {
      querySnapshot.forEach(function (doc) {
        // console.log(doc.id, " => ", doc.data());
        wherelist.push(doc.id);
        guide.push(doc.data());
      });
    });
  }else if(step==='2'){
    // console.log("2.0단계");
    await secondStep.get().then(function (querySnapshot) {
      querySnapshot.forEach(function (doc) {
        wherelist.push(doc.id);
        guide.push(doc.data());
      });
    });
  }else{
    // console.log("2.5단계");
    await thirdStep.get().then(function (querySnapshot) {
      querySnapshot.forEach(function (doc) {
        wherelist.push(doc.id);
        guide.push(doc.data());
      });
    });
  }

  //넣을 위치
  // var targetWhere = $("#local #local-container #table #stepWhere");
  var target = $("#local #local-container #table #stepContents"); //div
  target.empty();

  var sentence = '';
  for (var i = 0; i < guide.length; i++) {
    sentence += "<p name=\"added\" style=\"margin-bottom:12px;\">" + wherelist[i] + "은 ";
    if (guide[i].available) {
      if(guide[i].note !== ""){
          if(guide[i].time !== -1){
            sentence += "가도 되지만, " + guide[i].note + "되고, "+ guide[i].time + "시까지만 돼요.</p>";
            // sentence += "가도 되지만, " + guide[i].time + "시까지만 돼요.</p>";
          }else{
            sentence += "가도 되지만, " + guide[i].note + "일 때만 돼요.</p>";
          }
      }else{
        sentence += "갈 수 있어요.</p>";
      }
    } else {
      sentence += "가면 안돼요.</p>";
    }
  }
  
  target.append(sentence);
}
changeData(0);