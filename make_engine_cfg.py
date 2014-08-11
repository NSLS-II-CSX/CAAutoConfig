import argparse
from CAAutoConfig.utils import findFiles 
from sys import stdout, exit

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--source', action='store', type=file, required=True, help='PV list')
parser.add_argument('-g', '--group', action='store', required=True,\
                        help='location (eg: \'11IDA\')')
parser.add_argument('-d', '--destination', action='store', help='defaults to \'./engine.xml\'.')
parser.add_argument('-r', '--regex', action='store', required=True)
parser.add_argument('-m', '--monitor', action='store', default=True)
parser.add_argument('-p', '--period', action='store', default=1.0)

engine_preamble = '\
<?xml version="1.0" ?>\n\
<engineconfig>\n\
        <write_period>30</write_period>\n\
        <get_threshold>60</get_threshold>\n\
        <file_size>1000</file_size>\n\
        <ignored_future>6</ignored_future>\n\
        <buffer_reserve>3</buffer_reserve>\n\
        <max_repeat_count>120</max_repeat_count>\n\
\n\
</engineconfig>\n'

if __name__ == '__main__':
    #print engine_preamble
    args = parser.parse_args()
    print args.source
    print args.group
    print args.regex
    print args.monitor
    print args.period
    print args.destination

    # if no destination file is indicated, use './engine.xml'
    if args.destination is None:
        print 'No destination file provided. Defaulting to \'./engine.xml\''
        dest = findFiles('./', 'engine.xml')
        print dest
        if len(dest) == 0:
            #no 'engine.xml' found. Start a new one using 'engine_preamble', above
            dest = open('engine.xml', 'w+')
            dest.write(engine_preamble)
            dest.flush()
            dest.seek(0,0)
            for line in dest:
                stdout.write(line)
        elif len(dest) == 1:
            #found an existing engine.xml file. Open for appending.
            print 'Will append to existing \'engine.xml\' file'
            dest = open('engine.xml', 'w+')
        else:
            exit('\n\nExiting...\nSoooo confused! Found multiple destination files - %s\n\n'%dest)

    
        

