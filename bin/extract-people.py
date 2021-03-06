#!/usr/bin/env python

import argparse
import pandas as pd
import yaml
from pathlib import Path


def extract_people_info(row):
    '''Extract people information from a row of the csv
    and return them as a key and a dictionary

    :param row: df row
    '''
    info = {
        'first-name': row['First name'],
        'last-name': row['Last name'],
        'email': row['Email'],
        'twitter': row['Twitter username'],
        'website': row['Website'],
        'orcid': row['ORCID'],
        'affiliation': row['Affiliation'],
        'country': row['Country'],
        'pronouns': row['Pronouns'],
        'expertise': row['Areas of expertise (1 element per line)'],
        'bio': row['Bio']
    }
    github = row['Github username']
    if github is None:
        github = '%s-%s' % (
            info['first-name'].lower(),
            info['last-name'].lower())
        info['github'] = False
    if info['email'] is None:
        del info['email']
    if info['twitter'] is None:
        del info['twitter']
    if info['website'] is None:
        del info['website']
    if info['orcid'] is None:
        del info['orcid']
    if info['affiliation'] is None:
        del info['affiliation']
    if info['country'] is None:
        del info['country']
    if info['pronouns'] is None:
        del info['pronouns']
    if info['expertise'] is None:
        del info['expertise']
    if info['bio'] is None:
        del info['bio']
    return github, info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract people information from a sheet and add them to people.yaml')
    parser.add_argument('-i', '--information', help="Path to information sheet file")
    args = parser.parse_args()

    people_fp = Path('_data') / Path('people.yaml')

    # load people.yaml file into a dictionary
    with open(people_fp, 'r') as people_f:
        people = yaml.load(people_f, Loader=yaml.FullLoader)
    
    # load people information from sheet file
    # parse it
    # add information to people dictionary
    information_fp = Path(args.information)
    df = pd.read_csv(information_fp)
    df = df.where(pd.notnull(df), None)
    for index, row in df.iterrows():
        github, info = extract_people_info(row)
        if github not in people:
            people[github] = info

    # dump people dictionary into people.yaml file
    with people_fp.open("w") as people_f:
        people_f.write('# List of people (alphabetical order)\n')
        people_f.write('#\n')
        people_f.write('# Collection names should be equal to github username,\n')
        people_f.write('# if not, add github: false tag and\n')
        people_f.write('# use firstname-lastname as collection name\n')
        people_f.write('#\n')
        people_f.write('# List of tags for people\n')
        people_f.write('#\n')
        people_f.write('# first-name:\n')
        people_f.write('# last-name:\n')
        people_f.write('# twitter:\n')
        people_f.write('# email:\n')
        people_f.write('# website:\n')
        people_f.write('# gitter:\n')
        people_f.write('# orcid:\n')
        people_f.write('# affiliation:\n')
        people_f.write('# country:\n')
        people_f.write('# pronouns:\n')
        people_f.write('# expertise:\n')
        people_f.write('#    -\n')
        people_f.write('# bio:\n')
        people_f.write('#\n')
        people_f.write('# Mandatory: first-name, last-name, country\n')
        people_f.write('---\n')
        people_f.write(yaml.dump(people))
