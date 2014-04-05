# import from up a directory
import sys
sys.path.append('..')
# ---


from libs.BeautifulSoup import BeautifulSoup
import urllib2
import json

depts = ['ACCT', 'ADVRT', 'AER+E', 'AF+AM', 'A+B+E', 'AGEDS', 'A+E', 'AGRON', 'AFAS', 'AM+IN', 'ASL', 'A+ECL', 'AN+S', 'ANTHR', 'AESHM', 'A+M+D', 'ARABC', 'ARCH', 'ART', 'ARTED', 'ART+H', 'ASTRO', 'A+TR', 'ATH', 'BBMB', 'BIOE', 'BCBIO', 'BCB', 'BSE', 'BPM+I', 'BIOL', 'B+M+S', 'BR+C', 'BRT', 'BUSAD', 'CH+E', 'CHEM', 'CHIN', 'C+E', 'CL+ST', 'CMDIS', 'COMST', 'C+R+P', 'C+DEV', 'CL+PS', 'CPR+E', 'COM+S', 'CON+E', 'CJ+ST', 'C+I', 'DANCE', 'DES', 'DSN+S', 'DIET', 'EEB', 'EEOB', 'ECON', 'EDADM', 'EL+PS', 'E+E', 'ENGR', 'E+M', 'ENGL', 'ENT', 'ENSCI', 'ENV+S', 'EVENT', 'EXPRO', 'FCEDS', 'FFP', 'FIN', 'FS+HN', 'FOR', 'FRNCH', 'GEN', 'GENET', 'GDCB', 'GEOL', 'GER', 'GERON', 'GLOBE', 'GR+ST', 'ARTGR', 'GREEK', 'H+S', 'HG+ED', 'H+P+C', 'HIST', 'HON', 'HORT', 'HRI', 'HCI', 'HD+FS', 'H+SCI', 'IMBIO', 'IND+D', 'I+E', 'INFAS', 'ARTIS', 'IGS', 'ARTID', 'INTST', 'IA+LL', 'JL+MC', 'KIN', 'L+A', 'LATIN', 'L+TM', 'LAS', 'LIB', 'LING', 'MGMT', 'MIS', 'MKT', 'MAT+E', 'M+S+E', 'MATH', 'M+E', 'MTEOR', 'MICRO', 'M+S', 'MCDB', 'MUSIC', 'NREM', 'N+S', 'NEURO', 'NUC+E', 'NUTRS', 'OTS', 'PERF', 'PHIL', 'PHYS', 'PLBIO', 'PL+P', 'POL+S', 'PSYCH', 'P+R', 'RELIG', 'RESEV', 'RUS', 'STB', 'SOC', 'S+E', 'SPAN', 'SP+ED', 'SP+CM', 'STAT', 'SCM', 'SUSAG', 'SUS+E', 'T+SC', 'TSM', 'THTRE', 'TOX', 'TRANS', 'US+LS', 'U+ST', 'URB+D', 'VDPAM', 'V+C+S', 'V+MPM', 'V+PTH', 'WESEP', 'W+S', 'WLC', 'YTH']
classes_iastate_edu = 'http://classes.iastate.edu/soc.jsp?term=F2014&dept=%s&term2=F2014&dept2=ACCT+&course=&shour=06&sminute=00&sampm=am&ehour=11&eminute=55&eampm=pm&credit=+&instructor=&title=&edreq=&spclcourse=&partterm=2006-01-012006-12-31&smonth=01&sday=01&emonth=12&eday=31'

# these courses don't work on the website?
depts.remove('A+E')
depts.remove('BSE')
depts.remove('BR+C')
depts.remove('EXPRO')
depts.remove('GREEK')
depts.remove('IA+LL')
depts.remove('L+TM')


def parseSection(x):
    sects = [foo.strip() for foo in x.split('Textbook Information') if foo]
    sections = []
    for sect in sects:
        x = sect.split(' ')
        sect_info = {

        }
        if x[0].startswith('******'):
            break
        for n in xrange(len(x)):
            if n == 0:
                sect_info['id'] = x[n]
            elif n == 1:
                sect_info['section'] = x[n]
            elif n == 2:
                if x[n] == 'Reserved':
                    sect_info['status'] = 'Reserved'
                elif x[n] == 'Closed':
                    sect_info['status'] = 'Closed'
                elif x[n] == 'Open':
                    sect_info['status'] = 'Open'

                sect_info['seats'] = x[n]
            elif n == 4 and 'status' not in sect_info:
                sect_info['status'] = x[n]
            elif 'status' in sect_info:
                info = x[n].split(':')
                if len(info) == 1:
                    if x[n].startswith('ARRANGED'):
                        sect_info['days'] = 'ARRANGED'
                        sect_info['times'] = 'ARRANGED'
                        break

                    sect_info['days'] = sect_info.get('days', '') + x[n]
                else:
                    sect_info['times'] = x[n]
                    break
        sections.append(sect_info)
    return sections


def parseCourse(x, dept):
    return x.split(dept)[1].split(' ')[1]



for current_dept in depts:


    req = urllib2.Request(classes_iastate_edu % (current_dept,))
    response = urllib2.urlopen(req)


    soup = BeautifulSoup(response.read())


    table = soup.findAll('table')[1]
    rows = table.findAll('tr')


    currentNode = ''
    isu_class = {}
    shits = []

    for row in rows:
        cells = row.findAll('td')
        for cell in cells:
            attrs = dict(cell.attrs)

            if attrs.get('align') == 'right':
                x = cell.getText().split(':')[0].strip()
                if x == '':
                    continue
                currentNode = x

            elif attrs.get('colspan') == '7':
                shits.append(isu_class)

                isu_class = {}

            else:
                info = cell.getText()
                info = ' '.join(info.split())
                info = '&'.join(info.split('&amp;'))
                info = ' '.join(info.split('&nbsp;'))
                info = info.strip()

                if info.startswith('CREDIT:'):
                    isu_class['CREDIT'] = info.split(':')[1].strip()
                    continue

                info = ' '.join([isu_class.get(currentNode, ''), info])
                isu_class[currentNode] = info


    for shit in shits:
        shit['SECTION'] = parseSection(shit['SECTION'])
        shit['COURSE'] = parseCourse(shit['COURSE'], ' '.join(current_dept.split('+')))
    else:
        print current_dept
        filename = '../class_data/%s.json' % (current_dept,)
        with open(filename, 'w') as outfile:
            json.dump(shits, outfile)

