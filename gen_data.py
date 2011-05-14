def generate_dict(amount = 10, num = 0, rec = 0, keynum = 0, spec_val = None):
	''' generates long json message
	amount, rec = amount of keys in dictionary, recursion level
	spec_val - if evaluates to True then it will be used as value of key '''
	lst = ['{',]
	for i in range(amount):
		if not rec:
			val = spec_val or '"%s"' % num 
			num += 1
		else: 
			val, num, keynum = generate_dict(rec = rec - 1, num = num, keynum = keynum, spec_val = spec_val)
		keyname = "key"*1000
		key = '"%s%s"' % (keyname, keynum)
		keynum += 1
		lst.append ('%s:%s%s' % (key, val, i<amount-1 and ',' or ''))
	lst.append ('}')
	return ''.join(lst), num, keynum


if __name__ == '__main__':
	def write_file(name, cont):
		f = open (name, 'w')
		f.write (cont)
		f.close ()

	msg = generate_dict ()[0]
	write_file ('test_msg.py', "msg = '%s'" % msg)

	regex = generate_dict (spec_val = '"(\w+)"')[0]
	write_file ('test_regex.py', "msg_regex = '%s'" % regex)



