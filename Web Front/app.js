// index.js

const http = require("http");
const express = require("express");
const fs = require("fs");
const app = express();
const server = http.createServer(app);
const PORT = 8080;

const WEBPATH = "./view";

app.use('/public', express.static(__dirname + '/public'));

app.get("/", (req, res) => {
    fs.readFile(`${WEBPATH}/page1.html`, (error, data) => {
        if (error) {
            console.log(error);
            return res.status(500).send("<h1>500 Error</h1>");
        }
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log(`Server running on ${PORT}`);
});