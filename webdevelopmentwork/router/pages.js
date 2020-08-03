const express= require("express");
var router =express.Router();
const mysql =require('mysql');
var authconroller =require('../controller/auth')
//const connection =require('../dib/dbsql');
const { check, validationResult } = require('express-validator');
const connection = require('../dib/dbsql')

//former registration form
router.get("/farmerregistration",function(req,res){
    res.render("farmerregform",{message:''});
});
router.post("/",function(req,res){
/* [check('myaadhar').isLength({ min: 12 }),check('myaadhar').isNumeric()],
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(422).json({ errors:'Aadhar should be of length 12' })
  }*/
 let data ={ID:req.body.myadhar,Name:req.body.myname,BANKACCOUNT:req.body.mybank,LANDRECORD:req.body.myland,CROP1:req.body.crop1,CROP2:req.body.crop2,CROP3:req.body.crop3,CROP4:req.body.crop4	};
 // let data ={ Name:req.body.myname,ID:req.body.myaadhar,BANKACCOUNT:req.body.mybank,LANDRECORD:req.body.myland,CROP1:req.body.crop1,CROP2:req.body.crop2,CROP3:req.body.crop3,CROP4:req.body.crop4};
  var sql ="INSERT INTO farmer  SET ?";
   connection.query(sql,data,function(error,results,fields){
   console.log(results);
   res.redirect("/");
 });
});
//former registration
/*
router.post('/farmerregistration',(req,res)=>{
    
    let data = {Name:req.body.name,Aadhar:req.body.Aadhar,LandRecord_no:req.body.Aadhar,Bank_account_no:req.body.Aadhar,
        Area_of_land:req.body.Aadhar, Latitude:req.body.Aadhar,Longitude:req.body.Aadhar,SoilType:req.body.Aadhar,	Mobile_no:req.body.Aadhar,
        Address:req.body.Aadhar	};
  let sql ="INSERT INTO farmers  SET ?";
  connection.query(sql, data,function (error, results, fields) {
    if (error) throw error;
    //req.flash('message', 'Success!!');
    res.redirect("/",{message:"farmer registered"});
	});
}); 
//former login
router.get("/farmerlogin",function(req,res){
    res.render("login");
  });*/
router.post("/farmerlogin",authconroller.farmerlogin);

router.get('/admin',(req,res)=>{
    res.render("adminlogin");
});
//for shop registration
router.get('/shops',(req,res)=>{
  connection.query('select * from shops', function (error, results, fields) {
	  if (error) throw error;
    res.render("shops",{shops:results});
});
});
router.get("/shops/new",(req,res)=>{
    res.render("shopreg");
});

router.get('/shops/:id', function (req, res) {
    console.log(req);
    var ShopId= req.params.id;
    var sql=`SELECT * FROM shops WHERE id =`+ShopId;
    connection.query(sql ,function (error, results, fields){
     if (error) throw error;
     var x ={
      shops:results[0]
     }
     res.render('shop',x);
   });
  });
  
  //rest api to create a new record into mysql database
  router.post('/shops', function (req, res) {
    // var name  = req.body.employee_name;
    // var sallery  = req.body.employee_salary;
    // var age = req.body.employee_age;
    // var sql ='INSERT INTO `employees` (`id`, `employee_name`, `employee_salary`, `employee_age`) VALUES (NULL, name, sallery, age);
    let data = {ShopName:req.body.ShopName,Address:req.body.Address,Contact_No:req.body.Contact};
    let sql ="INSERT INTO shops  SET ?";
    connection.query(sql, data,function (error, results, fields) {
      if (error) throw error;
      //req.flash('message', 'Success!!');
      res.redirect("/");
      });
  });
//seed booking
router.get('/seedbooking',(req,res)=>{
  res.render("seedbooking");
});
router.post("/seedbooking",(req,res)=>{
  let data = {FarmerId:req.body.id,	FarmerName:req.body.name,Address:req.body.add,CropName:req.body.Crop,Aadhar:req.body.aadhar};
  let sql ="INSERT INTO seedbooking  SET ?";
    connection.query(sql, data,function (error, results, fields) {
      if (error) throw error;
      //req.flash('message', 'Success!!');
      res.redirect("/");
      });
});

router.get("/help",(req,res)=>{
  res.render('help1');
});

router.get("/phase",(req,res)=>{
  res.render('phaselogin',{errors:""});
});
router.post("/phaselogin",[check('FarmerId').isLength({ min: 12 }),
check('FarmerId').isNumeric()],authconroller.phase);
router.post("/phase",(req,res)=>{
  res.redirect("/");
});
router.get("/phasequestion",(req,res)=>{
  res.render("phasequestions");
});
router.get("/sellquestion",(req,res)=>{
  res.render("sellform");
});
router.get("/sell",(req,res)=>{
  res.render('cropsell',{errors:""});
});
router.post("/selllogin",[check('FarmerId').isLength({ min: 12 }),
check('FarmerId').isNumeric()],authconroller.sell);
router.post("/sell",(req,res)=>{
  res.redirect("/");
});
router.post("/sellform",authconroller.sellform);
router.get("/advise",(req,res)=>{
  res.render('advisory');
});
router.get("/showing",(req,res)=>{
  res.render("showing");
});
router.get("/landprep",(req,res)=>{
  res.render("landpreperation");
});
router.get("/irrrigation",(req,res)=>{
  res.render("irrigation");
});
router.get("/harvest",(req,res)=>{
  res.render("harvesting");
});
module.exports =router;
