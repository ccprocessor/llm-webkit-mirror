const Prism = require('prismjs');
const loadLanguages = require('prismjs/components/');
loadLanguages(['haml']);

// The code snippet you want to highlight, as a string
const code = `= ['hi', 'there', 'reader!'].join " "`;

// Returns a highlighted HTML string
const html = Prism.highlight(code, Prism.languages.haml, 'haml');