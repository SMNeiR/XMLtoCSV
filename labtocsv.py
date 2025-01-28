import pathlib
import glob
import re

"""
類 XML 轉 CSV 檔

功能：
- 轉換 *.txt、*.xml 檔案格式
- 類 XML 標籤處理包含大標 hdata、小標 rdata
"""

# hdata 鍵-值對
hdata_keys_values = { 
    'h1':'', 'h2':'', 'h3':'', 'h4':'', 'h5':'',
    'h6':'', 'h7':'', 'h8':'', 'h9':'', 'h10':'',
    'h11':'', 'h12':'', 'h13':'', 'h14':'', 'h15':'',
    'h19':'', 'h20':'', 'h22':''
    }

# rdata 鍵-值對
rdata_keys_values = {
    'r1':'', 'r2':'', 'r3':'', 'r4':'', 'r5':'',
    'r6':'', 'r7':'', 'r8':'', 'r10':'', 'r12':''
    }


def get_files():
    """
    使用 glob 取得轉檔檔案

    返回：
        files (list): 檔案清單
    """
    print("取得轉檔... ", end='')
    txt_files = glob.glob('*.txt')      # 取得當前目錄所有 *.txt
    xml_files = glob.glob('*.xml')      # 取得當前目錄所有 *.xml
    files = txt_files + xml_files       # 當前目錄所有 *.txt、*.xml
    print(f"【{files}】 ... 【完成】")
    return files

def del_csv_file():
    """ 刪除 CSV 檔案 """
    print("刪除 CSV 檔案... ", end='')
    csv_file = pathlib.Path(f'{filename}_py.csv')       # 取得 .csv 檔案
    if csv_file.exists():       # 判斷 .csv 檔案是否存在
        csv_file.unlink()       # 刪除 .csv 檔案
        print(f"【{filename}.csv】... ", end='')
    else:
        print("【.csv 不存在】... ", end='')
    print("【完成】")

def add_csv_title():
    """ 加入 CSV 標題 """
    print("加入 CSV 標題... ", end='')
    csv_title = ''
    for hdata_key in hdata_keys_values.keys():
        csv_title += f"\"{hdata_key}\","        # 加入 hdata 標題
    for rdata_key in rdata_keys_values.keys():
        csv_title += f"\"{rdata_key}\","        # 加入 rdata 標題
    csv_line = csv_title.rstrip(',')
    write_csv(csv_line)
    print("【完成】")

def add_csv_record():
    """ 加入 CSV 一筆紀錄 """
    csv_record = ''
    for hdata_value in hdata_keys_values.values():
        csv_record += f"\"{hdata_value}\","     # 加入 hdata 單筆紀錄
    for rdata_value in rdata_keys_values.values():
        csv_record += f"\"{rdata_value}\","     # 加入 rdata 單筆紀錄
    csv_line = csv_record.rstrip(',')
    print(csv_line)
    write_csv(csv_line)

def write_csv(csv_line):
    """ 
    寫入 CSV 檔案

    參數：
        csv_line (string): 寫入 .csv 字串
    """
    with open(f'{filename}_py.csv', 'a') as f:      # 寫入 .csv 檔案 (a 附加模式)
        f.write(csv_line + "\n")

def get_rdata_flag(line):
    """
    判斷是否為 rdata 資料區間

    參數：
        line (string): rdata 內容

    返回：
        rdata_flag (bool): rdata 資料區間 flag
    """
    global rdata_flag
    if line == '<rdata>':
        rdata_flag = True
    elif line == '</rdata>':
        rdata_flag = False
    return rdata_flag

def get_tag_name(line):
    """
    使用 re 擷取標籤名稱

    參數：
        line (string): rdata 或 hdata 內容
    
    返回：
        string: 標籤名稱
    """
    tag_name_match = re.search(r'<(\w+)>', line)
    if tag_name_match:
        return tag_name_match.group(1)      # 取得標籤名稱

def get_tag_content(line):
    """
    使用 re 擷取標籤的內容

    參數：
        line (string): rdata 或 hdata 內容
    
    返回：
        string: 標籤的內容
    """
    tag_content_match = re.search(r'<\w+>(.*?)</\w+>', line)
    if tag_content_match:
        return tag_content_match.group(1)       # 取得標籤的內容


if __name__ == '__main__':
    """ 主程式入口 """
    files = get_files()     # 取得轉檔檔案
    for file in files:
        print(f"【{file}】轉檔... ")
        filename = pathlib.Path(file).stem      # 取得檔案名稱，filename.txt => filename

        del_csv_file()      # 刪除 CSV 檔案
        add_csv_title()     # 加入 CSV 標題

        print("寫入 CSV 紀錄... ", end='')
        rdata_flag = False      # rdata 資料區間 flag
        with open(file, 'r') as f:      # 讀取轉檔資料 (r 唯讀)
            for line in f :
                line = line.strip()
                if get_rdata_flag(line):        # 判斷是否為 rdata 資料區間
                    rdata_key = get_tag_name(line)
                    if rdata_key in rdata_keys_values:
                        rdata_keys_values[rdata_key] = get_tag_content(line)        # 儲存 rdata 鍵-值對
                else:
                    if line == '</rdata>':      # 判斷是否為 </hdata>
                        add_csv_record()        # 加入 CSV 一筆紀錄 (hdata + rdata)
                        rdata_keys_values = dict.fromkeys(rdata_keys_values, '')        # 清空 hdata 所有 values 值，為空字串
                        continue
                    elif line == '</hdata>':        # 判斷是否為 </hdata>
                        hdata_keys_values = dict.fromkeys(hdata_keys_values, '')        # 清空 hdata 所有 values 值，為空字串
                        continue
                    hdata_key = get_tag_name(line)
                    if hdata_key in hdata_keys_values:
                        hdata_keys_values[hdata_key] = get_tag_content(line)        # 儲存 hdata 鍵-值對
        print(f"【{file}】轉檔...【完成】")