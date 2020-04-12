import tools.gdlevelclient as lc
import math
import random
import sys
import os
import base64


PSPREAD_FLASH_CRY = 2
PSPREAD_FLASH_8D = 5
PSPREAD_FLASH_HA = 5
PSPREAD_FLASH_DIE = 5
PSPREAD_FLASH_PAIN = 5
PSPREAD_FLASH_NO = 5
PSPREAD_FLASH_AHAH = 5
PSPREAD_S_SQUARE = 20
PSPREAD_S_CIRCLE = 20
PSPREAD_S_GEAR = 20
PSPREAD_S_CUBE = 20
PSPREAD_TEXT_CRY = 10

PSCALE_S_SQUARE = 0.5
PSCALE_S_CIRCLE = 0.5
PSCALE_S_GEAR = 0.5
PSCALE_S_CUBE = 0.5
PSCALE_TEXT_CRY = 0.5


COLOR_CHANNEL_BG = 1000
COLOR_CHANNEL_G1 = 1001
COLOR_CHANNEL_L = 1002
COLOR_CHANNEL_3DL = 1003
COLOR_CHANNEL_OBJ = 1004
COLOR_CHANNEL_P1 = 1005
COLOR_CHANNEL_P2 = 1006
COLOR_CHANNEL_G2 = 1009

KEY_ID = '1'
KEY_POSX = '2'
KEY_POSY = '3'
KEY_ROTATION = '6'
KEY_RED = '7'
KEY_GREEN = '8'
KEY_BLUE = '9'
KEY_R, KEY_G, KEY_B = KEY_RED, KEY_GREEN, KEY_BLUE # aliases
KEY_COLOR_CHANNEL = '21'
KEY_COLOR_TRIGGER_R = '7'
KEY_COLOR_TRIGGER_G = '8'
KEY_COLOR_TRIGGER_B = '9'
KEY_TRIGGER_DURATION = '10'
KEY_TRIGGER_OPACITY = '35'
KEY_COLOR_TRIGGER_CHANNEL = '23'
KEY_LAYER_GROUP = '24'
KEY_LAYER_Z = '25'
KEY_LAYERS = '57'
KEY_TEXT = '31'
KEY_SCALE = '32'

OBJS_TRIGGERS = [
    22, # No Screen Move
    23, # 22-28 are Screen Moves
    24,
    25,
    26,
    27,
    28,
    29, # Old BG
    30, # Old GRND
    32, # Enable Trail
    33, # Disable Trail
    55, # 55-59 are Screen Moves (55 is Unused)
    56,
    57,
    58,
    59,
    104, # Old LINE
    105, # Old OBJ
    221, # Old COLOR 1
    717, # Old COLOR 2
    718, # Old COLOR 3
    743, # Old COLOR 4
    744, # Old 3DL
    899, # Color
    900, # Old GRND 2 (Unused?)
    901, # Move
    915, # Old LINE (Unused?)
    1006, # Pulse
    1007, # Alpha
    1049, # Toggle
    1268, # Spawn
    1346, # Rotate
    1347, # Follow
    1520, # Shake
    1585, # Animate
    1595, # Touch
    1611, # Count
    1612, # Hide Player
    1613, # Show Player
    1616, # Stop
    1811, # Instant Count
    1812, # On Death
    1814, # Follow Player
    1815, # Collision
    1817, # Pickup
    1818, # BG Effect On
    1819 # BG Effect Off
]

OBJS_STATIC_COLOR_KEYS = 'kA13,0,kA15,0,kA16,0,kA14,,kA6,7,kA7,6,kA17,0,kA18,6,kS39,0,kA2,0,kA3,0,kA8,0,kA4,0,kA9,0,kA10,0,kA11,0;'

COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]

TEXT_KILLBOT = [
    '666',
    'You die now',
    'Welcome to HELL',
    'HELL',
    'Fatal wounds',
    'Load failed',
    'No need to live...',
    'DIE ALREADY!',
    'DIE!!!!!',
    'PAIN',
    'ERROR',
    'death',
    'Rest in Peace',
    'Keep Going!',
    'Take a Break',
    'WATCH OUT!',
    'Prepare to DIE',
    'Almost there...',
    'No escape',
    'Your blood..',
    'Keep it up!',
    'Welcome to die',
    '6666666',
    'Now I fear you'
]


def coreIsInt(s):
    try:
        s = int(s)
    except ValueError:
        return False
    return True


def coreIsFloat(s):
    try:
        s = float(s)
    except ValueError:
        return False
    return True

def corePYIPath(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

FILE_PATTERNS = corePYIPath('patterns.txt')


def initialColorDecrypter(encrypted):
    initialColors = str(encrypted)
    initialColors = initialColors[initialColors.index('kS38,') + 5:initialColors.index(',kA13')].split('|')
    for c in initialColors:
        c_split = c.split('_')
        c_dict = {}
        c_key = ''
        for i in range(0, len(c_split) - 1):
            if i % 2 == 0:
                c_key = int(c_split[i])
            else:
                c_value = c_split[i]
                c_dict[c_key] = c_value
        initialColors[initialColors.index(c)] = c_dict
        if len(c_dict) >= 1:
            c_dict[8] = 1
        elif c_dict == {}:
            initialColors.remove(c_dict)
    return initialColors


def initialColorEncrypter(initialColors, encrypted):
    order = [1, 2, 3, 11, 12, 13, 4, 6, 5, 7, 15, 10, 18, 8]
    rep = ''
    for color in initialColors:
        if color:
            for o in order:
                try:
                    rep += str(o) + '_' + str(color[o]) + '_'
                except KeyError:
                    pass
            rep = rep[:len(rep) - 1]
            rep += '|'
    enc_replace = str(encrypted)
    enc_replace = 'kS38,' + rep + enc_replace[enc_replace.index(',kA13'):]
    return enc_replace


def setColorChannel(initialColors, color_channel, r, g, b, blending=0):
    color_found = False
    for color in initialColors:
        try:
            if int(color[6]) == int(color_channel):
                color[1] = r
                color[2] = g
                color[3] = b
                color[5] = blending
                color_found = True
        except KeyError:
            pass
    if not color_found:
        c = {1: r, 2: g, 3: b, 6: color_channel, 5: blending, 7: 1, 15: 0, 18: 0, 8: 1}
        initialColors.append(c)
    return initialColors


def levelObjects(data):
    return data[data.index('kA11,') + 7:]


def objectToDict(data):
    data_split = data.replace('\'', '').split(',')
    data_split = [d for d in data_split if len(d) > 0]
    data_dict = {data_split[i]: data_split[i + 1].replace(';', '') for i in range(0, len(data_split) - 1, 2)}
    for key in data_dict.keys():
        if coreIsFloat(data_dict[key]):
            data_dict[key] = float(data_dict[key])
    for key in data_dict.keys():
        if coreIsInt(data_dict[key]):
            data_dict[key] = int(data_dict[key])
    return data_dict


def objectsToDict(data):
    if data.startswith('b\''):
        data = data[2:]
    if data[len(data) - 1] == '\'':
        data[:len(data) - 1]
    full_split = data.split(';')
    full = [objectToDict(obj) for obj in full_split]
    for d in full:
        if not d:
            full.remove(d)
    return full


def dictAddKeyValue(d, newkey, newvalue):
    d[newkey] = newvalue


def dictToObject(d):
    if d:
        if isinstance(d, dict):
            if 'kS38' not in d.keys():
                keys = sorted([key for key in d.keys()])
            else:
                keys = d.keys()
            data_t = ''
            for key in keys:
                data_t += key + ',' + str(d[key]) + ','
            data_t = data_t[:len(data_t) - 1]
            return data_t
    return ''


def dictToObjects(ddl):
    data_objs = [dictToObject(d) for d in ddl if d]
    data_t = ''
    for obj in data_objs:
        data_t += obj + ';'
    if 'kA11' in data_t:
        data_t = data_t[:data_t.index('kA11')] + 'kA11,0' + data_t[data_t.index('kA11') + 4:]
    # There's probably a more efficient way to do this but I don't care lol
    end_line_found = True
    try:
        _ = data_t.index('kA11')
    except ValueError:
        end_line_found = False
    if end_line_found:
        end_line_index = 0
        for i in range(data_t.index('kA11'), 0, -1):
            if data_t[i] == '|':
                end_line_index = i
                break
        if end_line_index != 0:
            data_t = data_t[:end_line_index] + '|,' + OBJS_STATIC_COLOR_KEYS + data_t[data_t.index('kA11') + 7:]
    return data_t


def objectSetPos(ddl, newx, newy):
    new_ddl = ddl
    for obj in new_ddl:
        obj[KEY_POSX] += (newx * 30) + 15
        obj[KEY_POXY] += (newy * 30) + 15
    return new_ddl


def generatorLevelRange(ddl, spread_x, spread_y, scatter_d, scale_range=0, is_text=False):
    global killbotCurrentProgress, killbotTotalProgress
    new_ddl = ddl
    new_ddl = [d for d in new_ddl if d and str(d) != '{}']
    highest_x = 0
    highest_y = 0
    lowest_x = 99999
    lowest_y = 99999
    for obj in new_ddl:
        try:
            if '1' in obj and obj[KEY_ID] not in OBJS_TRIGGERS:
                if obj[KEY_POSX] < lowest_x:
                    lowest_x = int(obj[KEY_POSX])
                if obj[KEY_POSY] < lowest_y:
                    lowest_y = int(obj[KEY_POSY])
                if obj[KEY_POSX] > highest_x:
                    highest_x = int(obj[KEY_POSX])
                if obj[KEY_POSY] > highest_y:
                    highest_y = int(obj[KEY_POSY])
        except KeyError:
            pass
    multiplier = int((((highest_x - lowest_x) - 15) / 30) / (3 * (spread_x * (400 / spread_x ** 2))))
    #print('spread_x=' + str(spread_x))
    #print('unit length=' + str(highest_x - lowest_x))
    #print('block length=' + str(int(((highest_x - lowest_x) - 15) / 30)))
    #print('multiplier=' + str(multiplier))
    spread_x *= multiplier # iffy on keeping this
    range_x = int((highest_x - lowest_x) / (spread_x + 1))
    used_ddl = []
    for x in range(spread_x):
        new_obj = [{k: obj[k] for k in obj.keys()} for obj in scatter_d]
        new_highest = 0
        new_lowest = 99999
        range_y = 20
        filtered_ddl = [o for o in new_ddl if o and '1' in o and '2' in o
        and not toolObjectIsTrigger(o) and (x * range_x) <= o[KEY_POSX] <= ((x + 1) * range_x)]
        for o in filtered_ddl:
            if o[KEY_POSY] < new_lowest:
                new_lowest = o[KEY_POSY]
            if o[KEY_POSY] > new_highest:
                new_highest = o[KEY_POSY]
        range_y = int((new_highest - new_lowest) / spread_y)
        #print('new_highest=' + str(new_highest))
        #print('new_lowest=' + str(new_lowest))
        #print('range_y=' + str(range_y))
        x_deviation = random.randint(0, range_x)
        negative = random.randint(0, 1)
        if negative:
            x_deviation = -x_deviation
        x_attempt = new_obj[0][KEY_POSX] + (x * range_x) + x_deviation
        x_attempt = abs(x_attempt)
        x_unclumped = True
        for used in used_ddl:
            if used[0] <= x_attempt <= used[1]:
                x_unclumped = False
        if not x_unclumped:
            while not x_unclumped:
                x_deviation = random.randint(0, range_x)
                negative = random.randint(0, 1)
                if negative:
                    x_deviation = -x_deviation
                x_attempt = new_obj[0][KEY_POSX] + (x * range_x) + x_deviation
                x_attempt = abs(x_attempt)
                for used in used_ddl:
                    if used[0] <= x_attempt <= used[1]:
                        continue
                x_unclumped = True
        #print('x_deviation=' + str(x_deviation))
        y_deviation = random.choice([(y * range_y) for y in range(spread_y - 1) 
            if new_highest >= (y * range_y) >= 0]) + new_lowest
        y_attempt = new_obj[0][KEY_POSY] + y_deviation
        y_unclumped = True
        for used in used_ddl:
            if used[2] <= y_attempt <= used[3]:
                y_unclumped = False
        if not y_unclumped:
            while not y_unclumped:
                y_deviation = random.choice([(y * (range_y - 1)) for y in range(spread_y - 1) 
                    if new_highest >= (y * range_y) >= 0]) + new_lowest
                y_attempt = new_obj[0][KEY_POSY] + y_deviation
                for used in used_ddl:
                    if used[2] <= y_attempt <= used[3]:
                        continue
                y_unclumped = True
        #print('scatter_d=' + str(scatter_d))
        for obj in new_obj:
            #killbotCurrentProgress -= 1
            #print(str(killbotCurrentProgress) + '/' + str(killbotTotalProgress))
            #print('obj=' + str(obj))
            try:
                obj[KEY_POSX] += (x * range_x) + x_deviation
                obj[KEY_POSX] = abs(obj[KEY_POSX])
                obj[KEY_POSY] += y_deviation
                if scale_range != 0:
                    scale_range = round(random.uniform(0, scale_range), 2)
                    negative = random.randint(0, 1)
                    if negative:
                        scale_range = -scale_range
                    obj = dictAddKeyValue(obj, KEY_SCALE, str(abs(1 + scale_range)))
                if is_text:
                    use_text = random.choice(TEXT_KILLBOT)
                    obj = dictAddKeyValue(obj, KEY_TEXT, base64.b64encode(use_text.encode()).decode())
            except KeyError:
                pass
        new_ddl += new_obj
        used_highest_x = 0
        used_lowest_x = 99999
        used_highest_y = 0
        used_lowest_y = 99999
        for d in new_obj:
            if d[KEY_POSX] < used_lowest_x:
                used_lowest_x = d[KEY_POSX]
            if d[KEY_POSX] > used_highest_x:
                used_highest_x = d[KEY_POSX]
            if d[KEY_POSY] < used_lowest_y:
                used_lowest_y = d[KEY_POSY]
            if d[KEY_POSY] > used_highest_y:
                used_highest_y = d[KEY_POSY]
        used_ddl.append([used_lowest_x, used_highest_x, used_lowest_y, used_highest_y])
    return new_ddl


def toolGetColorChannels(data):
    initialColors = initialColorDecrypter(data)
    return [channel[6] for channel in initialColors]


def toolSetColorChannel(data, color_channel, rgb, blending=0):
    initialColors = initialColorDecrypter(data)
    #print('channel=' + str(color_channel))
    #print('before=' + str(initialColors))
    initialColors = setColorChannel(initialColors, color_channel, rgb[0], rgb[1], rgb[2], blending)
    #print('after=' + str(initialColors))
    new_data = initialColorEncrypter(initialColors, data)
    return new_data


def toolSetTriggerColor(d, new_color):
    new_d = d
    dictAddKeyValue(new_d, KEY_R, new_color[0])
    dictAddKeyValue(new_d, KEY_G, new_color[1])
    dictAddKeyValue(new_d, KEY_B, new_color[2])
    return new_d


def toolObjectIsTrigger(d):
    return KEY_ID in d.keys() and d[KEY_ID] in OBJS_TRIGGERS


def toolSavePattern(data, name):
    obj = levelObjects(data)
    file_data = []
    f = open(FILE_PATTERNS, 'r')
    file_data = [line for line in f if len(line) > 2]
    for line in file_data:
        line_split = line.split(':::::')
        if line_split[1].startswith('0;'):
            file_data[file_data.index(line)] = line_split[0] + ':::::' + (line_split[1])[2:]
    f.close()
    file_data.append(name + ':::::' + obj)
    f = open(FILE_PATTERNS, 'w')
    f.truncate()
    f.write(''.join([l + '\n' for l in file_data]))
    f.close()


def toolLoadPattern(name):
    file_data = []
    f = open(FILE_PATTERNS, 'r')
    file_data = [line for line in f if len(line) > 2]
    for line in file_data:
        line_split = line.split(':::::')
        if line_split[1].startswith('0;'):
            file_data[file_data.index(line)] = line_split[0] + ':::::' + (line_split[1])[2:]
    f.close()
    for line in file_data:
        line_split = line.split(':::::')
        if line_split[0] == name:
            return line_split[1]
    """
    pattern = PATTERNS[name]
    if pattern.startswith('0;'):
        pattern = pattern[2:]
    return pattern
    """


def toolPatternDict(name):
    data = toolLoadPattern(name)
    return objectsToDict(data)


def toolLevelSize(data):
    ddl = objectsToDict(data)
    return len(ddl)


def killbotColorChannels(data):
    alt = 1
    new_data = data
    for channel in toolGetColorChannels(new_data):
        color = None
        if alt:
            color = COLOR_GREEN
            alt = 0
        else:
            color = COLOR_RED
            alt = 1
        new_data = toolSetColorChannel(new_data, channel, color)
    #print('old=' + str(new_data))
    #print('\n'*100)
    alt = abs(alt - 1)
    new_data = toolSetColorChannel(new_data, COLOR_CHANNEL_OBJ, [COLOR_RED, COLOR_GREEN][alt])
    alt = abs(alt - 1)
    new_data = toolSetColorChannel(new_data, COLOR_CHANNEL_3DL, [COLOR_GREEN, COLOR_RED][alt])
    for color in range(1, 999):
        alt = abs(alt - 1)
        new_data = toolSetColorChannel(new_data, color, [COLOR_GREEN, COLOR_RED][alt])
    #print('new=' + str(new_data))
    ddl = objectsToDict(new_data)
    alt = 1
    for obj in ddl:
        if toolObjectIsTrigger(obj):
            color = None
            if alt:
                color = COLOR_GREEN
                alt = 0
            else:
                color = COLOR_RED
                alt = 1
            toolSetTriggerColor(obj, [COLOR_GREEN, COLOR_RED][alt])
    new_data = dictToObjects(ddl)
    return new_data


killbotTotalProgress = 1
killbotCurrentProgress = 1


OBJS_KILLBOT_PROGRESS = [
    [toolPatternDict('FLASH_CRY'), PSPREAD_FLASH_CRY],
    [toolPatternDict('FLASH_8D'), PSPREAD_FLASH_8D],
    [toolPatternDict('FLASH_HA'), PSPREAD_FLASH_HA],
    [toolPatternDict('FLASH_DIE'), PSPREAD_FLASH_DIE],
    [toolPatternDict('FLASH_PAIN'), PSPREAD_FLASH_PAIN],
    [toolPatternDict('S_SQUARE'), PSPREAD_S_SQUARE],
    [toolPatternDict('S_GEAR'), PSPREAD_S_GEAR],
    [toolPatternDict('TEXT_CRY'), PSPREAD_TEXT_CRY]
]


def killbotGlobalProgress():
    global killbotTotalProgress, killbotCurrentProgress
    return [killbotTotalProgress, killbotCurrentProgress]


def killbotProgressEstimator():
    global killbotTotalProgress, killbotCurrentProgress
    killbotTotalProgress = sum([len(prog[0]) * prog[1] for prog in OBJS_KILLBOT_PROGRESS])
    killbotCurrentProgress = killbotTotalProgress


def killbotObjects(data):
    ddl = objectsToDict(data)
    print('Downloading killbot.exe...')
    ddl = generatorLevelRange(ddl, PSPREAD_FLASH_CRY, PSPREAD_FLASH_CRY, toolPatternDict('FLASH_CRY'))
    print('Installing program...')
    ddl = generatorLevelRange(ddl, PSPREAD_FLASH_8D, PSPREAD_FLASH_8D, toolPatternDict('FLASH_8D'))
    print('Virus detected...')
    ddl = generatorLevelRange(ddl, PSPREAD_FLASH_HA, PSPREAD_FLASH_HA, toolPatternDict('FLASH_HA'))
    print('Deleting virus, delete failed...')
    ddl = generatorLevelRange(ddl, PSPREAD_FLASH_DIE, PSPREAD_FLASH_DIE, toolPatternDict('FLASH_DIE'))
    print('Fatal error...')
    ddl = generatorLevelRange(ddl, PSPREAD_FLASH_PAIN, PSPREAD_FLASH_PAIN, toolPatternDict('FLASH_PAIN'))
    print('Fatal wounds...')
    ddl = generatorLevelRange(ddl, PSPREAD_S_SQUARE, PSPREAD_S_SQUARE, toolPatternDict('S_SQUARE'), 
        PSCALE_S_SQUARE)
    print('Cry...')
    ddl = generatorLevelRange(ddl, PSPREAD_S_GEAR, PSPREAD_S_GEAR, toolPatternDict('S_GEAR'), 
        PSCALE_S_GEAR)
    print('Loading map_02.dat...')
    ddl = generatorLevelRange(ddl, PSPREAD_TEXT_CRY, PSPREAD_TEXT_CRY, toolPatternDict('TEXT_CRY'), 
        scale_range=0, is_text=True)
    print('Error map not found...')
    return dictToObjects(ddl)

# Unused Killbot Objects
#ddl = generatorLevelRange(ddl, PSPREAD_FLASH_NO, PSPREAD_FLASH_NO, toolPatternDict('FLASH_NO'))
#ddl = generatorLevelRange(ddl, PSPREAD_FLASH_AHAH, PSPREAD_FLASH_AHAH, toolPatternDict('FLASH_AHAH'))
#ddl = generatorLevelRange(ddl, PSPREAD_S_CIRCLE, PSPREAD_S_CIRCLE, toolPatternDict('S_CIRCLE'), 
#    PSCALE_S_CIRCLE)
#ddl = generatorLevelRange(ddl, PSPREAD_S_CUBE, PSPREAD_S_CUBE, toolPatternDict('S_CUBE'), 
#    PSCALE_S_CUBE)