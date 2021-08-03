var express = require('express');

var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});

var bodyParser = require('body-parser');
const { equal } = require('assert');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 4500);

app.use(express.static(__dirname+ '/public'));


const mariadb = require('mariadb');
const pool = mariadb.createPool({
  host: 'classmysql.engr.oregonstate.edu',
  user: 'cs361_haneyad',
  password: 'PussyEater898!',
  database: 'cs361_haneyad',
  connectionLimit: 5
});

pool.getConnection()
    .then(conn => {
    
      conn.query("SELECT 1 as val")
        .then((rows) => {
          console.log(rows); //[ {val: 1}, meta: ... ]
          //Table must have been created before 
          // " CREATE TABLE myTable (id int, val varchar(255)) "
          return conn.query("INSERT INTO myTable value (?, ?)", [1, "mariadb"]);
        })
        .then((res) => {
          console.log(res); // { affectedRows: 1, insertId: 1, warningStatus: 0 }
          conn.end();
        })
        .catch(err => {
          //handle error
          console.log(err); 
          conn.end();
        })
        
    }).catch(err => {
      //not connected
    });

app.get('/', function(req,res){
  res.render('index');
});

app.get('/jobsearch', function(req,res){
  res.render('jobsearch');
});

app.post('/execute',function(req,res,next){
  myQuery = req.body["keyword"];
  console.log("myQuery is: ", myQuery);
  
  pool.getConnection()
    .then(conn => {
      conn.query("SELECT id, last_update, location, name, url FROM cl_jobsdata WHERE name like (?)", '%' + myQuery + '%')
        .then((rows) => {
          console.log(rows);
          res.json(rows);
          return conn.query("SELECT id, last_update, location, name, url FROM cl_jobsdata WHERE name like (?)", '%' + myQuery + '%');
        })
        .then((res) => {
          console.log(res); 
          conn.end();
        })
        .catch(err => {
          //handle error
          console.log(err); 
          conn.end();
        })
        
    }).catch(err => {
      //not connected
    });
  });

app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});

