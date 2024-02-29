import argparse
from .mls import LK21, NKP

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape download links from any site')
    parser.add_argument('-s', type=str, help='Site', dest='site')
    parser.add_argument('-t', type=str, help='Title', dest='title')
    parser.add_argument('-l', type=str, help='Limit', dest='limit')

    args = parser.parse_args()
    site = "LK21" if not args.site else args.site
    title = input("Input title : ") if not args.title else args.title
    limit = None if not args.limit else args.limit
    
    match site.upper():
        case "NKP": scrape = NKP()
        case "LK21": scrape = LK21()
    
    scrape.search(title, limit)