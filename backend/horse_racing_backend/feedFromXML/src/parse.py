import os

import xml.etree.ElementTree as ET
from datetime import datetime

DATA_DIR = "feedFromXML/data"
FORM_DIR = "mr_form"
FIELD_DIR = "mr_fields"

def getHorseObj(horse_obj):
    db_obj = horse_obj.attrib
    for child in horse_obj:
        if child.tag == "trainer":
            trainer = child.attrib
            trainer['statistics'] = []
            statistics = child.find ("statistics")
            for statistic in statistics:
                trainer['statistics'].append (statistic.attrib)
            db_obj['trainer'] = trainer
            continue
        if child.tag == "statistics":
            db_obj["statistics"] = []
            for statistic in child:
                db_obj['statistics'].append (statistic.attrib)
            continue
        if child.tag == "gear_changes":
            db_obj["gear_changes"] = []
            for gear_change in child:
                db_obj['gear_changes'].append (gear_change.attrib)
            continue
        if child.tag == "jockey":
            db_obj["jockey"] = child.attrib
            db_obj['jockey']['statistics'] = []
            statistics = child.find ("statistics")
            if statistics is None: continue
            for statistic in statistics:
                db_obj['jockey']['statistics'].append (statistic.attrib)
            continue
        if child.tag == "forms":
            forms = []
            for form in child:
                form_obj = {}
                for form_child in form:
                    if form_child.tag == "classes":
                        classes = []
                        for class_obj in form_child:
                            classes.append ({class_obj.tag: class_obj.text})
                        form_obj['classes'] = classes
                        continue
                    if form_child.tag == "other_runners":
                        runners = []
                        for runner_obj in form_child:
                            runners.append (runner_obj.attrib)
                        form_obj['other_runners'] = runners
                        continue
                    if form_child.text is not None: form_obj[form_child.tag] = form_child.text
                    if form_child.attrib != {}: form_obj[form_child.tag] = form_child.attrib
                forms.append (form_obj)
            db_obj['forms'] = forms
            continue
        if child.attrib != {}: db_obj[child.tag] = child.attrib
        if child.text is not None: db_obj[child.tag] = child.text
    return db_obj
        
def getRaceObj(race_obj):
    db_obj = race_obj.attrib

    for child in race_obj:
        if child.tag == "classes":
            db_obj['classes'] = {}
            for class_child in child:
                db_obj['classes'][class_child.tag] = class_child.text
            continue
        if child.tag == "prizes":
            db_obj['prizes'] = []
            for prize_child in child:
                db_obj['prizes'].append (prize_child.attrib)
            continue
        if child.tag == "records":
            db_obj['records'] = []
            for tracking_record in child:
                tracking_obj = {}
                for t_child in tracking_record:
                    if t_child.tag == "horse":
                        tracking_obj['horse'] = t_child.attrib
                        for horse_child in t_child:
                            if horse_child.attrib != {}: tracking_obj['horse'][horse_child.tag] = horse_child.attrib
                            if horse_child.text is not None: tracking_obj['horse'][horse_child.tag] = horse_child.text
                        continue

                    if t_child.text is not None: tracking_obj[t_child.tag] = t_child.text
                    if t_child.attrib != {}: tracking_obj[t_child.tag] = t_child.attrib
                db_obj['records'].append (tracking_obj)
            continue

        if child.tag == 'horses':
            db_obj['horses'] = []
            for horse in child:
                db_obj['horses'].append (getHorseObj(horse))
            continue

        if child.text is not None:
            db_obj[child.tag] = child.text
        if child.attrib != {}:
            db_obj[child.tag] = child.attrib
    return db_obj

# def main():
def parse():
    cur_dir = os.getcwd()

    form_file_list = os.listdir(os.path.join(cur_dir, DATA_DIR, FORM_DIR))
    form_file_dir = os.path.join(DATA_DIR, FORM_DIR)

    rlt = []
    for form_file in form_file_list:
        db_obj = {}
        tree = ET.parse(os.path.join(form_file_dir, form_file))
        root = tree.getroot()
        for child in root:
            if child.tag == "races":
                db_obj['races'] = []
                for race in child:
                    db_obj['races'].append (getRaceObj(race))
                continue
            if child.tag == "track":
                if 'name' in child.attrib: db_obj['name'] = child.attrib['name']
                if 'id' in child.attrib: db_obj['id'] = child.attrib['id']
                if 'expected_condition' in child.attrib: db_obj['expected_condition'] = child.attrib['expected_condition']
                if 'club' in child.attrib: db_obj['club'] = child.attrib['club']
                if 'track_surface' in child.attrib: db_obj['track_surface'] = child.attrib['track_surface']
                if 'location' in child.attrib: db_obj['location'] = child.attrib['location']
                if 'country' in child.attrib: db_obj['country'] = child.attrib['country']
                if 'state' in child.attrib: db_obj['state'] = child.attrib['state']
                if 'track_3char_abbrev' in child.attrib: db_obj['track_3char_abbrev'] = child.attrib['track_3char_abbrev']
                if 'track_4char_abbrev' in child.attrib: db_obj['track_4char_abbrev'] = child.attrib['track_4char_abbrev']
                if 'track_6char_abbrev' in child.attrib: db_obj['track_6char_abbrev'] = child.attrib['track_6char_abbrev']
                if 'night_meeting' in child.attrib: db_obj['night_meeting'] = child.attrib['night_meeting']
                continue
            if child.text is not None:
                db_obj[child.tag] = child.text
            if child.attrib != {}:
                db_obj[child.tag] = child.attrib
        rlt.append (db_obj)
    
    return rlt

def buildProfile():
    cur_dir = os.getcwd()

    form_file_list = os.listdir(os.path.join(cur_dir, DATA_DIR, FORM_DIR))
    form_file_dir = os.path.join(DATA_DIR, FORM_DIR)

    rlt = []
    for form_file in form_file_list:
        db_obj = {}
        tree = ET.parse(os.path.join(form_file_dir, form_file))
        root = tree.getroot()
        for child in root:
            if child.tag == "races":
                db_obj['races'] = []
                for race in child:
                    db_obj['races'].append (getRaceObj(race))
                continue
            if child.tag == "track":
                if 'name' in child.attrib: db_obj['name'] = child.attrib['name']
                if 'id' in child.attrib: db_obj['id'] = child.attrib['id']
                if 'expected_condition' in child.attrib: db_obj['expected_condition'] = child.attrib['expected_condition']
                if 'club' in child.attrib: db_obj['club'] = child.attrib['club']
                if 'track_surface' in child.attrib: db_obj['track_surface'] = child.attrib['track_surface']
                if 'location' in child.attrib: db_obj['location'] = child.attrib['location']
                if 'country' in child.attrib: db_obj['country'] = child.attrib['country']
                if 'state' in child.attrib: db_obj['state'] = child.attrib['state']
                if 'track_3char_abbrev' in child.attrib: db_obj['track_3char_abbrev'] = child.attrib['track_3char_abbrev']
                if 'track_4char_abbrev' in child.attrib: db_obj['track_4char_abbrev'] = child.attrib['track_4char_abbrev']
                if 'track_6char_abbrev' in child.attrib: db_obj['track_6char_abbrev'] = child.attrib['track_6char_abbrev']
                if 'night_meeting' in child.attrib: db_obj['night_meeting'] = child.attrib['night_meeting']
                continue
            if child.text is not None:
                db_obj[child.tag] = child.text
            if child.attrib != {}:
                db_obj[child.tag] = child.attrib
        rlt.append (db_obj)
    
    return rlt

def buildRaceProfile():
    cur_dir = os.getcwd()

    form_file_list = os.listdir(os.path.join(cur_dir, DATA_DIR, FORM_DIR))
    form_file_dir = os.path.join(DATA_DIR, FORM_DIR)

    rlt = []
    for form_file in form_file_list:
        tree = ET.parse(os.path.join(form_file_dir, form_file))
        root = tree.getroot()
        if root is None: continue
        
        homeTrack = root.find("track")
        homeTrackAttrib = homeTrack.attrib

        races = root.find("races")
        if races is None: continue
        
        races = races.findall("race")
        if races  is None: continue
        if len(races) == 0: continue
        for race in races:
            horses = race.find("horses")
            if horses is None: continue
            horses = horses.findall("horse")
            if len(horses) == 0: continue

            for horse in horses:
                horseAttrib = horse.attrib

                trainer = horse.find('trainer')
                trainerAttrib = trainer.attrib

                sire = horse.find('sire')
                sireAttrib = sire.attrib

                dam = horse.find('sire')
                damAttrib = dam.attrib

                sire_dam = horse.find('sire_of_dam')
                sireDamAttrib = sire_dam.attrib

                jockey = horse.find('jockey')
                jockeyAttrib = jockey.attrib

                win_p = horse.find('win_percentage')
                place_p = horse.find('place_percentage')

                forms = horse.find("forms")
                if forms is None: continue
                forms = forms.findall("form")
                if len(forms) == 0: continue
                for form in forms:
                    tmp = {}
                    tmp['horse_name'] = horseAttrib['name'] if 'name' in horseAttrib else ''
                    tmp['horse_country'] = horseAttrib['country'] if 'country' in horseAttrib else ''
                    tmp['horse_age'] = int(horseAttrib['age']) if 'age' in horseAttrib else -1
                    tmp['horse_colour'] = horseAttrib['colour'] if 'colour' in horseAttrib else ''
                    tmp['horse_sex'] = horseAttrib['sex'] if 'sex' in horseAttrib else ''
                    tmp['horse_id'] = int(horseAttrib['id']) if 'id' in horseAttrib else -1
                    tmp['horse_foaling_date'] = datetime.strptime(horseAttrib['foaling_date'], "%d/%m/%Y") if 'foaling_date' in horseAttrib else None

                    tmp['home_track_name'] = homeTrackAttrib['name'] if 'name' in homeTrackAttrib else ''
                    tmp['home_id_name'] = homeTrackAttrib['id'] if 'id' in homeTrackAttrib else ''
                    tmp['home_track_surface'] = homeTrackAttrib['track_surface'] if 'track_surface' in homeTrackAttrib else ''
                    tmp['home_track_3char_abbrev'] = homeTrackAttrib['track_3char_abbrev'] if 'track_3char_abbrev' in homeTrackAttrib else ''
                    
                    tmp['sire_name'] = sireAttrib['name'] if 'name' in sireAttrib else ''
                    tmp['sire_country'] = sireAttrib['country'] if 'country' in sireAttrib else ''
                    tmp['sire_id'] = int(sireAttrib['id']) if 'id' in sireAttrib else ''

                    tmp['dam_name'] = damAttrib['name'] if 'name' in damAttrib else ''
                    tmp['dam_country'] = damAttrib['country'] if 'country' in damAttrib else ''
                    tmp['dam_id'] = int(damAttrib['id']) if 'id' in damAttrib else ''

                    tmp['sire_dam_name'] = sireDamAttrib['name'] if 'name' in sireDamAttrib else ''
                    tmp['sire_dam_country'] = sireDamAttrib['country'] if 'country' in sireDamAttrib else ''
                    tmp['sire_dam_id'] = sireDamAttrib['id'] if 'id' in sireDamAttrib else ''
                    
                    tmp['trainer_name'] = trainerAttrib['name'] if 'name' in horseAttrib else ''
                    tmp['trainer_firstname'] = trainerAttrib['firstname'] if 'firstname' in horseAttrib else ''
                    tmp['trainer_surname'] = trainerAttrib['surname'] if 'surname' in horseAttrib else ''
                    tmp['trainer_id'] = int(trainerAttrib['id']) if 'id' in horseAttrib else -1

                    tmp['jockey_name'] = jockeyAttrib['name'] if 'name' in jockeyAttrib else ''
                    tmp['jockey_firstname'] = jockeyAttrib['firstname'] if 'firstname' in jockeyAttrib else ''
                    tmp['jockey_surname'] = jockeyAttrib['surname'] if 'surname' in jockeyAttrib else ''
                    tmp['jockey_id'] = int(jockeyAttrib['id']) if 'id' in jockeyAttrib else -1
                    tmp['jockey_riding_weight'] = float(jockeyAttrib['riding_weight']) if 'riding_weight' in jockeyAttrib and  len(jockeyAttrib['riding_weight'].strip()) > 0 else -1
                    tmp['jockey_apprentice_indicator'] = jockeyAttrib['apprentice_indicator'] if 'apprentice_indicator' in jockeyAttrib else ''

                    tmp['win_percentage'] = float(win_p.text) if win_p is not None else -1
                    tmp['place_percentage'] = float(place_p.text) if place_p is not None else -1

                    if form.getchildren() is None: continue
                    for child in form.getchildren():
                        if child.tag == "meeting_date": tmp['date'] = datetime.strptime(child.text, "%d/%m/%Y")
                        if child.tag == "event_id": tmp['event_id'] = int(child.text)
                        if child.tag == "jockey":
                            jockey = child.attrib
                            tmp['jockey_name'] = jockey['name']
                            tmp['jockey_id'] = int(jockey['id'])
                        if child.tag == 'track':
                            track = child.attrib
                            tmp['track_name'] = track['name']
                            tmp['track_id'] = int(track['id'])
                            tmp['track_location'] = track['location']
                            tmp['track_condition'] = track['condition']
                            try:
                                tmp['track_grading'] = int(track['grading'])
                            except:
                                tmp['track_grading'] = -1
                            tmp['track_surface'] = track['track_surface'] if 'track_surface' in track else 'A'
                            tmp['track_3char_abbrev'] = track['track_3char_abbrev']
                            tmp['track_4char_abbrev'] = track['track_4char_abbrev']
                            tmp['track_6char_abbrev'] = track['track_6char_abbrev']
                        if child.tag == "race":
                            form_race = child.attrib
                            tmp['race_num'] = form_race['number']
                            tmp['race_name'] = form_race['name']
                        if child.tag == "starters":
                            tmp['starters'] = int(child.text)
                        if child.tag == "barrier":
                            tmp['barrier'] = int(child.text)
                        if child.tag == "weight_carried":
                            tmp['weight'] = float(child.text)
                        if child.tag == "positions":
                            positions = child.attrib
                            tmp['settling'] = int(positions['settling_down']) if 'settling_down' in positions else -1
                        if child.tag == "distance":
                            distance = child.attrib
                            tmp['distance'] = int(distance['metres'])
                        if child.tag == "sectional":
                            sectional = child.attrib
                            if sectional['distance'] == "600":
                                t = sectional['time'].split(":")
                                tmp['last_600'] = float(t[1])
                        if child.tag == "finish_position":
                            try:
                                tmp['finish_number'] = int(child.text)
                            except:
                                tmp['finish_number'] = -1
                        if child.tag == "margin":
                            try:
                                tmp['margin'] = float(child.text)
                            except:
                                tmp['margin'] = -1
                        if child.tag == "event_duration":
                            t = child.text.split (":")
                            tmp['time'] = float (t[1]) + 60 * float(t[0])
                        if child.tag == "event_prizemoney":
                            tmp['prizemoney_won'] = float(child.text)
                        if child.tag == "horse_prizemoney":
                            tmp['horse_prizemoney'] = float(child.text) if child.text is not None else -1
                        if child.tag == "horse_prizemoney_bonus":
                            tmp['horse_prizemoney_bonus'] = float(child.text) if child.text is not None else -1
                        if child.tag == "classes":
                            classId = child.find("class_id")
                            className = child.find("class")
                            tmp['class_id'] = int(classId.text) if classId is not None else -1
                            tmp['class'] = className.text if className is not None else ''
                    
                    if 'starters' in tmp and 'settling' in tmp:
                        if tmp['settling'] > 0:
                            tmp['settling'] = float("{:.2f}".format((tmp['starters'] - tmp['settling']) * 100 / (tmp['starters'] - 1)))
                        else:
                            tmp['settling'] = 0
                    if 'starters' in tmp and 'finish_number' in tmp:
                        if tmp['finish_number'] > 0:
                            if tmp['starters'] > 1:
                                tmp['finish_percentage'] = float("{:.2f}".format((tmp['starters'] - tmp['finish_number']) * 100 / (tmp['starters'] - 1)))
                            else:
                                tmp['finish_percentage'] = 0
                        else:
                            tmp['finish_percentage'] = -1
                    if 'distance' in tmp and 'time' in tmp and 'margin' in tmp:
                        if (tmp['time'] == 0): tmp['speed'] = 'INFINITY'
                        else:
                            tmp['time'] = float("{:.2f}".format((tmp['distance'] + tmp['margin'] * 2.4) * tmp['time'] /tmp['distance']))
                            tmp['speed'] = float("{:.2f}".format(tmp['distance'] / tmp['time']))

                    rlt.append (tmp)
            # break
        # for horse in horses:

        # break
    return rlt
# if __name__ == "__main__":
#     main()
