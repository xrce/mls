<div align="center">

# Movie Link Scraper

</div>

> [!TIP]
> Open issue if you found any bugs and contribute if you want to add more bugs

## Options

| Options | Name  | Description    |
| :-----: | ----- | -------------- |
| -s      | Site  | Site to scrape |
| -t      | Title | Movie title    |
| -l      | Limit | Search limit   |         |

## Installation
**PyPI :**
```
pip install movielinkscraper
```
**Repository :**
```
git clone https://github.com/xrce/mls
cd mls
pip install .
```

## Module Usage
```py
from mls import *

scrape = <site>
scrape.search(<title>, <limit>)
```
**Example :**
```py
from mls import *

scrape = LK21()
scrape.search("transformers", 3)
```

## Direct Usage
```
python -m mls -s <site> -t <title> -l <limit>
```
**Example :**
```
python -m mls -s LK21 -t sherlock
```
```
python -m mls -t "Incantation 2022" -l 2
```
