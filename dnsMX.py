import dns.resolver

a = input("Enter target:")


answers = dns.resolver.query(a, 'MX')

for rdata in answers: 
	print "Host", rdata.exchange, 'has preference', rdata.preference