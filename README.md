# dtcli

## Introduction

DTCli is a tool to query jokes from three websites : DTC ([DansTonChat](https://danstonchat.com/)), NSF ([NuitSansFolie](https://nuitsansfolie.com/)) and [bash.org](http://bash.org/). Because I'm French, two of the websites are french (only [bash.org](http://bash.org/) is in english).

## Installation

WIP

## Configuration

By default, the tool query either DTC or bash.org according to system language. A YAML configuration file can be used to set the language ('fr' or 'en'), the website ('dtc', 'nsf', 'bash.org') to use, hiding or not the banner or the title (only works for DTC). You can create the default one using the tool, or copying it : 
```yaml
hide_banner: false
hide_title: false
language: null
website: null
```

## License
MIT, refer to [LICENSE](https://github.com/Recidiviste/dtcli/blob/master/LICENSE) for complete text
