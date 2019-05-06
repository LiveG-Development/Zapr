# Zapr
Zapr; the app-building system for LiveG.

This repository is licensed by the [LiveG Open-Source Licence](https://github.com/LiveG-Development/Zapr/blob/master/LICENCE.md).

## Add to PATH in Bash
If you would like to use Zapr wherever you are in your terminal, you should add Zapr to your PATH:

1. Open up the file at `~/.bashrc` in your favourite text editor.
2. Right at the very bottom, add:
    ```bash
    export PATH="$PATH:/path/to/zapr"
    ```
    Where of course `/path/to/zapr` is the directory path which Zapr is contained in (and not the actual `zapr` file).
3. Logout and in again (or just open up a new terminal session), and use zapr by just typing `zapr`!

## List of useful Zapr variables
Here's a good list of useful Zapr variables:

| Name      | Description                                                                        |
|-----------|------------------------------------------------------------------------------------|
| hide      | Hide the Zapr notice every time you invoke Zapr (must be set to `true` to enable). |
| locale    | Set the locale name (for example, `en_GB`).                                        |