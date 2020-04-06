import os
import re
import time
import traceback

ads = ['3xplanet', '3XPLANET', '.com', '.net','.COM','.NET','.la','.me','.1080p','.720p','.cc','SIS001','sis001','-720p','-1080p','.HD','FHD','hjd2048','456k.me','psk.la']

def check_part_format(filename):  # 识别不规范的分集文件名
    for ad in ads:
        if ad in filename:
            filename = filename.replace(ad,'')
    if '_' in filename:
        filename = filename.replace('_','-')
    if re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-{0,1}[a-fA-F]{1}\.', filename):  # 匹配 MIDE-123B / MIDE-123-B这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-0{0,1}[1-9]{1}',filename):  # 匹配 abp-758-2 / abp-758-02这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6}[0-9]{2,4})-0{0,1}[1-9]{1}',filename):  # 匹配 GIRO02-02这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6}-[0-9]{2,5})\s{1,7}[a-zA-Z]{1}', filename):  # 匹配 "IDBD-304   A"这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6}-[0-9]{2,5})(cd|CD)[1-9]{1}', filename):  # 匹配 "mxt-020cd6"这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})0{2}([0-9]{2,5})hhb([1-9]{1})', filename):  # 匹配 "iptd00781hhb1"这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})([0-9]{2,5})hhb([1-9]{1})', filename):  # 匹配 "iptd781hhb1"这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD([a-fA-F]{1})', filename):  # 匹配 'RBD-366HDB' 这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([1-9]{1,2})\.', filename): #  匹配 (PRESTIGE)(SOR-018)浜辺の美少女を、本気でヤッちゃいました。2014 vol.3_2.wmv 这样的分集，注意_已被替换成-
        return True
    elif re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([a-gA-G]{1})\.', filename): #  匹配 SUPD-106 - DIGITAL CHANNEL DC106 石原莉奈-A.wmv 这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5}).{3,}HD([1-9]{1})', filename):  # 匹配 '(SOE539)FULLHD1' 这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD-([1-9]{1})', filename):# 匹配 IPTD873HD-1.wmv 这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})0{2}([0-9]{3,5})-([0-9]{1})', filename):# 匹配 1dandy00386-0.mp4 这样的分集
        return True
    elif re.search('([a-zA-Z]{2,6})-?([0-9]{3,5})hhb-([a-zA-Z]{1})', filename): # 匹配 iptd566hhb_B.wmv 这样的分集
        return True
    elif re.search('([0-9]{6}-[0-9]{3})-(.*)whole([0-9]{1})',filename):  #  匹配 090214_874-1pon-whole1_hd.mp4 这样的分集
        return True
    else:
        return False

def check_name(filename):  # 识别不规范的文件名
    for ad in ads:
        if ad in filename:
            filename = filename.replace(ad,'')
    if '_' in filename:
        filename = filename.replace('_','-')
    if re.search('[a-zA-Z]{2,6}[0-9]{2,5}\.',filename):
        return True
    elif re.search('[a-zA-Z]{2,6}-{0,1}[0-9]{2,5}FHD', filename):
        return True
    elif re.search('(heyzo).*([0-9]{4})', filename.lower()):  #  识别 heyzo_hd_1001_full.mp4
        return True



def format_part(filename):
    mapping = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7'}
    new_name = filename
    case = ''
    try:
        if '_' in new_name:
            new_name = new_name.replace('_','-')
        for ad in ads:
            if ad in new_name:
                new_name = new_name.replace(ad, '')   # 去掉3xplanet之类的广告字符
        ####################   规范格式化分集  #########################
        if re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-{0,1}([a-fA-F]{1})\.', new_name): # 匹配 MIDE-123B这样的分集
            serial = re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-{0,1}([a-fA-F]{1})', new_name).group(1)  # 提取番号 MIDE-123
            part = re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-{0,1}([a-fA-F]{1})', new_name).group(2)   # 提取分集 B
            new_name = serial + '-cd' + part.replace(part,mapping[part.lower()])
            case = '1'
        elif re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-0{0,1}[1-9]{1}',new_name):   # 匹配 abp-758-2 / abp-758-02这样的分集
            serial = re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-(0{0,1}[1-9]{1})',new_name).group(1)  # 提取番号 abp-758
            part = re.search('([a-zA-Z]{2,6}-[0-9]{2,5})-(0{0,1}[1-9]{1})',new_name).group(2).replace('0','',1)  # 提取分集 2
            new_name = serial + '-cd' + part
            case = '2'
        elif re.search('([a-zA-Z]{2,6}(-{1}|_{1})[0-9]{2,5})\s{1,7}([a-fA-F]{1})', new_name):  # 匹配 "IDBD-304   A"这样的分集
            serial = re.search('([a-zA-Z]{2,6}(-{1}|_{1})[0-9]{2,5})\s{1,7}[a-fA-F]{1}', new_name).group(1)  # 提取番号IDBD-304
            part = re.search('([a-zA-Z]{2,6}-[0-9]{2,5})\s{1,7}([a-fA-F]{1})', new_name).group(2)  # 提取分集 A
            new_name = serial + '-cd' + part.replace(part, mapping[part.lower()])
            case = '3'
        elif re.search('([a-zA-Z]{2,6}(-{1}|_{1})[0-9]{2,5})(cd|CD)([0-9]{1})', new_name):  # 匹配"mxt-020cd6"这样的分集
            serial = re.search('([a-zA-Z]{2,6}(-{1}|_{1})[0-9]{2,5})(cd|CD)([0-9]{1})',new_name).group(1)  # 提取番号mxt-020
            part = re.search('([a-zA-Z]{2,6}(-{1}|_{1})[0-9]{2,5})(cd|CD)([0-9]{1})',new_name).group(4)  # 提取分集 6
            new_name = serial + '-cd' + part
            case = '4'
        elif re.search('([a-zA-Z]{2,6}[0-9]{2,4})-0{0,1}[1-9]{1}', new_name):  # 匹配 GIRO02-02 / GIRO02-2这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})([0-9]{2,4})-0{0,1}[1-9]{1}',new_name).group(1)  # 提取字母GIRO
            serial_num = re.search('([a-zA-Z]{2,6})([0-9]{2,4})-0{0,1}[1-9]{1}',new_name).group(2)   # 提取数字02
            part = re.search('([a-zA-Z]{2,6})([0-9]{2,4})-(0{0,1}[1-9]{1})',new_name).group(3).replace('0','',1)  # 提取分集02
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '5'
        elif re.search('([a-zA-Z]{2,6})0{2}([0-9]{2,5})hhb([1-9]{1})', new_name):  # 匹配 iptd00781hhb1
            serial_alph =  re.search('([a-zA-Z]{2,6})0{2}([0-9]{2,5})hhb([1-9]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})0{2}([0-9]{2,5})hhb([1-9]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})0{2}([0-9]{2,5})hhb([1-9]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '6'
        elif re.search('([a-zA-Z]{2,6})([0-9]{2,5})hhb([1-9]{1})', new_name):  # 匹配 "iptd781hhb1"这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})([0-9]{2,5})hhb([1-9]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})([0-9]{2,5})hhb([1-9]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})([0-9]{2,5})hhb([1-9]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '7'

        elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD([a-fA-F]{1})', new_name):  # 匹配 'RBD-366HDB' 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD([a-fA-F]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD([a-fA-F]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD([a-fA-F]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part.replace(part, mapping[part.lower()])
            case = '8'
        elif re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([1-9]{1,2})\.',new_name):  # 匹配 (PRESTIGE)(SOR-018)浜辺の美少女を、本気でヤッちゃいました。2014 vol.3_2.wmv 这样的分集，注意_已被替换成-
            serial_alph = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([1-9]{1,2})\.', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([1-9]{1,2})\.', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([1-9]{1,2})\.', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '9'
        elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5}).{3,}HD([1-9]{1})', new_name):   # 匹配 '(SOE539)FULLHD1' 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5}).{3,}HD([1-9]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5}).{3,}HD([1-9]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5}).{3,}HD([1-9]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '10'
        elif re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD-([1-9]{1})', new_name):  # 匹配 IPTD873HD-1.wmv 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD-([1-9]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD-([1-9]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})[-]{0,1}([0-9]{2,5})HD-([1-9]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part
            case = '11'
        elif re.search('([a-zA-Z]{2,6})0{2}([0-9]{3,5})-([0-9]{1})', new_name):  # 匹配 1dandy00386-0.mp4 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})0{2}([0-9]{3,5})-([0-9]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})0{2}([0-9]{3,5})-([0-9]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})0{2}([0-9]{3,5})-([0-9]{1})', new_name).group(3).replace('0','')
            case = '12'
            if part:  # 判断分集是否为0，为0即只有一集
                new_name = serial_alph + '-' + serial_num + '-cd' + part
            else:
                new_name = serial_alph + '-' + serial_num
        elif re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([a-gA-G]{1})\.',new_name):  # 匹配 SUPD-106 - DIGITAL CHANNEL DC106 石原莉奈-A.wmv 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([a-gA-G]{1})\.',new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([a-gA-G]{1})\.',new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})-([0-9]{2,5}).{4,}-([a-gA-G]{1})\.',new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part.replace(part, mapping[part.lower()])
            case = '13'
        elif re.search('([a-zA-Z]{2,6})-?([0-9]{3,5})hhb-([a-zA-Z]{1})', new_name):  # 匹配 iptd566hhb_B.wmv 这样的分集
            serial_alph = re.search('([a-zA-Z]{2,6})-?([0-9]{3,5})hhb-([a-zA-Z]{1})', new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})-?([0-9]{3,5})hhb-([a-zA-Z]{1})', new_name).group(2)
            part = re.search('([a-zA-Z]{2,6})-?([0-9]{3,5})hhb-([a-zA-Z]{1})', new_name).group(3)
            new_name = serial_alph + '-' + serial_num + '-cd' + part.replace(part, mapping[part.lower()])
            case = '14'

        ####################   规范化无码分集  #########################
        elif re.search('([0-9]{6}-[0-9]{3})-(.*)whole([0-9]{1})', new_name):  # 匹配 090214_874-1pon-whole1_hd.mp4 这样的分集
            serial_num = re.search('([0-9]{6}-[0-9]{3})-(.*)whole([0-9]{1})', new_name).group(1)
            part = re.search('([0-9]{6}-[0-9]{3})-(.*)whole([0-9]{1})', new_name).group(3)
            new_name = serial_num.replace('-','_') + '-' + 'cd' + part
            case = '15'

        ####################   规范格式化分集  #########################

        ####################   规范格式化名称  #########################
        elif re.search('[a-zA-Z]{2,6}[0-9]{3,5}\.',new_name):  # 匹配 AVOP122这样的名称
            serial_alph = re.search('([a-zA-Z]{2,6})([0-9]{3,5})\.',new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})([0-9]{3,5})\.',new_name).group(2)
            new_name = serial_alph + '-' +serial_num
            case = '16'
        elif re.search('[a-zA-Z]{2,6}-{0,1}[0-9]{2,5}FHD', new_name):  # 匹配 mide330FHD
            serial_alph = re.search('([a-zA-Z]{2,6})-{0,1}([0-9]{2,5})FHD',new_name).group(1)
            serial_num = re.search('([a-zA-Z]{2,6})-{0,1}([0-9]{2,5})FHD', new_name).group(2)
            new_name = serial_alph + '-' + serial_num
            case = '17'
        elif re.search('(heyzo).*([0-9]{4})', new_name.lower()):  # 识别 heyzo_hd_1001_full.mp4
            serial_alph = re.search('(heyzo).*([0-9]{4})', new_name.lower()).group(1)
            serial_num = re.search('(heyzo).*([0-9]{4})', new_name.lower()).group(2)
            new_name = serial_alph + '-' + serial_num
            case = '18'
    finally:
        return new_name, case



if __name__ == '__main__':

    try:
        target_dir = r"Y:\downloaded_HGST\aria2\downloads\temp"
        for filename in os.listdir(target_dir):
                if not os.path.isdir(os.path.join(target_dir,filename)):
                    if check_part_format(filename) or check_name(filename):
                        new_name, case = format_part(filename)
                        ext = os.path.splitext(filename)[1]
                        print(filename + ' has been renamed to: ' + new_name + ext + ', the case is: ' + case)
                        os.rename(os.path.join(target_dir,filename), os.path.join(target_dir, new_name) + ext)
    except:
        traceback.print_exc()
    '''
    filename = 'hjd2048.com_080119_878-1pon-1080p.mp4'
    if check_part_format(filename) or check_name(filename):
        print(format_part(filename))
    '''