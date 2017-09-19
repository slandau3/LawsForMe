
var express = require('express');
var router = express.Router();
var pg = require('pg');

/* GET home page. */
router.get('/', function(req, res, next) {
    console.log(" I AM HERE");
  res.render('login');
});

module.exports = router;
