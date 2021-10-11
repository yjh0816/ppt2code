// node_modules 에 있는 express 관련 파일을 가져온다.
var express = require('express')

// express 는 함수이므로, 반환값을 변수에 저장한다.
var app = express()

// 8080 포트로 서버 오픈
app.listen(8080, function() {
    console.log("start! express server on port 8080")
})

// request 와 response 라는 인자를 줘서 콜백 함수를 만든다.
// localhost:8080 브라우저에 res.sendFile() 내부의 파일이 띄워진다.

app.get('/', function(req,res) {
  res.sendFile(__dirname + "/public/views/index.html")
})

// // localhost:8080/main 브라우저에 res.sendFile() 내부의 파일이 띄워진다.
// app.get('/main', function(req,res) {
//   res.sendFile(__dirname + "/public/views/page1.html")
// })

// public 디렉토리를 static으로 기억한다.
// public 내부의 파일들을 localhost:8080/파일명 으로 브라우저에서 불러올 수 있다.
app.use(express.static('public'))

//웹 서버 open 완료

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
