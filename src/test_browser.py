from anonbrowser import AnonBrowser
from sys import argv

if __name__ == "__main__":
    test_browser = AnonBrowser(use_soup=True)
    if len(argv) > 1 and argv[1] == "rotate": 
        print("Starting IP: {}".format(test_browser.check_ip()))
        limit = int(argv[2]) if len(argv) > 2 else 3
        for _ in range(limit):
            test_browser._rotate_ip()
    else:
        page = test_browser.get("http://cadelwatson.com/")
        print(page)