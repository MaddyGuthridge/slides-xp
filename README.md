# Slides XP

A simple but flexible markdown slide-show viewer.

## Running

```sh
sxp <directories to serve>
```

## Custom CSS

You can use the `--theme` option to specify the a built-in theme, or a path to
a directory containing CSS theme files.

* `main.css`: main stylesheet. Always loaded.
* `slide.css`: stylesheet for slide pages.
* `picker.css`: stylesheet for slide picker page.

These stylesheets are mounted at the `/theme` endpoint.

Within these stylesheets, the following classes can be selected.

* `.highlight`: code blocks
* `.slide-content`: slide content
* `.picker-box`: slide picker
* `.picker-item`: slide within slide picker

And the following variables are available:

* `--hl-comment`: code block highlighting, comment
* `--hl-doc`: code block highlighting, documentation
* `--hl-keyword`: code block highlighting, keyword
* `--hl-var`: code block highlighting, variable
* `--hl-func`: code block highlighting, function
* `--hl-type`: code block highlighting, type
* `--hl-string`: code block highlighting, string
