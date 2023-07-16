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

const htmlstring_to_html = (htmlstring) => {
    const div = document.createElement("div");
    div.innerHTML = htmlstring.trim();
    return div.firstChild;
};

files.forEach((file) => {
    const compiledFunction = pug.compileFile(
        sourcePath + file,
        (options = {
            filters: {
                table_type_filter: (text, options) => {
                    text = pug.render(text);
                    text = text.replace(/__table_type__/g, options.type);
                    text = text.replace(
                        /__Table_type__/g,
                        options.type.charAt(0).toUpperCase() +
                            options.type.slice(1),
                    );
                    text = text.replace(
                        /__TABLE_TYPE__/g,
                        options.type.toUpperCase(),
                    );
                    return text;
                },
            },
        }),
    );

    fs.writeFileSync(
        outputPath + file.replace(/\.pug$/, ".html"),
        compiledFunction(),
    );
});
