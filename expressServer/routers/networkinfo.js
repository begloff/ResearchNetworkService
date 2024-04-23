const router = require("express").Router();
const fs = require("fs");
const path = require("path");

const postNetworkInfo = (req, res) => {
  console.log("Received Network Info POST request");

  const currentDate = new Date().toISOString().slice(0, 10); // Get current date in yyyy-mm-dd format
  const currentTime = new Date().toISOString(); // Get current time in ISO format

  const outputFolderPath = path.resolve(__dirname, "..", "outputFiles"); // Get absolute path to outputFiles folder
  const fileName = path.join(outputFolderPath, `${currentDate}.json`); // File name with current date

  // Read existing data from file if it exists, otherwise initialize as an empty object
  let jsonData = {};
  if (fs.existsSync(fileName)) {
    const fileData = fs.readFileSync(fileName, "utf8");
    jsonData = JSON.parse(fileData);
  }

  // Append new data to the object with current time as the key
  jsonData[currentTime] = req.body;

  // Write updated data back to the file
  fs.writeFile(fileName, JSON.stringify(jsonData, null, 2), (err) => {
    if (err) {
      console.error("Error writing file:", err);
      res.status(500).send("Error writing file");
    } else {
      console.log(`Data appended to ${fileName}`);
      res.status(200).send("Success");
    }
  });
};

router.post("/", postNetworkInfo);

module.exports = router;
