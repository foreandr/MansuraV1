import os
from openpyxl.styles import Side, Border
from openpyxl import Workbook

from datetime import datetime
import pytz

dict_for_test = {
    '1' : {'VALUE': {'VOTES': 6, 'PERCENT': '%0.06451613', 'AMOUNT': '19.89'}, 'ORDER': ['foreandr', 'foreandr', 'cheatsie', 'foreandr1', 'foreandr2', 'foreandr3', 'foreandr33']},
    '4' : {'VALUE': {'VOTES': 3, 'PERCENT': '%0.03225806', 'AMOUNT': '9.45'}, 'ORDER': ['foreandr', 'andrfore', 'foreandr68', 'foreandr99'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.50'}},
    '2' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.32'}, 'ORDER': ['foreandr', 'foreandr4']},
    '5' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr', 'foreandr5', 'foreandr9'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.33'}},
    '6' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr', 'foreandr6'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '3' : {'VALUE': {'VOTES': 4, 'PERCENT': '%0.04301075', 'AMOUNT': '13.26'}, 'ORDER': ['foreandr', 'foreandr7', 'foreandr10', 'foreandr58', 'foreandr80']},
    '8' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr', 'foreandr8'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '53' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr34', 'foreandr20'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.17'}},
    '50' : {'VALUE': {'VOTES': 4, 'PERCENT': '%0.04301075', 'AMOUNT': '12.60'}, 'ORDER': ['foreandr31', 'foreandr21', 'foreandr27', 'foreandr72', 'foreandr90'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.66'}},
    '86' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr67', 'foreandr22'], 'REPLY': {'REPLYING_TO': 'foreandr38', 'AMOUNT': '0.17'}},
    '32' : {'VALUE': {'VOTES': 4, 'PERCENT': '%0.04301075', 'AMOUNT': '12.60'}, 'ORDER': ['foreandr3', 'foreandr23', 'foreandr63', 'foreandr76', 'foreandr93'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.66'}},
    '58' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr39', 'foreandr24', 'foreandr35'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.33'}},
    '48' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr29', 'foreandr25', 'foreandr29'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.33'}},
    '87' : {'VALUE': {'VOTES': 4, 'PERCENT': '%0.04301075', 'AMOUNT': '12.60'}, 'ORDER': ['foreandr68', 'foreandr26', 'foreandr36', 'foreandr62', 'foreandr73'], 'REPLY': {'REPLYING_TO': 'foreandr39', 'AMOUNT': '0.66'}},
    '43' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr24', 'foreandr28'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '47' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr28', 'foreandr30'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.17'}},
    '75' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr56', 'foreandr31'], 'REPLY': {'REPLYING_TO': 'foreandr27', 'AMOUNT': '0.17'}},
    '20' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr2', 'foreandr32'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '63' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr44', 'foreandr34', 'foreandr86'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.33'}},
    '25' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr3', 'foreandr37', 'foreandr57'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.33'}},
    '22' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr2', 'foreandr38'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '34' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr3', 'foreandr39', 'foreandr53'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.33'}},
    '67' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr48', 'foreandr40'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '12' : {'VALUE': {'VOTES': 3, 'PERCENT': '%0.03225806', 'AMOUNT': '9.45'}, 'ORDER': ['foreandr', 'foreandr41', 'foreandr66', 'foreandr94'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.50'}},
    '88' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr69', 'foreandr42'], 'REPLY': {'REPLYING_TO': 'foreandr40', 'AMOUNT': '0.17'}},
    '90' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr71', 'foreandr43'], 'REPLY': {'REPLYING_TO': 'foreandr42', 'AMOUNT': '0.17'}},
    '26' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr3', 'foreandr44'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '28' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr3', 'foreandr45'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '71' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr52', 'foreandr46'], 'REPLY': {'REPLYING_TO': 'foreandr23', 'AMOUNT': '0.17'}},
    '80' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr61', 'foreandr47'], 'REPLY': {'REPLYING_TO': 'foreandr32', 'AMOUNT': '0.17'}},
    '89' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr70', 'foreandr48'], 'REPLY': {'REPLYING_TO': 'foreandr41', 'AMOUNT': '0.17'}},
    '39' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr20', 'foreandr49', 'foreandr54'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.33'}},
    '51' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr32', 'foreandr50'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.17'}},
    '77' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr58', 'foreandr51'], 'REPLY': {'REPLYING_TO': 'foreandr29', 'AMOUNT': '0.17'}},
    '59' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr40', 'foreandr52'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '24' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr2', 'foreandr55'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '98' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr79', 'foreandr56'], 'REPLY': {'REPLYING_TO': 'foreandr50', 'AMOUNT': '0.17'}},
    '14' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr', 'foreandr59', 'foreandr83'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.33'}},
    '16' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr', 'foreandr60'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '70' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr51', 'foreandr61', 'foreandr77'], 'REPLY': {'REPLYING_TO': 'foreandr22', 'AMOUNT': '0.33'}},
    '30' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr3', 'foreandr64'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '37' : {'VALUE': {'VOTES': 3, 'PERCENT': '%0.03225806', 'AMOUNT': '9.45'}, 'ORDER': ['foreandr3', 'foreandr65', 'foreandr74', 'foreandr85'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.50'}},
    '66' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr47', 'foreandr67', 'foreandr70'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.33'}},
    '62' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr43', 'foreandr69'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '23' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr2', 'foreandr71'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '65' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr46', 'foreandr75'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '55' : {'VALUE': {'VOTES': 2, 'PERCENT': '%0.02150538', 'AMOUNT': '6.30'}, 'ORDER': ['foreandr36', 'foreandr78', 'foreandr82'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.33'}},
    '99' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr80', 'foreandr79'], 'REPLY': {'REPLYING_TO': 'foreandr51', 'AMOUNT': '0.17'}},
    '49' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr30', 'foreandr81'], 'REPLY': {'REPLYING_TO': 'foreandr2', 'AMOUNT': '0.17'}},
    '61' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr42', 'foreandr84'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '46' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr27', 'foreandr87'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '44' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr25', 'foreandr88'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '56' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr37', 'foreandr89'], 'REPLY': {'REPLYING_TO': 'foreandr3', 'AMOUNT': '0.17'}},
    '33' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr3', 'foreandr91'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '10' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr', 'foreandr92'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '92' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr73', 'foreandr95'], 'REPLY': {'REPLYING_TO': 'foreandr44', 'AMOUNT': '0.17'}},
    '93' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr74', 'foreandr96'], 'REPLY': {'REPLYING_TO': 'foreandr45', 'AMOUNT': '0.17'}},
    '45' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr26', 'foreandr97'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}},
    '29' : {'VALUE': {'VOTES': 1, 'PERCENT': '%0.01075269', 'AMOUNT': '3.15'}, 'ORDER': ['foreandr3', 'foreandr98'], 'REPLY': {'REPLYING_TO': 'foreandr', 'AMOUNT': '0.17'}}
}

def WRITE_HEADERS_TO_EXCEL(equity_dict, vote_type, equity_total, all_temp_dicts, testing=False):
    
    my_time = pytz.timezone('US/Eastern') 
    current_datetime = datetime.now(my_time).replace(microsecond=0).replace(tzinfo=None)
    current_date = current_datetime.strftime('%Y-%m-%d')
    #print(current_datetime)
    # print(current_date)


    wb = Workbook()
    ws = wb.active

    #print("WRITE_HEADERS_TO_EXCEL========")
    #print("TESTING        :", testing)
    #print("VOTE TYPE      :", vote_type)
    #print("EQUITY AMOUNTS :", equity_total)
    #print("EQUITY DICT    :", equity_dict)
    #print()

    #TODO SHOW EXPENSIES

    # TITLE
    ws.cell(row=1, column=1).value = "MANSURA"
    ws.cell(row=1, column=2).value = str(current_date)
    ws.cell(row=1, column=3).value = vote_type

    # EXPENSES
    ws.cell(row=3, column=1).value = "EXPENSES"

    ws.cell(row=4, column=1).value = "SERVER"
    ws.cell(row=4, column=2).value = "DATABASE"
    ws.cell(row=4, column=3).value = "DOMAIN"
    ws.cell(row=4, column=4).value = "INC TRANS FEES"

    ws.cell(row=5, column=1).value = "$-x"
    ws.cell(row=5, column=2).value = "$-x"
    ws.cell(row=5, column=3).value = "$-x"
    ws.cell(row=5, column=4).value = "$-x"


    # TOTAL AMOUNT FOR THIS PERIOD
    ws.cell(row=7, column=1).value = "SYSEM TOT"
    ws.cell(row=7, column=2).value = "EQUITY TOT"
    ws.cell(row=7, column=3).value = "POOL TOT"
    ws.cell(row=8, column=1).value = f"${equity_total * 5}"
    ws.cell(row=8, column=2).value = f"${equity_total}"
    ws.cell(row=8, column=3).value = f"${(equity_total * 5 ) - equity_total}"


    # EQUITY DISTRIBUTION
    ws.cell(row=10, column=1).value = "EQUITY"  
    i = 1
    for key, value in equity_dict.items():
        # print(key, value)
        single_string = f'{key} ${"{:.2f}".format(float(value / 100) * equity_total)}'
        
        # print(single_string)
        # print(i, ":", single_string)
        ws.cell(row=11, column=i).value = single_string

        i+=1

    #USERS DISTRIBUTION
    ws.cell(row=13, column=1).value = "USERS"
    ws.cell(row=13, column=1).value = "FILE_ID"
    ws.cell(row=13, column=2).value = "VOTES"
    ws.cell(row=13, column=3).value = "PERCENT"
    ws.cell(row=13, column=4).value = "AMOUNT"
    ws.cell(row=13, column=5).value = "REPLYING_TO"
    ws.cell(row=13, column=6).value = "RATIO"
    ws.cell(row=13, column=7).value = "UPLOADER"
    ws.cell(row=13, column=8).value = "IN ORDER"

    ITERATION = 0
    for key, value in all_temp_dicts.items():
        # print(f"{key}:{value}")
        
        local_index = 0 # ANNOYING AND I NEED TO FIND A BETTER WAY TO DO THIS
        for key_, value_ in value["ORDER"].items():
            full_string = f"{key_} {value_}"

            if local_index == 0:
                ws.cell(row=14+ITERATION, column=7).value = full_string
            else:
                ws.cell(row=14+ITERATION, column=7+local_index).value = full_string
            local_index += 1
        

        # print(value)
        votes = f'{value["VALUE"]["VALUE"]["VOTES"]}'
        percent = f'{value["VALUE"]["VALUE"]["PERCENT"]}'
        amount = f'{value["VALUE"]["VALUE"]["AMOUNT"]}'

        if "RATIO" in value["VALUE"]:
            # print(value["VALUE"]["RATIO"])
            rat_key = (list(value["VALUE"]["RATIO"].keys())[0])
            rat_amount = value["VALUE"]["RATIO"][f"{rat_key}"]
            ratio_dict = str(rat_key) + " " + str(rat_amount)
        else:
            ratio_dict = ""
        
        if "REPLY" in value["VALUE"]:
            reply_to = value["VALUE"]["REPLY"]["REPLYING_TO"]
        else:
            reply_to = ""

        # ws.cell(row=14+ITERATION, column=8).value = "IN ORDER"
        ws.cell(row=14+ITERATION, column=1).value = key
        ws.cell(row=14+ITERATION, column=2).value = votes
        ws.cell(row=14+ITERATION, column=3).value = percent
        ws.cell(row=14+ITERATION, column=4).value = amount
        ws.cell(row=14+ITERATION, column=5).value = reply_to
        ws.cell(row=14+ITERATION, column=6).value = ratio_dict

        ITERATION +=1


    # print(F"TESTING IS: {testing}")
    wb.save(F"/root/mansura/Python/HISTORY/{vote_type}/{current_date}.xlsx")      

       
    