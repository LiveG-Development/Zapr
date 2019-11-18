# Zapr
Zapr, the app-building system for LiveG.

This repository is licensed by the [LiveG Open-Source Licence](https://github.com/LiveG-Development/Zapr/blob/master/LICENCE.md).

Zapr is a command-line tool that allows you to easily, effectively and efficiently build, compile and minify HTML, CSS and JavaScript-made apps and sites. Making apps can be done with just JavaScript, and allows you to easily import libraries designed for Zapr. The built app will be available as a single compressed HTML file, holding all of the code and assets needed to be supported as a standalone file. Making sites can be done with HTML, and optionally CSS and JavaScript. HTML files can be constructed similarly to that of JavaScript files, allowing you to import other HTML files directly. Localisation support is also built-in for static sites.

## Add to PATH in Bash
If you would like to use Zapr wherever you are in your terminal, you should add Zapr to your PATH:

1. Open up the file at `~/.bashrc` in your favourite text editor.
2. Right at the very bottom, add:
    ```bash
    export PATH="$PATH:/path/to/zapr"
    ```
    Where of course `/path/to/zapr` is the directory path which Zapr is contained in (and not the actual `zapr` file).
3. Logout and in again (or just open up a new terminal session), and use zapr by just typing `zapr`!

## Available commands and features
Below is a list of commands that you can use in Zapr, and the features that they bring.

### `--hide` (argument)
temporarily hide the header that appears when a Zapr command is run. This can be automated by setting the `hide` variable to `true`.

Aliases: `-h`

### `help`
```
help        Display this help screen.
```

Display the help screen that is a simpler equivalent to this section.

Aliases: `--help`, `/?`

### `var`
```
var         Read, set or delete variables.
            <name>              Read data contained in variable.
            <name> <data>       Write data to variable.
            <name> --delete     Delete variable.
```

Read, set or delete variables stored for usage with Zapr. Please see [List of useful Zapr variables](https://github.com/LiveG-Development/Zapr#list-of-useful-zapr-variables) for a list of useful variables and their descriptions.

Variables are stored as plain files in `~/.zaprset`, along with the `cache` folder.

### `build`
```
build       Build files in directory and output them to the `build` subdirectory.
            app                 Build files as final app.
            static              Build files as final static site.
```

Build files in the current directory and output the final built files in the `build` subdirectory. You will need to have a valid `manifest.json` in the directory so that the build can be made.

### `docgen`
```
docgen      Generate documentation for Zapr JavaScript libraries to the `docs` subdirectory.
```

Generate documentation for Zapr JavaScript libraries stored in the current directory and subdirectories. The generated documentation will be stored as JSON files in the `docs` subdirectory.

## List of useful Zapr variables
Here's a good list of useful Zapr variables:

| Name       | Description                                                                          |
|------------|--------------------------------------------------------------------------------------|
| `hide`     | Hide the Zapr notice every time you invoke Zapr (must be set to `true` to enable).   |
| `locale`   | Set the locale name (for example, `en_GB`).                                          |
| `useCache` | Enable cache storage for online imports (default `true`, set to `false` to disable). |

## Manifest templates
Below is the templates for `manifest.json` files which are required for building your Zapr project.

### App
```json
{
    "package": "com.example.testpackage",
    "version": "1.0.0",
    "name": {
        "en_GB": "Test Package"
    },
    "description": {
        "en_GB": "A sample package which is buildable with Zapr."
    },
    "defaultLocale": "en_GB",
    "mainScript": "script.js"
}
```

> **Note:** With this manifest, you'll need 1 file to build the app: `script.js`.

### Static
```json
{
    "urlFormat": "/<locale>/<path>",
    "defaultLocale": "en_GB",
    "staticFiles": "static",
    "localeFiles": "locale",
    "rootFiles": "root"
}
```

> **Note:** With this manifest, you'll need 3 subdirectories to build the static site: `static`, `locale` and `root`.

## Locale template
The locale template shown here is primarily made for static sites, but is also compatible with the `l10n` Zapr library.

```json
{
    "friendlyName": "English (United Kingdom)",
    "friendlyNameShort": "English",
    "direction": "ltr",
    "strings": {
        "hello": "Hello!",
        "paragraph": "This is a test paragraph."
    }
}
```
