var app = require('http').createServer(handler)
  , io = require('socket.io').listen(app)
  , fs = require('fs')
  , spawn = require('child_process').spawn;

app.listen(8080);

function handler (req, res) {
  fs.readFile(__dirname + '/index.html', function (err, data) {
    res.writeHead(200);
    res.end(data);
  });
}

io.sockets.on('connection', function (socket) {
  var shell = spawn('bash')
    , output = function (msg) {
        socket.emit('output', msg.toString());
      };

  shell.stdout.on('data', output);
  shell.stderr.on('data', output);
  shell.on('close', function () {
    output('Exit');
    socket.disconnect(true);
  });

  socket.on('input', function (data) {
    shell.stdin.write(data);
  });

  socket.on('disconnect', function () {
    shell.kill('SIGKILL');
  });
});
