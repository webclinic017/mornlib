# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 12:51:58 2018

@author: Dennis.Liang
"""
##########GLOBALS##############################################################

requesttimeout = 10
defaultrawdir = "RawFiles"

##########SUB##################################################################

def url_keyratio (symbol, market=""):
	
	#key ratios : precalculated financial ratios
	
	#http://financials.morningstar.com/ajax/exportKR2CSV.html?t=<market>:<stock>
	
	if market:
		symbol = market+":"+symbol
	
	syntax = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="+symbol
	return syntax

def url_financials (symbol, reporttype, period, order="asc", datatype="A", denomview = "raw", columnyear="5", unit="1", market=""):
	
	#raw earnings data
	
	#reportType: is = Income Statement, cf = Cash Flow, bs = Balance Sheet
	#period: 12 for annual reporting, 3 for quarterly reporting
	#dataType: this doesn't seem to change and is always A
	#order: asc or desc (ascending or descending)
	#columnYear: 5 or 10 are the only two values supported
	#number: The units of the response data. 1 = None 2 = Thousands 3 = Millions 4 = Billions
	
	#http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=<market>:<stock>&reportType=<is|cf|bs>&period=<12|3>&dataType=<A|R>&order=<asc|desc>&denominatorView=<raw|percentage|decimal>&columnYear=5&number=3
	
	if market:
		symbol = market+":"+symbol
	
	#syntax = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+symbol+"&reportType="+reporttype+"&period="+period+"&dataType="+datatype+"&order="+order+"&columnYear="+columnyear+"&number="+unit
	syntax = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="+symbol+"&reportType="+reporttype+"&period="+period+"&dataType="+datatype+"&order="+order+"&denominatorView="+denomview+"&columnYear="+columnyear+"&number="+unit
	return syntax

def download_file(url,fileloc,to=requesttimeout,redirect=True):
	try:
		r = requests.get(url, allow_redirects=redirect, timeout=to)
		with open(fileloc, 'wb') as f:
			f.write(r.content)
		del r
		return 1
	except:
		return 0

############## DUMPER #########################################################
	

def dumptofile (symlist, datatype, savelocation=defaultrawdir, overwrite=0):
	
	t1=time.gmtime()
	tt1=time.time()
	
	begintime = time.strftime('%a, %d %b %Y %H:%M:%S GMT',t1)
	
	datatype = datatype.capitalize()
	
	print("Begin Morningstar Fundamentals "+datatype+" DB Dump at "+begintime)
	
	fileloc = savelocation+"\\"+datatype+"\\"
	
	logd = open(fileloc+".downloadlog.txt","a+")
	loge = open(fileloc+".errorlog.txt","a+")

	logd.write("\n##############################################################################################################\n")
	loge.write("\n##############################################################################################################\n")
	
	logd.write(begintime+ "\nBegin Logging:\n")
	loge.write(begintime+ "\nBegin Logging:\n")
	
	if datatype == "Financials":
		reporttype = ["is","cf","bs"]
		periods = ["12","3"]
	else:
		reporttype = "1"
		periods = "1"   
	
	
	for sym in symlist:
		for rettype in reporttype:
			for period in periods:

				filename = datatype+'.'+sym
				filename = filename.replace('*','9')
				filename = filename.replace('#','9')
											
				if datatype == "Financials":
					url = url_financials(sym,rettype,period)
					if period == "12":
						ext = "ANNUAL"
					elif period == "3":
						ext = "QUARTERLY"						
					filename = filename+'.'+rettype+'.'+ext
					filename = filename+".csv"
					file = fileloc+rettype+"\\"+ext+"\\"+filename
				elif datatype == "Keyratio":
					url = url_keyratio(sym)
					filename = filename+".csv"
					file = fileloc+filename
					
				print("Fetching " + sym + " via " + url + " try saving to "+file)
				
				if (not overwrite):
					
					#testfile = open(fileloc+filename, "r", encoding="UTF-8")
					#test_json = json.loads(testfile.read())
					#testfile.close()
					
					try:
						testfile = open(file, "r", encoding="UTF-8")
						statinfo = os.stat(file)
						#test_json = json.loads(testfile.read())
						#testfile.close()
						#print(fileloc+filename+" Already exist skipping..")
						#continue
						if (statinfo.st_size > 0):
							print(file+" Already exist skipping..")
							continue
					except FileNotFoundError:
						print(file+" File not found downloading..")
					except ValueError:
						print(file+" Bad JSON found downloading..")
						#exit()
						
				if(download_file(url, file)):
					print("Fetch "+url+" sucessfully saved to "+file)				
					logd.write("Fetch "+url+" sucessfully saved to "+file+"\n")
				else:
					print("Fetch "+url+" failed to save to "+file)
					loge.write("Fetch "+url+" failed to save to "+file+"\n")
				
	t2 = time.gmtime()
	tt2 = time.time()
	
	endtime = time.strftime('%a, %d %b %Y %H:%M:%S GMT',t2)	 
	
	elapsedtime = str(tt2-tt1)
	
	logd.write(endtime+ "\nEnd Logging Time Elapsed: \n"+elapsedtime)
	loge.write(endtime+ "\nEnd Logging Time Elapsed: \n"+elapsedtime)
	
	
	logd.close()
	loge.close()
	
	print("End Morningstar Fundamentals "+datatype+" DB Dump at "+endtime+ " Took :"+elapsedtime+" seconds. \n")
	
	return 1;



def qw(s):
	return list(s.split())


###############################################################################


################################# MAIN ########################################

import csv
import requests
import pandas as pd
import time
import os
#import urllib2
#import csv
#import re
#import numpy as np
#import matplotlib.pyplot as plt
#import urllib
#import urllib.reqests
#import urllib.error


url = url_financials("ERI","is","12","asc")
response = requests.get(url)
#response = urllib.urlopen(url)
cr = csv.reader(response.text, delimiter=',', quotechar='\n')

localdir = "RawFilesTest"

download_file(url,localdir+"\\ERI_is.csv")

data = pd.read_csv(url)

print (cr)

for row in cr:
	print (row)
	
	

print ("begin morn dump \n")

sp1500list2 = qw("DDD MMM EGHT AIR ABM ACIW ADTN ACM AES AFL AGCO AKS AMAG AMCX AME AMN ANIP ANSS ARR ARRS ASGN T ATNI AZZ AAON AAN ABBV ABT ANF ABMD ACHC AKR ACN ACET ACOR ATVI ATU AYI ACXM ADNT ADBE ATGE ASIX AAP AEIS AMD AEGN AJRD AVAV AET AMG A AGYS ADC APD AKAM AKRX ALG ALRM ALK AIN ALB ALEX ARE ALXN ALGN Y ATI ALGT ALLE AGN ALE ADS LNT MDRX ALL GOOGL GOOG MO AMZN AMBC AMED AEE AAL AAT AXL ACC AEO AEP AEL AXP AFG AIG APEI AWR AMT AVD AWK AMWD AMP ABCB AMSF ABC AMGN AMPH APH APC ADI ANDV ANDE ANGO ANIK AXE ANTM AON APA AIV APY APOG ARI AAPL AIT AMAT AAOI ATR APTV WTR ARCB ADM AROC ARNC ANET AHH ARW ABG ASNA ASH AHL ASRT ASB AIZ ASTE AAWW ATO AN AZO ADSK ADP AVB AVNS AVY CAR AVA AVT AVP ACLS AAXN BOFI BGS OZK BBT BJRI BMI BHGE BCPC BLL BANC BXS BAC BOH BANR BNED BKS B BAX BDX BBBY BELFB BDC BEL BMS BHE BRK.B BHLB BBY BGFV BIG BIO TECH BEAT BIIB BKH BLK BLKB HRB BCOR BA BCC BCEI BKNG BWA SAM BPFH BXP BSX EPAY BYD BRC BGG BHF EAT BMY BRS AVGO BR BRKL BRKS BRO BF.B BC BKE CJ CA CACI CBL CBRE CBS CDK CF CHRW CIEN CME CMS CNO CNX CEIX CROX CSGS CSX CTS CVBF CVS CABO CBT CCMP COG CDNS CALM CAMP CVGW CAL CWT ELY CPE CBM CPT CPB CMD COF CMO CRR CAH CATM CTRE CECO CSL KMX CCL CRS CRZO CARS CRI CASY CTLT CAT CATY CATO CVCO CBOE CDR CELG CNC CNP CENT CENTA CPF CENX CTL CERN CEVA CRL GTLS CHTR CLDT CAKE CHE CHFC CHK CHSP CVX CHS PLCE CMG CB CHD CHDN CHUY CI XEC CBB CINF CNK CTAS CIR CRUS CSCO C CFG CTXS CHCO CLH CLW CLX CLD COKE KO CCOI CGNX CTSH COHR COHU CL COLB CMCSA CMA FIX CBSH CMC CBU CYH CHCT CVLT CMP CPSI CMTL CAG CXO CNMD COP CNSL ED STZ CTRL CVG COO CTB CPS CPRT CORT CLB CORE CXW CLGX COR GLW OFC CRVL COST COTY CUZ CBRL CR CRAY CREE CCRN CCI CRY CUB CFR CMI CW CUBI CUTR CY CONE CYTK DISH DSPG DSW DTE DXC DXPE DVA DAKT DAN DHR DRI DAR PLAY DF DECK DE DLPH DAL DLX DNR XRAY DVN DO DRH DKS DBD DGII DLR DDS DCOM DIN DIOD DPLO DFS DISCA DISCK DG DLTR D DPZ UFS DCI DFIN RRD DORM DEI DOV DWDP DRQ DUK DRE DNB DNKN DY ETFC EOG EPR EQT ESE EVTC SSP EZPW EXP EGRX EWBC EGP DEA EMN ETN EV EBIX ECHO ECL EPC EIX EW EE LOCO ERI ESIO EA EFII EME EBS EMR EIG NPO ENTA EHC ECPG WIRE ENDP EGN ENR ENS EGL ENVA ESV ETR EVHC PLUS EFX EQIX EQR ERA ESND ESS EL ESL ETH EVR RE EVRG ES EXEL EXC EXLS EXPE EXPD EXPO EXPR ESRX EXTN EXR EXTR XOM FFIV FARO FLIR FMC FNB FCN FN FB FDS FICO FAST FDX FRT FSS FII FIS LION FRGI FITB FNSR FAF FBP FCF FFBC FFIN FHN FR FMBI FSLR FCFS FE FISV FIVE FLT FTK FLO FLS FLR FL F FORM FORR FTNT FTV FBHS FWRD FOSL FCPT FOXF FRAN FELE FSB BEN FSP FCX FTR FUL FULT FF GIII GATX AJG GME GCI GPS GRMN IT GD GE GIS GM GCO GWR GNTX THRM GPC GNW GEO GEOS GTY ROCK GILD GBCI GLT GNL GPN GMED GS GT GOV GGG GHC GWW GVA GPMT GWB GNBC GDOT GPRE GBX GHL GEF GFF GPI GES GIFI GPOR HCA HCI HCP HF HMSY HNI HPQ HAE HAIN HAL HWC HBI HAFC THG HOG HLIT HRS HSC HIG HAS HVT HE HA HWKN HAYN HQY HSTM HR HCSG HTLD HSII HELE HLX HP JKHY HFWA HT HSY HSKA HES HPE HIBB HPR HIW HRC HI HLT HFC HOLX HOMB HD HMST HON HOPE HMN HRL DHI HPT HST HUBG HUBB HUM JBHT HBAN HII ICUI IDA IEX IDXX INFO IIVI INTL IPGP IQV IRDM ITT ICHR ITW ILMN INCY IRT INDB IR NGVT INGR IPHS IOSP INVA INGN NSIT NSP IBP IIIN ITGR IART IDTI INTC IPAR IDCC IBKR ICE TILE IPG IBOC IBM IFF IP ISCA INTU ISRG IVC IVZ IVR ITG IRM ITRI JJSF JCOM JBGS JPM JBL JACK JEC JRVR JHG JEF JBLU JBT JW.A JNJ JCI JLL JNPR KBH KBR KLAC KLXE KALU KAMN KSU KS K KELYA KEM KMPR KMT KEY KEYS KRC KMB KIM KMI KEX KIRK KRG KNX KN KSS KOPN KOP KFY KRA KR KLIC LB LLL LCII LGIH LHCG LKQ LXU LKSD LTC LZB LHO LH LRCX LAMR LW LANC LSTR LCI LNTH LPI LMAT LTXB LM LEG LDOS TREE LEN LII LXP LPT LSI LPNT LGND LLY LECO LNC LNN LQDT LAD LFUS LIVN LYV LPSN LMT L LOGM LPX LOW LL LITE LMNX LDL LYB MTB MHO MHLD MMS MBFI MDC MDU MGM MKSI MGPI MSA MSM MSCI MTSC MYRG MAC CLI M MGLN MNK MANH MAN MANT MRO MPC MCS HZO MKTX MAR VAC MMC MRTN MLM MAS MASI MA MTDR MTRN MTRX MATX MAT MATW MXL MKC MDR MCD MCK MPW MDSO MED MD MDT MRK MCY MRCY MDP VIVO MMSI MTH CASH MEI MET MTD MDXG KORS MSTR MCHP MU MSFT MAA MLHR MTX MINI MHK MOH TAP MNTA MCRI MDLZ MPWR TYPE MNRO MNST MCO MOG.A MS MOS MPAA MSI MOV MLI LABL MUR MUSA MYE MYL MYGN NBTB NCR EGOV NKE NMIH NFBK DNOW NRG NUS NVR NBR NANO NDAQ NBHC NFG NATI NOV NPK NNN NSA BABY NLS NAVI NCI NAVG NP NKTR NEOG NTAP NFLX NTGR NTCT NJR NEWM NYCB NYMT NYT NEU NWL NFX NEM NR NWSA NWS NEE NXGN NLSN NI NE NBL NDSN JWN NSC NTRS NOC NWBI NWN NWE NCLH NUVA NUE NTRI NVDA ORLY OFG OGE OGS OKE OPB OSIS OAS OXY OII OCLR ODP OIS ODFL ONB ORI OLN OLLI ZEUS OHI OMCL OMC OSPN OSUR ORCL ORN ORIT OFIX OSK OMI OI OXM PCAR PBF PDCE PDFS PCG PGTI PNC PNM PPG PPL PRAA PSB PTC PVH PACW PPBI PKG PZZA PARR PKE PH PATK PDCO PTEN PYPL PAYX PENN PVAC JCP PEI PMT PNR PBCT PEP PRFT PKI PRGO PERY PRSP PETS PFE PAHC PM PSX PLAB PNFP PNW PES PXD PJC PBI PLT PLXS PII POL POOL POST PCH POWL POWI PRAH PX PFBC PBH PRI PFG PRA PLD PUMP PG PGNX PRGS PGR PB PRLB PRSC PFS PRU PEG PSA PHM QEP QCOM QRVO KWR QLYS NX PWR DGX QNST QHC RMAX RGNX REX RH RLI RPM RL RMBS RPT RRC RAVN RJF RYAM RYN RTN RLGY O RHT RRGB RWT RBC REG REGN RF RGS RGA RS RNR REGI RCII RGEN RSG RMD RECN ROIC REI RHI ROK COL ROG ROL ROP ROST RDC RCL RGLD RTEC RUTH R STBA SPGI SBAC SCG CKH SEIC SLG SLM SM SPSC SPXC FLOW SRCI STE SIVB SBRA SABR SAFT SAIA CRM SBH SAFM JBSS SANM BFS SCSC HSIC SLB SCHL SCHW SWM SAIC SGMS SMG SBCF STX SEE SEM SIGI SRE SMTC SENEA SNH SXT SCI SFBS SHAK SHW SCVL SFLY SSTK SBNY SIG SLGN SLAB SFNC SPG SSD SIX SKX SKYW SWKS SNBR AOS SJM SNA SEDG SAH SONC SON BID SJI SO SBSI LUV SWX SWN SPTN SPPI SR SPOK SFM STMP SMP SXI SWK SBUX STT STLD SCL SRCL STL SHOO STC SF STRA SYK RGR INN SXC STI SPN SUP SUPN SVU SRDX SYKE SYMC SYNA SYF SYNH SNX SNPS SNV SYY TROW TCF TEL TGNA ENSG TJX TPH TTEC TTMI TRHC TCMD TLRD TTWO SKT TPR TGT TCO TISI TECD FTI TDY TFX TDS TPX THC TNC TDC TER TEX TTEK TTI TCBI TXN TXRH TXT BK BCO CC KHC MDCO MIK TTS WEN WMB TMO TPRE THO TIVO TIF TKR TMST TWI TVTY TOL TMP TR BLD TMK TTC TSS TSCO TDG RIG TRV TVPT TG THS TREX TRMB TRN TRIP TBK TGI TBI TRST TRMK TUP FOXA FOX TWTR TYL TSN UDR UGI UMBF USB USCR ECOL USPH SLCA ULTA ULTI UCTT UMPQ UAA UA UFI UNF UNP UIS UNT UBSI UCBI UAL UFCS UIHC UNFI UPS URI X UTX UTHR UNH UNIT UVV UEIC UFPI UHT UHS UVE UNM UE URBN UBA VFC VRTU VLO VLY VMI VVV VREX VAR VVC VECO VTR VRA VRSN VRSK VRTV VZ VSM VRTX VSAT VIAB VVI VIAV VICR VRTS V VSH VSTO VC VSI VG VNO VMC WDFC WEC WEX WPX WRB WNC WAB WDR WAGE WBA WD WMT DIS WAFD WPG WM WAT WSO WTS WBS WTW WRI WCG WFC WELL WERN WST WRK WABC WDC WU WY WHR WSR WLH WSM WLTW WING WGO WTFC WETF WWW WWD WRLD INT WWE WOR WYND WH WYNN XOXO XEL XRX XLNX XPER XYL YUM ZBRA ZBH ZION ZTS ZUMZ EBAY EHTH IRBT STAR NVT")

symlist = sp1500list2

#dumptofile (symlist,"Keyratio")
#dumptofile (symlist,"Financials")

import sys
sys.path.append('..\\..\\iexlib\\scripts')

from iexdownloadlib import getsymlist

symlist = getsymlist()

print (symlist)

dumptofile (symlist,"Keyratio")
dumptofile (symlist,"Financials")
