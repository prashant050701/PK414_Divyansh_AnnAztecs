const mysql =require('mysql');
const conn =require('../dib/dbsql');
const { check, validationResult } = require('express-validator');
exports.farmerlogin =async(req,res)=>{
    var x =req.body.myaadhar;
    var sql='SELECT * FROM farmers WHERE ID ='+x;
  conn.query(sql ,function (error, results, fields){
   if (error) throw error;
   var x ={
    farmer:results[0]
   }
  //res.render('farmers',x);
  res.render('farmers',x);
   console.log(x.farmer);
 });
}
exports.phase =(req,res)=>{ 
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.render('phaselogin',{ errors:'Please enter correct FarmerId Or Password '});
  }
   res.render('phasequestions');
}
exports.sell =(req,res)=>{ 
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.render('cropsell',{ errors:'Please enter correct FarmerId Or Password '});
  }
   res.render('sellform');
}
exports.sellform =(req,res)=>{
  var x=req.body.name;
  var y =Math.floor(Math.random() * 1000000000);

  res.render('sellinvoice',{name:x,refno:y});
}
