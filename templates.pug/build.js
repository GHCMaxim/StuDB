const pug = require("pug");
const fs = require("fs");
const sourcePath = "templates.pug/";
const outputPath = "templates/";

if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath);
}

const files = fs.readdirSync(sourcePath).filter((file) => {
    return file.match(/\.pug$/);
});

files.forEach((file) => {
    const compiledFunction = pug.compileFile(sourcePath + file);
    const html = compiledFunction();
    fs.writeFileSync(outputPath + file.replace(/\.pug$/, ".html"), html);
});
