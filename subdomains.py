from supermo.core.subdomain import subdomain

if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options] target.com', version="%prog 1.0.6")
    parser.add_option('-f', dest='file', default='subnames.txt',
                      help='File contains new line delimited subs, default is subnames.txt.')
    parser.add_option('--full', dest='full_scan', default=False, action='store_true',
                      help='Full scan, NAMES FILE subnames_full.txt will be used to brute')
    parser.add_option('-i', '--ignore-intranet', dest='i', default=False, action='store_true',
                      help='Ignore domains pointed to private IPs')
    parser.add_option('-t', '--threads', dest='threads', default=100, type=int,
                      help='Num of scan threads, 100 by default')
    parser.add_option('-o', '--output', dest='output', default=None,
                      type='string', help='Output file name. default is {target}.txt')

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    d = subdomain.subdomain(target=args[0], options=options)
    d.run()
    d.outfile.flush()
    d.outfile.close()