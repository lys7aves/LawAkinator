/* socket\app.js */
const app = require("express")();
const http = require("http").createServer(app);
const { spawn } = require("child_process");
const io = require("socket.io")(http, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

io.on("connection", (socket) => {
  let dataTosend;

  console.log("a user connected");
  const python = spawn("python", ["test.py"]);
  python.stdout.on('data', (data) => {
    dataTosend = data.toString();
    console.log("py well done" + dataTosend);
  });
  /*socket.on("send message", (item) => {
    const msg = item.name + ":" + item.message;
    let msg1 = dataTosend;
    console.log("msg:  " + msg);
    io.emit("receive message", { name: item.name, message: item.message });
  });*/
  socket.on("request question", () => {
    console.log("request question");
    let msg = dataTosend;
    console.log(`msg: ${msg}`);
    io.emit("receive question", "~와 연관이 있습니까?");
  });
  socket.on("answer", (number) => {
    io.emit("result", "판례 A와 연관이 있습니다");
    console.log("number", number);
  });
  socket.on("disconnect", () => {
    console.log("user disconnected", socket.id);
  });
});
http.listen(5000, () => {
  console.log("Connected at 5000");
});
