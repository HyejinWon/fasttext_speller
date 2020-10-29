import re
import random
import copy
import math

#유니코드 한글 시작 : 44032 / 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# -----------------------------------edit distance 기준 오타 생성----------------------
# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# -----------------------------------------------------------------------------------

# ------------------필요한가...?--------------------
#초성 된소리 리스트
KO_ATOM_C = { 'ㄲ': ('ㄱ','ㄱ'), 'ㄸ': ('ㄷ','ㄷ'), 'ㅃ': ('ㅂ','ㅂ'), 'ㅆ': ('ㅅ','ㅅ'), 'ㅉ': ('ㅈ','ㅈ')}
#중성 이중모음 리스트
KO_ATOM_JU = { 'ㅘ': ( 'ㅗ', 'ㅏ' ), 'ㅙ' : ( 'ㅗ', 'ㅐ' ), 'ㅚ' : ( 'ㅗ', 'ㅣ' ), 'ㅝ' : ( 'ㅜ', 'ㅓ' ), 'ㅞ' : ( 'ㅜ', 'ㅔ' ), 'ㅟ': ( 'ㅜ', 'ㅣ' ), 'ㅢ': ( 'ㅡ', 'ㅣ' )}
#종성 이중모음 리스트
KO_ATOM_JO = { 'ㄲ' : ( 'ㄱ', 'ㄱ' ), 'ㄳ': ( 'ㄱ', 'ㅅ' ), 'ㄵ': ( 'ㄴ', 'ㅈ' ), 'ㄶ': ( 'ㄴ', 'ㅎ' ), 'ㄺ' : ( 'ㄹ', 'ㄱ' ), 'ㄻ' : ( 'ㄹ', 'ㅁ' ), 'ㄼ' : ( 'ㄹ', 'ㅂ' ), 'ㄽ' : ( 'ㄹ', 'ㅅ' ),\
      'ㄾ': ( 'ㄹ', 'ㅌ' ), 'ㄿ': ( 'ㄹ', 'ㅍ' ), 'ㅀ' : ( 'ㄹ', 'ㅎ' ), 'ㅄ': ( 'ㅂ', 'ㅅ' ), 'ㅆ': ( 'ㅅ', 'ㅅ' )}
#----------------------------------------------------

# -----------------------------------키보드 기준 오타생성-----------------------------
# 키보드 기준 초성, 종성 (된소리나 이중 받침은 제외)
keyboard_cartesian_CH = {'ㅂ': {'x':0, 'y':0}, 'ㅈ': {'x':1, 'y':0}, 'ㄷ': {'x':2, 'y':0}, 'ㄱ': {'x':3, 'y':0}, \
'ㅅ': {'x':4, 'y':0}, 'ㅁ': {'x':0, 'y':1},'ㅋ': {'x':0, 'y':2},'ㄴ': {'x':1, 'y':1},'ㅌ': {'x':1, 'y':2},\
'ㅇ': {'x':2, 'y':1},'ㅊ': {'x':2, 'y':2}, 'ㄹ': {'x':3, 'y':1}, 'ㅎ': {'x':4, 'y':1}, 'ㅍ': {'x':3, 'y':2} }
# 키보드 기준 중성
# 예외적으로, 'ㅔ': {'x':4, 'y':0} 를 keyboard_cartesian_MO에 넣어줌 으로써 문제 해결
keyboard_cartesian_JU = {'ㅛ': {'x':0, 'y':0}, 'ㅕ': {'x':1, 'y':0}, 'ㅑ': {'x':2, 'y':0}, 'ㅐ': {'x':3, 'y':0}, \
     'ㅗ': {'x':0, 'y':1}, 'ㅓ': {'x':1, 'y':1}, 'ㅏ': {'x':2, 'y':1}, 'ㅣ': {'x':3, 'y':1},\
        'ㅠ': {'x':0, 'y':2}, 'ㅜ': {'x':1, 'y':2}, 'ㅡ': {'x':2, 'y':2} }

# 키보드 shift 
keyboard_cartesian_SH = {'ㅃ':('ㅂ','ㅉ','ㅁ'),'ㅉ':('ㅈ','ㅃ','ㄸ','ㄴ'),'ㄸ':('ㄷ','ㅉ','ㄲ','ㅇ'),'ㄲ':('ㄱ','ㅆ','ㄸ','ㄹ'),'ㅆ':('ㅅ','ㄲ','ㅎ')}
# 이중모음이 변경될 수 있는 항목
keyboard_cartesian_MO = {'ㅔ':('ㅐ','ㅣ','ㅖ'),'ㅘ':('ㅚ','ㅗ','ㅏ'), 'ㅙ':('ㅗ','ㅣ','ㅚ'), 'ㅚ' : ('ㅘ','ㅗ','ㅣ','ㅙ'), 'ㅝ' : ( 'ㅜ', 'ㅓ' ), 'ㅞ' : ('ㅟ', 'ㅜ', 'ㅔ' ), 'ㅟ': ( 'ㅞ','ㅜ', 'ㅣ' ), 'ㅢ': ( 'ㅡ', 'ㅣ','ㅟ' ),'ㅒ':('ㅐ','ㅑ','ㅖ','ㅣ'),'ㅖ':('ㅔ','ㅒ','ㅣ')}
# 이중 받침이 변경될 수 있는 항목
keyboard_cartesian_BA = {'ㄲ' : ( 'ㄱ', 'ㅆ', 'ㄸ'), 'ㄳ': ( 'ㄱ','ㅅ'), 'ㄵ': ( 'ㄴ','ㅈ' ), 'ㄶ': ( 'ㄴ','ㅎ' ), 'ㄺ' : ( 'ㄹ','ㄱ' ), 'ㄻ' : ( 'ㄹ','ㅁ','ㄼ' ), 'ㄼ' : ( 'ㄹ','ㅂ', 'ㄻ' ), 'ㄽ' : ( 'ㄹ','ㅅ','ㄺ'),\
      'ㄾ': ( 'ㄹ','ㅌ' ), 'ㄿ': ( 'ㄹ','ㅍ','ㅀ' ), 'ㅀ' : ( 'ㄹ','ㅎ','ㄿ','ㄽ' ), 'ㅄ': ( 'ㅂ','ㅅ'), 'ㅆ': ( 'ㅅ','ㄲ')}
# -----------------------------------------------------------------------------------

def check_hangul(word):
    return re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', word)

def check_except(word):
    '''
    쉼표, 영어 등이 들어간 경우 return 값 가짐
    '''
    return re.match('.*[0-9a-zA-Z,]+.*',word)

# 자소 완전 분해 ex. ㅁㅏ(ㄴㅎ) ㄷㅏ
def jamoAtomSplit(keyword):
    result = list()

    for word in list(keyword.strip()):
        temp = list()
        if check_hangul(word) is not None or check_except is None:
            #초성
            char_code = ord(word) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            if CHOSUNG_LIST[char1] in KO_ATOM_C:
                temp.append(KO_ATOM_C[CHOSUNG_LIST[char1]])
            else:
                temp.append(CHOSUNG_LIST[char1])
            #중성
            char2 = int((char_code-(CHOSUNG *char1)) / JUNGSUNG)
            if JUNGSUNG_LIST[char2] in KO_ATOM_JU:
                temp.append(KO_ATOM_JU[JUNGSUNG_LIST[char2]])  
            else:
                temp.append(JUNGSUNG_LIST[char2])

            #종성
            char3 = int((char_code - (CHOSUNG *char1) - (JUNGSUNG *char2)))
            if JONGSUNG_LIST[char3] in KO_ATOM_JO:
                temp.append(KO_ATOM_JO[JONGSUNG_LIST[char3]]) 
            else:
                temp.append(JONGSUNG_LIST[char3])
        else:
            #print("is not hangul char",word)
            temp.append(word)

        result.append(temp)


    return result

# 자소 분해 ex. ㅁㅏㄶ ㄷㅏ
def jamoSplit(keyword):
    result = list()
    hangul_index = list() # 한글만 들어간 곳의 인덱스를 저장함

    for i, word in enumerate(list(keyword.strip())):
        temp = list()
        if check_hangul(word) is not None or check_except is None:
            #초성
            char_code = ord(word) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            temp.append(CHOSUNG_LIST[char1])

            #중성
            char2 = int((char_code-(CHOSUNG *char1)) / JUNGSUNG)
            temp.append(JUNGSUNG_LIST[char2])

            #종성
            char3 = int((char_code - (CHOSUNG *char1) - (JUNGSUNG *char2)))
            temp.append(JONGSUNG_LIST[char3])

            hangul_index.append(i)
        else:
            #print("is not hangul char",word)
            temp.append(word)

        result.append(temp)


    return result, hangul_index
    #return ''.join(result)

'''
def makeCharErrorExcept(word):
    except_wordlist = [(match.start(), match.end()) for match in re.finditer(['a-zA-Z0-9,']+,word)]
    
    return 0

def check_only_hangul(word):
    return [m.start() for m in re.finditer('[ㄱ-ㅎㅏ-ㅣ가-힣]',word)]
'''

def deletionAction(target):
    target[2] = JONGSUNG_LIST[0]

    return target
    
def substitutionAction(random_int, target):
    #초성
    if random_int == 1:
        char1 = CHOSUNG_LIST.index(target[0])

        while True:
            char_rand = random.randint(0,18)
            if char_rand != char1:
                target[0] = CHOSUNG_LIST[char_rand]
                break     
    #중성
    elif random_int == 2:
        char1 = JUNGSUNG_LIST.index(target[1])
        while True:
            char_rand = random.randint(0,20)
            if char_rand != char1:
                target[1] = JUNGSUNG_LIST[char_rand]
                break   
    #종성
    else:
        char1 = JONGSUNG_LIST.index(target[2])
        while True:
            char_rand = random.randint(0,27)
            if char_rand != char1:
                target[2] = JONGSUNG_LIST[char_rand]
                break    
    
    return target

# jamoSplit() 함수를 거친뒤 진행
# edit distance 기준으로 오타 생성
def editDistance_error(wordList, hangul_index):
    #wordList 중에서 한 개의 음절에만 오타를 부여함
    
    target_index = random.choice(hangul_index)
    target = wordList[target_index]
    rawindex = wordList.index(target)

    #초성, 중성, 종성 중에서 고르기
    random_int = random.randint(1,3)
    #edit distance에서 delete 1, insert & substitution 2 중에서 고르기
    random_edit = random.randint(1,2)

    #종성에 대해서만 삭제연산 일어남
    if random_edit == 1 and target[2] != ' ':
        target = deletionAction(target)

    elif random_edit == 2 or (random_edit == 1 and target[2] == ' '):
        target = substitutionAction(random_int, target)

    return rawindex, mergeCharSplit(target)

# 필요시 사용
def euclidean_distance(a,b):
    X = (keyboard_cartesian[a]['x'] - keyboard_cartesian[b]['x'])**2
    Y = (keyboard_cartesian[a]['y'] - keyboard_cartesian[b]['y'])**2
    return math.sqrt(X+Y)

def get_key(val,AtomType):
    if AtomType: #True = 초성
        for key, value in keyboard_cartesian_CH.items():
            if val == value:
                return key

    else:
        for key, value in keyboard_cartesian_JU.items():
            if val == value:
                return key


def positive_or_negative():
    return 1 if random.random() < 0.5 else -1

def changing_value(target_dic,target_index, random_add, porn, binar):
    
    if random_add == 'x':
        x = target_dic[target_index][random_add] + porn
        y = target_dic[target_index]['y']
    else:
        x = target_dic[target_index]['x']
        y = target_dic[target_index][random_add] + porn
    changed_value = get_key({'x':x,'y':y}, binar)

    if changed_value is None:
        if random_add == 'x':
            x = target_dic[target_index][random_add] - porn
            y = target_dic[target_index]['y']
        else:
            x = target_dic[target_index]['x']
            y = target_dic[target_index][random_add] - porn
        changed_value = get_key({'x':x,'y':y}, binar)
        

    return changed_value

def changing_value_shift(target_dic, target_index):
    return random.choice(target_dic[target_index])

def changing_value_shift_all(target_dic, target_index):
    return target_dic[target_index]   

def changing_value_doensori(jamo):
    if jamo == 'ㅅ':
        return 'ㅆ'
    elif jamo == 'ㄱ':
        return 'ㄲ'
    elif jamo == 'ㄷ':
        return 'ㄸ'
    elif jamo == 'ㅈ':
        return 'ㅉ'
    elif jamo == 'ㅂ':
        return 'ㅃ'    

# jamoSplit() 함수를 거친뒤 진행
# 키보드거리에 의한 오타 생성
def keyboardDistance_error(wordList, hangul_index):
    
    target_index = random.choice(hangul_index)
    target = wordList[target_index]
    rawindex = wordList.index(target)

    #print(target)

    if target[2] == ' ':
        random_int = random.randint(1,2)
    else:
        random_int = random.randint(1,3)
    
    random_add = random.choice('xy')

    if random_int == 1:
        try:
            change_value = changing_value(keyboard_cartesian_CH, target[0], random_add, positive_or_negative(), True)
        except KeyError:
            change_value = changing_value_shift(keyboard_cartesian_SH, target[0])

        target[0] = change_value

    elif random_int == 2:
        try:
            change_value = changing_value(keyboard_cartesian_JU, target[1], random_add, positive_or_negative(), False)
        except KeyError:
            change_value = changing_value_shift(keyboard_cartesian_MO, target[1])

        target[1] = change_value
        
    elif random_int == 3:
        try:
            change_value = changing_value(keyboard_cartesian_CH, target[2], random_add, positive_or_negative(), True)
        except KeyError:
            change_value = changing_value_shift(keyboard_cartesian_BA, target[2])
        
        target[2] = change_value
        
    return rawindex, mergeCharSplit(target)


# jamoAtomSplit() 함수를 거친 뒤 진행됨
# Todo : 연음법칙에 의한 오타 생성
def yeoneum(wordList):

    for word in wordList:
        if len(word) == 1:
            continue
        else:
            if [0] == 'ㅇ':
                print('a')
        
def mergeCharSplit(inputlist):
    # 쪼개놓은 한글을 합치는 코드
    try:
        characterValue = ( (CHOSUNG_LIST.index(inputlist[0]) * 21) + JUNGSUNG_LIST.index(inputlist[1])) * 28 + JONGSUNG_LIST.index(inputlist[2]) + 0xAC00
        return chr(characterValue)

    except:
        print(inputlist)



# eumjol_bi 를 위한 함수임,, 
# 음절에 대해서 키보드 거리만큼의 나올수 잇는 음절 다 만들어서 내보낼거임
# eumjol_bi에서 make_candidate를 그다음에 사용하면됌
# jamoAtomSplit() 함수를 거친 뒤 진행됨
def keyboardDistance_error_onlyeumjol(wordList):
    
    #print(wordList)

    # 초성, 중성
    if wordList[2] == ' ':
        ran = range(2)
    else: # 초성, 중성, 종성
        ran = range(3)

    # 초성, 중성, 종성 +-1 씩해서 찾은 단어들이 [[['ㄱ','ㅈ'],'ㅏ','ㅌ'],['ㄷ',['ㅓ','ㅣ],'ㅌ']...] 으로 들어가있음
    # 순서는 초성, 중성, 종성 순서임.
    result = []
    for index, i in enumerate(ran):
        temp = list()
        if index == 0:
            try:
                for j in [-1, 1]: # 좌, 우
                    change_value = changing_value(keyboard_cartesian_CH, wordList[0], 'x', j, True)
                    change_value2 = changing_value(keyboard_cartesian_CH, wordList[0], 'y', j, True)
                    
                    temp.append(change_value)
                    temp.append(change_value2)
                # 받침이 'ㅅ'으로 되어서 오타가 난 경우, 'ㅆ'의 경우를 넣어주는 부분
                if wordList[0] in ['ㅅ','ㄱ','ㄷ','ㅈ','ㅂ']:
                    temp.append(changing_value_doensori(wordList[0]))

                result.append([temp, wordList[1], wordList[2]])

            except KeyError: 
                change_value = changing_value_shift_all(keyboard_cartesian_SH, wordList[0])
                result.append([change_value, wordList[1], wordList[2]])
        
        elif index == 1:
            try:
                for j in [-1, 1]: # 좌, 우
                    change_value = changing_value(keyboard_cartesian_JU, wordList[1], 'x', j, False)
                    change_value2 = changing_value(keyboard_cartesian_JU, wordList[1], 'y', j, False)
                    
                    temp.append(change_value)
                    temp.append(change_value2)

                result.append([wordList[0], temp, wordList[2]])

            except KeyError:
                change_value = changing_value_shift_all(keyboard_cartesian_MO, wordList[1])
                result.append([wordList[0], change_value, wordList[2]])
            
        elif index == 2:
            try:
                for j in [-1, 1]: # 좌, 우
                    change_value = changing_value(keyboard_cartesian_CH, wordList[2], 'x', j, True)
                    change_value2 = changing_value(keyboard_cartesian_CH, wordList[2], 'y', j, True)
                    
                    temp.append(change_value)
                    temp.append(change_value2) 

                # 받침이 'ㅅ'으로 되어서 오타가 난 경우, 'ㅆ'의 경우를 넣어주는 부분
                if wordList[2] in ['ㅅ','ㄱ','ㄷ','ㅈ','ㅂ']:
                    temp.append(changing_value_doensori(wordList[2]))

                result.append([wordList[0], wordList[1], temp])          

            except KeyError:
                change_value = changing_value_shift_all(keyboard_cartesian_BA, wordList[2])
                result.append([wordList[0], wordList[1], change_value])                

    return result

"""
if __name__ == "__main__":
    #sample = 'ㅁㅁ'
    #keyboardDistance_error(sample)

    
    sample = '닦었쓴괞,'
    
    #jamo = jamoAtomSplit(sample)
    #print(jamo)
    '''
    jamo = jamoSplit(sample)
    
    index, result = keyboardDistance_error(jamo)
    
    print(sample[:index], result, sample[index +1 :])
    '''
    # deepcopy 사용
    jamo, hangul_index =  jamoSplit(sample)    
    raw = copy.deepcopy(jamo)

    
    original_index, error = editDistance_error(jamo, hangul_index)
    
    print(raw)
    print(original_index, error)
    print(raw[original_index])

    a = mergeCharSplit(error)
    print(sample[:original_index],a,sample[original_index +1 :])
    #print(a)
    
"""