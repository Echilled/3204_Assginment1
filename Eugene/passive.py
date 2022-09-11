import whois
from nslookup import Nslookup

domain = "example.com"


def main():
	print("hi")
	w = whois.whois(domain)
	print(w)


main()