#! /usr/bin/env python

import csv, re
import os, shutil, argparse

def checkm_analysis(file_,fasta):
    checkm = list(csv.reader(open(file_,'rb')))
    new = []
    for list_ in checkm:
        for string in list_:
            x = re.sub(' +',' ',str(re.split(r'\t+', string.rstrip('\t'))))
            new.append(x)
    
    del new[0], new[1], new[(len(new)-1)]
    new_2 = []
    for list_ in new:
        x = list_.strip("['']")
        x_2 = x.split()
        new_2.append(x_2)
    del new_2[0]
    High_completion = []
    Low_completion = []
    High_contamination = []
    Strain_variation = []
    for list_ in new_2:
        if float(list_[12]) > 80 and (float(list_[13])<=10):
            High_completion.append(list_[0])
        elif float(list_[12]) > 50 and (float(list_[13])<=5):
            High_completion.append(list_[0])
        elif float(list_[12]) < 50 and float(list_[13])<=5:
            Low_completion.append(list_[0])
        elif float(list_[13])>50 and float(list_[14])>90:
            Strain_variation.append(list_[0])
        else:
            High_contamination.append(list_[0])


    os.makedirs("high_completion")
    os.makedirs("low_completion")
    os.makedirs("high_redundancy")
    os.makedirs("strain_redundancy")
    
    for name in High_completion:
        shutil.move((str(name)+fasta), "high_completion")
    for name in Low_completion:
        shutil.move((str(name)+fasta),"low_completion")
    for name in High_contamination:
        shutil.move((str(name)+fasta),"high_redundancy")
    for name in Strain_variation:
        shutil.move((str(name)+fasta),"strain_redundancy")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='checkm_analysis', usage='%(prog)s -checkM checkm_qa -f fasta suffix [.fa,.fasta,.fna]',description="""Script pulls CheckM qa results and separates files into low completion, high completion, and high redundancy""")
    parser.add_argument("-checkM", dest="inputqa", help="Specify a checkM file")
    parser.add_argument("-f", dest="inputfa", type=str, default=".fna",help="Identify what your suffix for fasta file is [default: .fna]")
    args = parser.parse_args()
    
    if args.inputqa is None:
        print parser.print_help()
    else:
        checkm_analysis(args.inputqa,args.inputfa)
        

        
