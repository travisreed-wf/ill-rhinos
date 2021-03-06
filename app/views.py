import logging
import random
import json

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app.models import user
from flask_login import login_required
from flask_login import current_user

majors = [{"value":"ACCT","text":"ACCOUNTING"},{"value":"ADVRT","text":"ADVERTISING"},{"value":"AER+E","text":"AEROSPACE ENGINEERING"},{"value":"AF+AM","text":"AFRICAN AND AFRICAN AMERICAN STUDIES"},{"value":"A+B+E","text":"AGRICULTURAL AND BIOSYSTEMS ENGINEERING"},{"value":"AGEDS","text":"AGRICULTURAL EDUCATION & STUDIES"},{"value":"A+E","text":"AGRICULTURAL ENGINEERING"},{"value":"AGRON","text":"AGRONOMY"},{"value":"AFAS","text":"AIR FORCE AEROSPACE STUDIES"},{"value":"AM+IN","text":"AMERICAN INDIAN STUDIES"},{"value":"ASL","text":"AMERICAN SIGN LANGUAGE"},{"value":"A+ECL","text":"ANIMAL ECOLOGY"},{"value":"AN+S","text":"ANIMAL SCIENCE"},{"value":"ANTHR","text":"ANTHROPOLOGY"},{"value":"AESHM","text":"APPAREL, EVENTS, AND HOSPITALITY MANAGEM"},{"value":"A+M+D","text":"APPAREL, MERCHANDISING, AND DESIGN"},{"value":"ARABC","text":"ARABIC"},{"value":"ARCH","text":"ARCHITECTURE"},{"value":"ART","text":"ART & DESIGN"},{"value":"ARTED","text":"ART EDUCATION"},{"value":"ART+H","text":"ART HISTORY"},{"value":"ASTRO","text":"ASTRONOMY & ASTROPHYSICS"},{"value":"A+TR","text":"ATHLETIC TRAINING"},{"value":"ATH","text":"ATHLETICS"},{"value":"BBMB","text":"BIOCHEM, BIOPHYSICS & MOLECULAR BIO"},{"value":"BIOE","text":"BIOENGINEERING"},{"value":"BCBIO","text":"BIOINFORMATICS & COMPUTATIONAL BIOL-UG"},{"value":"BCB","text":"BIOINFORMATICS AND COMPUTATIONAL BIOL"},{"value":"BSE","text":"BIOLOGICAL SYSTEMS ENGINEERING"},{"value":"BPM+I","text":"BIOLOGICAL/PRE-MEDICAL ILLUSTRATION"},{"value":"BIOL","text":"BIOLOGY"},{"value":"B+M S","text":"BIOMEDICAL SCIENCES"},{"value":"BR+C","text":"BIORENEWABLE CHEMICALS"},{"value":"BRT","text":"BIORENEWABLE RESOURCES & TECHNOLOGY"},{"value":"BUSAD","text":"BUSINESS ADMINISTRATION"},{"value":"CH+E","text":"CHEMICAL ENGINEERING"},{"value":"CHEM","text":"CHEMISTRY"},{"value":"CHIN","text":"CHINESE"},{"value":"C+E","text":"CIVIL ENGINEERING"},{"value":"CL+ST","text":"CLASSICAL STUDIES"},{"value":"CMDIS","text":"COMMUNICATION DISORDERS"},{"value":"COMST","text":"COMMUNICATION STUDIES"},{"value":"C+R+P","text":"COMMUNITY & REGIONAL PLANNING"},{"value":"C+DEV","text":"COMMUNITY DEVELOPMENT"},{"value":"CL+PS","text":"COMMUNITY LEADERSHIP AND PUBLIC SERVICE"},{"value":"CPR+E","text":"COMPUTER ENGINEERING"},{"value":"COM+S","text":"COMPUTER SCIENCE"},{"value":"CON+E","text":"CONSTRUCTION ENGINEERING"},{"value":"CJ+ST","text":"CRIMINAL JUSTICE STUDIES"},{"value":"C+I","text":"CURRICULUM & INSTRUCTION"},{"value":"DANCE","text":"DANCE"},{"value":"DES","text":"DESIGN"},{"value":"DSN+S","text":"DESIGN STUDIES"},{"value":"DIET","text":"DIETETICS"},{"value":"EEB","text":"ECOLOGY & EVOLUTIONARY BIOLOGY"},{"value":"EEOB","text":"ECOLOGY, EVOLUTION & ORGANISMAL BIOL"},{"value":"ECON","text":"ECONOMICS"},{"value":"EDADM","text":"EDUCATIONAL ADMINISTRATION"},{"value":"EL+PS","text":"EDUCATIONAL LEADERSHIP & POLICY ST"},{"value":"E+E","text":"ELECTRICAL ENGINEERING"},{"value":"ENGR","text":"ENGINEERING"},{"value":"E+M","text":"ENGINEERING MECHANICS"},{"value":"ENGL","text":"ENGLISH"},{"value":"ENT","text":"ENTOMOLOGY"},{"value":"ENSCI","text":"ENVIRONMENTAL SCIENCE"},{"value":"ENV+S","text":"ENVIRONMENTAL STUDIES"},{"value":"EVENT","text":"EVENT MANAGEMENT"},{"value":"EXPRO","text":"EXCHANGE PROGRAM"},{"value":"FCEDS","text":"FAMILY & CONSUMER SCIENCES ED & STUDIES"},{"value":"FFP","text":"FAMILY FINANCIAL PLANNING"},{"value":"FIN","text":"FINANCE"},{"value":"FS+HN","text":"FOOD SCIENCE & HUMAN NUTRITION"},{"value":"FOR","text":"FORESTRY"},{"value":"FRNCH","text":"FRENCH"},{"value":"GEN","text":"GENETICS"},{"value":"GENET","text":"GENETICS - INTERDISCIPLINARY"},{"value":"GDCB","text":"GENETICS, DEVELOPMENT & CELL BIOL"},{"value":"GEOL","text":"GEOLOGY"},{"value":"GER","text":"GERMAN"},{"value":"GERON","text":"GERONTOLOGY"},{"value":"GLOBE","text":"GLOBAL RESOURCE SYSTEMS"},{"value":"GR+ST","text":"GRADUATE STUDIES"},{"value":"ARTGR","text":"GRAPHIC DESIGN"},{"value":"GREEK","text":"GREEK"},{"value":"H+S","text":"HEALTH STUDIES"},{"value":"HG+ED","text":"HIGHER EDUCATION"},{"value":"H+P+C","text":"HISTORICAL, PHILOSOPHICAL & COMP ED"},{"value":"HIST","text":"HISTORY"},{"value":"HON","text":"HONORS"},{"value":"HORT","text":"HORTICULTURE"},{"value":"HRI","text":"HOTEL RESTAURANT & INSTITUTION MGMT"},{"value":"HCI","text":"HUMAN COMPUTER INTERACTION"},{"value":"HD+FS","text":"HUMAN DEVELOPMENT & FAMILY STUDIES"},{"value":"H+SCI","text":"HUMAN SCIENCES"},{"value":"IMBIO","text":"IMMUNOBIOLOGY"},{"value":"IND+D","text":"INDUSTRIAL DESIGN"},{"value":"I+E","text":"INDUSTRIAL ENGINEERING"},{"value":"INFAS","text":"INFORMATION ASSURANCE"},{"value":"ARTIS","text":"INTEGRATED STUDIO ARTS"},{"value":"IGS","text":"INTERDISCIPLINARY GRADUATE STUDIES"},{"value":"ARTID","text":"INTERIOR DESIGN"},{"value":"INTST","text":"INTERNATIONAL STUDIES"},{"value":"IA+LL","text":"IOWA LAKESIDE LABORATORY"},{"value":"JL+MC","text":"JOURNALISM & MASS COMMUNICATION"},{"value":"KIN","text":"KINESIOLOGY"},{"value":"L+A","text":"LANDSCAPE ARCHITECTURE"},{"value":"LATIN","text":"LATIN"},{"value":"L+TM","text":"LEARNING TEAM"},{"value":"LAS","text":"LIBERAL ARTS & SCIENCES"},{"value":"LIB","text":"LIBRARY"},{"value":"LING","text":"LINGUISTICS"},{"value":"MGMT","text":"MANAGEMENT"},{"value":"MIS","text":"MANAGEMENT INFORMATION SYSTEMS"},{"value":"MKT","text":"MARKETING"},{"value":"MAT+E","text":"MATERIALS ENGINEERING"},{"value":"M+S+E","text":"MATERIALS SCIENCE & ENGINEERING"},{"value":"MATH","text":"MATHEMATICS"},{"value":"M+E","text":"MECHANICAL ENGINEERING"},{"value":"MTEOR","text":"METEOROLOGY"},{"value":"MICRO","text":"MICROBIOLOGY"},{"value":"M+S","text":"MILITARY SCIENCE"},{"value":"MCDB","text":"MOLECULAR CELLULAR DEV BIOLOGY"},{"value":"MUSIC","text":"MUSIC"},{"value":"NREM","text":"NATURAL RESOURCE ECOLOGY AND MGMT"},{"value":"N+S","text":"NAVAL SCIENCE"},{"value":"NEURO","text":"NEUROSCIENCE"},{"value":"NUC+E","text":"NUCLEAR ENGINEERING"},{"value":"NUTRS","text":"NUTRITIONAL SCIENCES"},{"value":"OTS","text":"ORGANIZATION FOR TROPICAL STUDIES"},{"value":"PERF","text":"PERFORMING ARTS"},{"value":"PHIL","text":"PHILOSOPHY"},{"value":"PHYS","text":"PHYSICS"},{"value":"PLBIO","text":"PLANT BIOLOGY"},{"value":"PL+P","text":"PLANT PATHOLOGY"},{"value":"POL+S","text":"POLITICAL SCIENCE"},{"value":"PSYCH","text":"PSYCHOLOGY"},{"value":"P+R","text":"PUBLIC RELATIONS"},{"value":"RELIG","text":"RELIGIOUS STUDIES"},{"value":"RESEV","text":"RESEARCH & EVALUATION"},{"value":"RUS","text":"RUSSIAN"},{"value":"STB","text":"SEED TECHNOLOGY AND BUSINESS"},{"value":"SOC","text":"SOCIOLOGY"},{"value":"S+E","text":"SOFTWARE ENGINEERING"},{"value":"SPAN","text":"SPANISH"},{"value":"SP+ED","text":"SPECIAL EDUCATION"},{"value":"SP+CM","text":"SPEECH COMMUNICATION"},{"value":"STAT","text":"STATISTICS"},{"value":"SCM","text":"SUPPLY CHAIN MANAGEMENT"},{"value":"SUSAG","text":"SUSTAINABLE AGRICULTURE"},{"value":"SUS+E","text":"SUSTAINABLE ENVIRONMENTS"},{"value":"T+SC","text":"TECHNOLOGY & SOCIAL CHANGE"},{"value":"TSM","text":"TECHNOLOGY SYSTEMS MANAGEMENT"},{"value":"THTRE","text":"THEATRE"},{"value":"TOX","text":"TOXICOLOGY"},{"value":"TRANS","text":"TRANSPORTATION"},{"value":"US+LS","text":"U.S. LATINO/A STUDIES"},{"value":"U+ST","text":"UNIVERSITY STUDIES"},{"value":"URB+D","text":"URBAN DESIGN"},{"value":"VDPAM","text":"VET DIAGNOSTIC & PRODUCTION AN MED"},{"value":"V+C S","text":"VETERINARY CLINICAL SCIENCES"},{"value":"V+MPM","text":"VETERINARY MICROBIOLOGY & PREV MED"},{"value":"V+PTH","text":"VETERINARY PATHOLOGY"},{"value":"WESEP","text":"WIND ENERGY SCIENCE, ENGINEERING AND POL"},{"value":"W+S","text":"WOMENS STUDIES"},{"value":"WLC","text":"WORLD LANGUAGES AND CULTURES"},{"value":"YTH","text":"YOUTH"}]


blueprint = Blueprint('views', __name__)

@blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@blueprint.route('/browse', methods=['GET'])
def browse():
    return render_template('browse.html', majors=majors)


@blueprint.route('/schedule', methods=['GET'])
def schedule():
    return render_template('schedule.html', majors=majors)


@blueprint.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@blueprint.route('/alerts', methods=['GET'])
@login_required
def alerts():
    return render_template('alerts.html')

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('email')
        pw = request.form.get('password')
        user.login(username, pw)
        if current_user.is_authenticated():
            next_url = request.args.get('next', url_for('views.alerts'))
            return redirect(next_url, code=302)
    return render_template("login.html")
