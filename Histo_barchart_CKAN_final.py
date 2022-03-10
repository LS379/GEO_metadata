import os
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import shutil
import pandas as pd

df = pd.read_csv('GSMs_particular.csv')
#make a list with all GSEs that will be use for iterating through it and selecting each GSE
list_genes = df['GSE']
# list_genes = ['GSE31263']
# list_genes = ['GSE16717', 'GSE14202', 'GSE40936','GSE20236', 'GSE16717', 'GSE40936', 'GSE46895', 'GSE53890',
#               'GSE58045', 'GSE57110', 'GSE65767', 'GSE84495', 'GSE92486', 'GSE93642'  ]
# list_genes = ['GSE20236']

# list_genes = ['GSE16717']
# list_genes = ['GSE40936']
# list_genes = ['GSE46895']
# list_genes = ['GSE53890']#
# list_genes = ['GSE58045']
# list_genes = ['GSE57110']
# list_genes = ['GSE65767']
# list_genes = ['GSE84495']
# list_genes = ['GSE92486']
# list_genes = ['GSE93642']
# list_genes = ['GSE31263']
### Call function 1 for a chosen GSE and obtain a list of characteristics for this GSE
#global variable used to give folder name that will hold histograms
gse_name = ''

def select_chrs_gse (gse):
    #select rows from Characteristic column that correspond with given GSE
    rows_chrs = df.loc[df["GSE"] == gse, "Characteristics"]
    # print(rows_chrs)
    #make a directory for each GSE and name it with GSE's id
    directory = gse
    patern_dir = "/home/Desktop/GSE_caz_particular/"
    path = os.path.join(patern_dir, directory)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    return rows_chrs


# m = select_chrs_gse("GSE108978")
# print(m)

###Call function 2 to process the list of characteristic for a specific GSE
#This function will process the list until all characteristic within that will have the same format: ["Age: 4 years", "Tissue: blood"]

def split_by_many_ch (rows_chrs):
    final_list = []

    for char in rows_chrs:
        # print(char)
        if type(char) == str:
            split1 = char.replace("\t","").replace("/","-").split(";")
            # split1 = char.split(";\t")
            # print(split1)
            for i in split1:
                # print(i)
                if i.count(":") == 1:
                    final_list.append(i)
                    # print(final_list)
                elif i.count(":") >= 2:
                    # print(final_list)
                    split2 = i.split(',')
                    # print(split2)
                    for j in split2:
                        if j.count(":")==1:
                            final_list.append(j)
                        elif j.count(":")>=2:
                            split3 = j.replace("Diet",",Diet").replace("Age",",Age").replace("tissue",",tissue").replace("Gender",",Gender").replace(";", ",").replace(", ,",",").replace(" ,", ",").split(',')
                            for empty_string in split3:
                                if (empty_string != ""):
                                    final_list.append(empty_string)
                            # final_list += (split3)
                        else:
                            final_list.append(j)

                        # print(final_list)
                else:
                    final_list.append(i)



    return final_list

# n = split_by_many_ch(select_chrs_gse("GSE108978"))
# print(n)



# Function4: make a dictionary {key: [list of values]}
##Transform the strings within the list of characteristic into a dictionary, based on colon symbol that divide annotation in category and characteristics
def sort_chars(final_list):
    chrs_for_hist = {}
    # print(final_list)
    for str_list in final_list:
        # print(str_list)
        chrs_gse_split = str_list.split(":")
        # print(chrs_gse_split)
        key_without_space = chrs_gse_split[0].strip()
        if key_without_space in chrs_for_hist:
            # print()
            chrs_for_hist[key_without_space].append(chrs_gse_split[1])

        else:
            chrs_for_hist[key_without_space] = [chrs_gse_split[1]]

    # print(chrs_for_hist)
    return chrs_for_hist


# Function3: check if each string contain just a single colon ":"

def gse_is_ok (final_list):
    # print(final_list)
    gse_is = 0
    for one_colon in final_list:
        # print(final_list)
        if one_colon.count(":") == 1:
            # print(gse_nr)
            gse_is += 1


    if gse_is == len(final_list):
        return True
    else:
        return False

# v = gse_is_ok(split_by_many_ch(select_chrs_gse("GSE108978")))
# print(v)

###Function5: histograms:


def plot_histogram (key, value):

    plt.hist(value, color = '#80bfff')
    plt.title(key)
    plt.xlabel('')
    plt.ylabel('')
    # plt.xticks(rotation=65, ha = 'right', fontsize=7)
    plt.savefig("/home/yoda/Desktop/GSE_caz_particular/"+ gse_name + '/' + key + '.png', format = 'png')

    # plt.show()
    plt.clf()
    plt.close()

def plot_bar(key, value):
    from cycler import cycler
    # colors = mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    categories = list(set(value))
    colors = ['#80bfff', '#80ff80', '#ff8566', '#99e6e6', '#df9fdf', '#ffbf80', '#bfbfbf',
              '#80ffaa', '#ff80ff', '#ffff66', '#e60073', '#8585ad', '#cc4400', '#00994d',
              '#cc6600', '#ffb3b3', '#008000', '#e6e600', '#86b300', '#004d4d', '#ff6600',
              '#e62e00', '#008040', '#ff7733', '#0073e6', '#cce6ff', '#fffe1a', '#800000',
              '#5500ff', '#ff6600', '#2eb82e', '#009999', '#660099', '#ff0055', '#c2c2f0',
              '#ff7733', '#A52A2A', '#003366', '#B8860B', '#008B8B', '#6495ED', '#004d00',
              '#ffbf00', '#0077b3', '#52527a', '#bf4080', '#ffbf80', '#39ac73', '#ff0080',
              '#66ff33', '#ffd633', '#DC143C', '#8B008B', '#8FBC8F',
              '#E9967A', '#00BFFF']
    values = []
    for x in categories:
        values.append(value.count(x))

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.4, wspace=0.1)
    ax.set_title(key)

    ax.bar(categories, values, color=colors, width=0.25)
    ax.set_xlim(-1,len(categories))

    if len(values) > 1 and len(values) <= 5:
        handles = [plt.Rectangle((0, 0), 1, len(values), color=color) for color in colors]
        ax.legend(handles=handles, labels=categories, loc='upper center', bbox_to_anchor=(0.4, -0.05),
                  prop={"size": 6.5}, fancybox=False, shadow=False, ncol=1)
    elif len(values) > 10 and len(values) <= 13:
        handles = [plt.Rectangle((0, 0), 1, len(values), color=color) for color in colors]
        ax.legend(handles=handles, labels=categories, loc='upper center', bbox_to_anchor=(0.4, -0.05), prop={"size": 6},
                  fancybox=False, shadow=False, ncol=1)
    elif len(values) > 13 and len(values) <= 30:
        handles = [plt.Rectangle((0, 0), 1, len(values), color=color) for color in colors]
        ax.legend(handles=handles, labels=categories, loc='upper center', bbox_to_anchor=(0.5, -0.2), prop={"size": 6},
                  fancybox=False, shadow=False, ncol=5)
    elif len(values) > 30:
        handles = [plt.Rectangle((0, 0), 0.5, len(values), color=color) for color in colors]
        ax.legend(handles=handles, labels=categories, loc='upper center', bbox_to_anchor=(0.5, -0.05), prop={"size": 5},
                  fancybox=False, shadow=False, ncol=5)
    else:
        handles = [plt.Rectangle((0, 0), 1, len(values), color=color) for color in colors]
        ax.legend(handles=handles, labels=categories, loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=False,
                  shadow=False, ncol=2)
    plt.xticks([])
    # plt.show()
    plt.savefig("/home/yoda/Desktop/GSE_caz_particular/"+ gse_name + '/' + key + '.png', format = 'png')
    plt.clf()
    plt.close()

# Function7: check if the values are numeric, if not try to convert them.
### Call function 5 if values are numeric and fc 6 if aren't
def sort_for_hist_or_bar (chrs_for_hist):
    # print(chrs_for_hist.items())

    for key, value in chrs_for_hist.items():
        if sum([not s.replace(' ','').isnumeric() for s in value])==0:
            hist_val=[int(s.replace(' ','')) for s in value]
            plot_histogram(key, hist_val)
        elif sum([not s.replace(' ','').replace('.','',1).isnumeric() for s in value])==0:
            hist_val=[float(s.replace(' ','')) for s in value]
            plot_histogram(key, hist_val)
        # elif 'age' in key.lower():
        elif re.findall(r'\bage\b', key.lower()) or re.findall(r'\sage\b', key.lower()):
            hist_val =[]
            for each_value in value:
                # print(hist_val)
                print(value)
                # print(value)
                # ages = re.findall("\s\d+\s", each_value)
                # ages = re.findall("\s\d+\.\d+", each_value) #functioneaza pentru 20236
                ages = re.findall("\s\d+\.\d+\s", each_value)
                ages+= re.findall("\s\d+\s", each_value)

                # print(ages)
                if len(ages) == 1:
                    # hist_val.append(int(", ".join(ages)))
                    hist_val.append(float(", ".join(ages)))
                else:
                    hist_val.append(each_value)

            plot_histogram(key, hist_val)
        else:
            plot_bar(key, value)



###The main program
##Iterate through a list of GSEs, and for each of them call those 7 functions written above
for gse in set(list_genes):
    gse_name = gse
    m = select_chrs_gse(gse)
    print(gse)
    n = split_by_many_ch(m)
    print(n)
    # print(gse_is_ok(n))
    if gse_is_ok(n) is True:
        sort_chars(n)
        sort_for_hist_or_bar(sort_chars(n))
        # print(sort_chars(n))
    else:
        print("GSE is not ok")






