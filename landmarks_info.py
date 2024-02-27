from bs4 import BeautifulSoup
import numpy as np

#---------------------------------------
# List of participants
#---------------------------------------

participants = ['ca', 'jf', 'tc', 'cs', 'ra', 'kk', 'vc', 'bew', 'ttt', 'kp', 'jo', 'jvm', 'tt', 'lucie', 'ast', 'rs', 'es', 'jb', 'pw']

participants_names = {'jf': 'Jana',
                     'jo': 'Jasmin',
                     'bew': 'Bettina',
                     'ca': 'Cassian',
                     'cs': 'Christina',
                     'jvm': 'Javier',
                     'kk': 'Kristaps',
                     'kp':'Kaisa',
                     'ra':'Rashi',
                     'tc':'Tiago ',
                     'tt': 'Thomas',
                     'ttt': 'Tina',
                     'vc': 'Valerie',
                     'lucie': 'Lucie ',
                     'ast': 'Anna-Sophia',
                     'rs': 'Risa',
                     'es': 'Encarnacion',
                     'jb': 'Joergen',
                     'pw': 'Philip'}

participants_pointset_count= {
                     'jf': 3,
                     'jo': 5,
                     'bew': 2,
                     'ca': 4,
                     'cs': 3,
                     'jvm': 3,
                     'kk': 3,
                     'kp': 5,
                     'ra': 4,
                     'tc': 2,
                     'tt': 3,
                     'ttt': 3,
                     'vc': 5,
                     'lucie':4,
                     'ast': 3,
                     'rs': 2,
                     'es': 4,
                     'jb': 4,
                     'pw':3}

#---------------------------------------
# Landmarks info
#---------------------------------------

set_vert = {
    'name': 'Vert',
    'file_name': 'PointSet1_Vert'.lower(),
    'landmarks': [
        'Transition skull to spine',
        'Vert1',
        'Vert2',
        'Vert3',
        'Vert4',
        'Vert5',
        'Vert_Last_Center'
    ]
}

set_fins = {
    'name': 'Fins',
    'file_name': 'PointSet2_Fins'.lower(),
    'landmarks': [
        'Pectoral_dorsal most breast fin to body connection 1_right',
        'Pectoral_dorsal most breast fin to body connection 2_left',
        'Abdominal_fins back 1_right',
        'Abdominal_fins back 2_left'
    ]
}

set_digest = {
    'name': 'Digest',
    'file_name': 'PointSet3_Digest'.lower(),
    'landmarks': [
        'anus_Center',
        'esophagus'
    ]
}

set_heart = {
    'name': 'Heart',
    'file_name': 'PointSet4_Heart'.lower(),
    'landmarks': [
        'tip of bulbus arteriosus vessel inside',
        'sinus venosus',
        'apex of ventricle',
        'anterior most point of ventricle'
    ]
}

set_eyes = {
    'name': 'Eyes',
    'file_name': 'PointSet5_Eyes'.lower(),
    'landmarks': [
        'optic nerve head 1_right',
        'optic nerve head 2_left',
        'optic chiasm_crossing',
        'most_anterior_right',
        'most_anterior_left',
        'most_posterior_right',
        'most_posterior_left',
        'most_dorsal_right',
        'most_dorsal_left',
        'most_ventral_right',
        'most_ventral_left'
    ]
}

set_skull_front = {
    'name': 'Skull Front',
    'file_name': 'PointSet6_Skull_Front'.lower(),
    'landmarks': [
        'dorsal side of nostril outlet right',
        'dorsal side of nostril outlet left',
        'mandible dentary',
        'tongue tip',
        'upper jaw channel',
        'hyoid fusion'
    ]
}

set_skull_center = {
    'name': 'Skull Center',
    'file_name': 'PointSet7_Skull_Center'.lower(),
    'landmarks': [
        'subhypophysis bone',
        'hyoid between branchial arches',
        'split of afferent branchial artery 1',
        'split of afferent branchial artery 2',
        'gills bone right',
        'gills bone left'
    ]
}

set_skull_end = {
    'name': 'Skull End',
    'file_name': 'PointSet8_Skull_End'.lower(),
    'landmarks': [
        'skull landmark A right',
        'skull landmark A left',
        'fusion of epibranchial artery 2',
        'center of utricle right',
        'center of utricle left'
    ]
}

set_brain = {
    'name': 'Brain',
    'file_name': 'PointSet9_Brain'.lower(),
    'landmarks': [
    'hypophysis',
    'olfactoryN_right',
    'olfactoryN_left',
    'glomerulosus_R',
    'glomerulosus_L',
    'OT_rightmost',
    'OT_leftmost',
    'cerebellum',
    'OT cerebellum torus',
    'epiphysis'
    ]
}


def read_landmarks(file_name, mode='def'):
    
    if mode == 'lowercase':
        file_name = file_name.lower()
    
    with open(str(file_name), 'r') as f:
        data = f.read()
    
    xml_data = BeautifulSoup(data, "xml")
    points = xml_data.find_all('point')
    
    landmarks = []
    
    # First landmark should be zero
    p = points[0]
    if p.find('x').text != '0' and p.find('y').text != '0' and p.find('z').text != '0':
        print(f'WARNING: {file_name}. First landmark is not zero!')
    
    # Skip first
    for p in points[1:]:
        #if p.find('x').text == '0' and p.find('y').text == '0' and p.find('z').text == '0':
        #    continue

        x = float(p.find('x').text)
        y = float(p.find('y').text)
        z = float(p.find('z').text)

        landmarks.append(np.asarray([x,y,z]))
        
    f.close()
        
    return landmarks

def get_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
