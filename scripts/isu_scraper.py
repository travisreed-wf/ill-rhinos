# import from up a directory
import sys
sys.path.append('..')
# ---


from libs.BeautifulSoup import BeautifulSoup
import urllib2
import json

depts = ['ACCT', 'ADVRT', 'AER+E', 'AF+AM', 'A+B+E', 'AGEDS', 'A+E', 'AGRON', 'AFAS', 'AM+IN', 'ASL', 'A+ECL', 'AN+S', 'ANTHR', 'AESHM', 'A+M+D', 'ARABC', 'ARCH', 'ART', 'ARTED', 'ART+H', 'ASTRO', 'A+TR', 'ATH', 'BBMB', 'BIOE', 'BCBIO', 'BCB', 'BSE', 'BPM+I', 'BIOL', 'B+M+S', 'BR+C', 'BRT', 'BUSAD', 'CH+E', 'CHEM', 'CHIN', 'C+E', 'CL+ST', 'CMDIS', 'COMST', 'C+R+P', 'C+DEV', 'CL+PS', 'CPR+E', 'COM+S', 'CON+E', 'CJ+ST', 'C+I', 'DANCE', 'DES', 'DSN+S', 'DIET', 'EEB', 'EEOB', 'ECON', 'EDADM', 'EL+PS', 'E+E', 'ENGR', 'E+M', 'ENGL', 'ENT', 'ENSCI', 'ENV+S', 'EVENT', 'EXPRO', 'FCEDS', 'FFP', 'FIN', 'FS+HN', 'FOR', 'FRNCH', 'GEN', 'GENET', 'GDCB', 'GEOL', 'GER', 'GERON', 'GLOBE', 'GR+ST', 'ARTGR', 'GREEK', 'H+S', 'HG+ED', 'H+P+C', 'HIST', 'HON', 'HORT', 'HRI', 'HCI', 'HD+FS', 'H+SCI', 'IMBIO', 'IND+D', 'I+E', 'INFAS', 'ARTIS', 'IGS', 'ARTID', 'INTST', 'IA+LL', 'JL+MC', 'KIN', 'L+A', 'LATIN', 'LAS', 'LIB', 'LING', 'MGMT', 'MIS', 'MKT', 'MAT+E', 'M+S+E', 'MATH', 'M+E', 'MTEOR', 'MICRO', 'M+S', 'MCDB', 'MUSIC', 'NREM', 'N+S', 'NEURO', 'NUC+E', 'NUTRS', 'OTS', 'PERF', 'PHIL', 'PHYS', 'PLBIO', 'PL+P', 'POL+S', 'PSYCH', 'P+R', 'RELIG', 'RESEV', 'RUS', 'STB', 'SOC', 'S+E', 'SPAN', 'SP+ED', 'SP+CM', 'STAT', 'SCM', 'SUSAG', 'SUS+E', 'T+SC', 'TSM', 'THTRE', 'TOX', 'TRANS', 'US+LS', 'U+ST', 'URB+D', 'VDPAM', 'V+C+S', 'V+MPM', 'V+PTH', 'WESEP', 'W+S', 'WLC', 'YTH']

# depts = ['AER+E']
# depts = ['GERON']
# depts = ['ACCT']
classes_iastate_edu = 'http://classes.iastate.edu/soc.jsp?term=F2014&dept=%s&term2=F2014&dept2=ACCT+&course=&shour=06&sminute=00&sampm=am&ehour=11&eminute=55&eampm=pm&credit=+&instructor=&title=&edreq=&spclcourse=&partterm=2006-01-012006-12-31&smonth=01&sday=01&emonth=12&eday=31'

# these courses don't work on the website?
# depts.remove('A+E')
# depts.remove('BSE')
# depts.remove('BR+C')
# depts.remove('EXPRO')
# depts.remove('GREEK')
# depts.remove('IA+LL')
# depts.remove('L+TM')


def parseSection(x):
    if x is None:
        return []
    if x[0].startswith('******'):
        return []

    sects = [foo.strip() for foo in x.split('Textbook Information') if foo]

    sections = []

    for sect in sects:
        
        sect_info = {

            'times': [],
            'seats': '0',
            'section': ''
        }

# 1544005 A 32 Seats Open T 12:10pm-2:00pm  WIERSEMA JAN  Meets: 08/25 - 12/19
        foo = sect.split(' ')

        last_thing = ''
        if 'Taught at, in or' in sect or 'Computer Requirement' in sect:
            continue

        for bar in foo:
            if (bar in ('M', 'T', 'W', 'R', 'F')) or (('pm' in bar or 'am' in bar) and ':' in bar):

                try:
                    if foo[foo.index(bar)+1] not in ('Closed', 'Reserved', 'Off'):
                        if ':' in bar:
                            sect_info['times'].append(bar)
                        elif foo[foo.index(bar)-1].isdigit():
                            sect_info['times'].append(bar)
                        elif bar in ('M', 'T', 'W', 'R', 'F'):
                            sect_info['times'].append(bar)

                    else:
                        sect_info['section'] = bar
                except:
                    pass

            elif bar == 'Seats':
                sect_info['seats'] = last_thing
            elif len(bar) <= 2 and bar not in ('-', '', '&', 'TO', 'BY', 'IS') and sect_info['section'] == '':

                try:
                    if foo[foo.index(bar)+1] in ('Closed', 'Reserved', 'Off') or foo[foo.index(bar)+2] in ('Seats',):
                        sect_info['section'] = bar
                except:
                    pass

                if not bar.isdigit() and all(c.isupper() or c.isdigit() for c in bar):
                    sect_info['section'] = bar

            last_thing = bar
        # sect_info['days'] = ' '.join(sect_info['days'])
        sect_info['times'] = ' '.join(sect_info['times'])

        sections.append(sect_info)
    return sections


def parseCourse(x, dept):
    if x is None:
        return []
    w = x.count(dept)
    return x.split(dept)[w].split(' ')[1]



for current_dept in depts:


    req = urllib2.Request(classes_iastate_edu % (current_dept,))
    response = urllib2.urlopen(req)


    soup = BeautifulSoup(response.read())


    table = soup.findAll('table')[1]
    rows = table.findAll('tr')


    currentNode = ''
    isu_class = {}
    courses = []

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
                courses.append(isu_class)

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


    for course in courses:
        course['SECTION'] = parseSection(course.get('SECTION'))
        course['COURSE'] = parseCourse(course.get('COURSE'), ' '.join(current_dept.split('+')))
    else:
        print current_dept
        filename = '../static/data/%s.json' % (current_dept,)
        with open(filename, 'w') as outfile:
            json.dump(courses, outfile)

