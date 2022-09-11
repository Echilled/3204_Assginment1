import whois
from nslookup import Nslookup
import re
from requests_html import HTMLSession
import html

domain = "example.com"


def email_extractor(url):
	url = "https://www.generatormix.com/random-email-addresses"
	EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
	session = HTMLSession()
	r = session.get(url)
	r.html.render()
	for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
		print(re_match.group())


def main():
	# print("hi")
	# w = whois.whois(domain)
	# # print(w)
	#
	# dns_query = Nslookup()
	# ips_record = dns_query.dns_lookup(domain)
	# print(ips_record.response_full, ips_record.answer)
	email_extractor("https://www.randomlists.com/email-addresses")


if __name__ == "__main__":
	main()