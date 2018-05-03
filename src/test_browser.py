from anonbrowser import AnonBrowser

if __name__ == "__main__":
    test_browser = AnonBrowser()
    print(test_browser.check_ip())
    test_browser._rotate_ip()
    print(test_browser.check_ip())
