# WARNING
**THIS PROGRAM IS BLOATED __AS HELL__: PLEASE AVOID USING IT**

# dtcli

## Introduction

DTCli is a tool to query jokes from three websites : DTC ([DansTonChat](https://danstonchat.com/)), NSF ([NuitSansFolie](https://nuitsansfolie.com/)) and [bash.org](http://bash.org/). Because I'm French, two of the websites are french (only [bash.org](http://bash.org/) is in english).

## Installation

Using [pipx](https://pipxproject.github.io/pipx/) : 

```shell
pipx install ./
```

## Options

- `-h/--help` : Pretty self explanatory : Print the help message.
- `-v/--verbose` : Print verbose informations : errors, informations...
- `-i/--ignore` : Continue even if the URL tested is giving an error. Same for errors during the processing of the text.
- `--version` : Print the version of the script
- `-n/--number` : Specify the number of the joke you want to get. Of course, must be a number. Specifying this cancel any title/lines related options. Use default website or, if passed, the specified one.
- `-b/--hide-banner` : Choose to hide the banner containing the informations about the joke printed. Doing so also hide the title if there's one.
- `-t/--hide-title` : Choose to hide the title of the DTC. Doing so doesn't hide the rest of the banner.
- `-f/--force-title` : Search only for a DTC with a title. This option doesn't do anything if the website is NSF or QDB.
- `-l/--lines` : Works only for DTC and QDB, search only for the jokes containing a specific number of lines.
- `-o/--over` : Works only for DTC and QDB, search only for the jokes containing over (inclusive) a specific number of lines
- `-u/--under` : Works only for DTC and QDB, search only for the jokes containing under (inclusive) a specific number of lines.
- `-w/--website` : Specify the website you want to take the jokes from. The possible values are `dtc`, `nsf`, `bash`.

## To Do

- [ ] Enhance NSF displaying (wrapping it better, cutting on `:` ?).
- [ ] Reorganise the code (Of course...).
- [ ] Comment the code.
- [ ] Enhance installation (Posting it on PyPi).
- [ ] Make it faster, it's so slooooooow.
  - [ ] Implement caching of jokes.
  - [ ] Implement caching of max number, based on the date.
- [x] Check for new posts on websites, and get the max allowed number.
- [x] Add module annotations.
- [x] Add module and function docstring.
- [x] Rework NSF, it seems to cause unknown problem : `Error 104, Connection reset by peer`



## License
MIT, refer to [LICENSE](https://github.com/Luc-Saccoccio/dtcli/blob/master/LICENSE) for complete text
