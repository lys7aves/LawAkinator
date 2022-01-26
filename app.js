/* socket\app.js */
const app = require("express")();
const http = require("http").createServer(app);
require("dotenv").config();
const { spawn } = require("child_process");
const io = require("socket.io")(http, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

let fin = false;

const results = [
  "판례 A와 연관이 있습니다",
  "판례 B와 연관이 있습니다",
  "판례 C와 연관이 있습니다",
  ,
  "판례 D와 연관이 있습니다",
  ,
  "판례 E와 연관이 있습니다",
];
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

io.on("connection", (socket) => {
  let dataTosend;
  const python = spawn("python", ["./src/main.py"]);
  console.log("a user connected");

  /*socket.on("send message", (item) => {
    const msg = item.name + ":" + item.message;
    let msg1 = dataTosend;
    console.log("msg:  " + msg);
    io.emit("receive message", { name: item.name, message: item.message });
  });*/
  socket.on("request question", () => {
    console.log("request question");
    python.stdout.on("data", (data) => {
      dataTosend = data.toString();
      console.log(dataTosend);
      io.emit("receive question", `${dataTosend}`);
    });
  });
  socket.on("answer", (payload) => {
    console.log(payload);

    python.stdin.write(payload.answer + "\n");
    python.stdout.on("data", (data) => {
      dataTosend = data.toString();
      if (dataTosend == "fin\n") {
        fin = true;
      } else if (fin) {
        io.emit("result", dataTosend);
        fin = false;
      } else {
        io.emit("receive question", dataTosend);
      }
    });
  });
  socket.on("disconnect", () => {
    console.log("user disconnected", socket.id);
    python.kill();
  });
});
http.listen(process.env.PORT, (PORT) => {
  console.log(`Connected at ${process.env.PORT}`);
});
