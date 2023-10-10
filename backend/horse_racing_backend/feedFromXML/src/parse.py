import os

import xml.etree.ElementTree as ET
from datetime import datetime

DATA_DIR = "./data"
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
                        tracking_obj['horse'] = {}
                        tracking_obj['horse']['name'] = t_child.attrib ["name"]
                        tracking_obj['horse']['country'] = t_child.attrib ["country"]
                        tracking_obj['horse']['id'] = t_child.attrib ["id"]
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
    form_file_list = os.listdir(os.path.join(DATA_DIR, FORM_DIR))
    form_file_dir = os.path.join(DATA_DIR, FORM_DIR)
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
            if child.text is not None:
                db_obj[child.tag] = child.text
            if child.attrib != {}:
                db_obj[child.tag] = child.attrib


if __name__ == "__main__":
    main()
