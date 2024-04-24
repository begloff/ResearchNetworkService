const router = require("express").Router();

router.use("/networkinfo", require("./networkinfo"));

module.exports = router;
