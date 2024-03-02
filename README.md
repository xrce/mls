<div align="center">

# Movie Link Scraper

</div>

> [!TIP]
> Open issue if you found any bugs and contribute if you want to add more bugs

## Available Sites

| Code        | Name                                         | Status |
| ----------- | -------------------------------------------- | :----: |
| **LK21**    | [LayarKaca21](https://amp.lk21official.mom/) | ✅    |
| **NKP**     | [Nekopoi](https://nekopoi.care/)             | ✅    |
| **REBAHIN** | [REBAHIN](http://179.43.169.211/)            | ✅    |
| **IMDB**    | [IMDB](https://www.imdb.com/)                | ✅    |

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
