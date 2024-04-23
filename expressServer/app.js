// app.js
const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.options("*", cors());

app.use((req, res, next) => {
  express.json()(req, res, next);
});
app.use("/api/v1", require("./routers"));

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server started on port ${port}`));
