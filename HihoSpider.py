import requests
import re
import os
import shutil 
def GetURL(url):
    r= requests.get(url)
    if   r.status_code==200 :
            r.encoding = "UTF-8"
            return r.text
    else :
            print("爬取失败：URL="+url+"\n"+"错误码：")
            print(r.status_code)
            return ""
def Decode_Code(code):
    code=code.replace(r"\r\n","\n")
    code=code.replace(r"\t","\t")
    code=code.replace(r"\/","/")
    code=code.replace(r"\\","\\")
    code=code.replace(r'\"','"')
    code=code.replace(r"\'","'")
    return code
def GetText(html):
    lang = re.search(r'<p class="solution-lang l">Lang:.*</p>',html).group(0)
    ans = re.search(r'Verdict:<strong class="(fn-color-red fn-color-green|fn-color-red)">.*</strong>',html).group(0)
    code = re.search(r'editor\.getSession\(\)\.setValue\((.*)\)',html).group(0)
    tscore = re.search(r'<div>Score:<strong>[0-9]+ / [0-9]+</strong></div>',html).group(0)
    lang=lang[32:len(lang)-4]
    ans=ans.replace(r'"fn-color-red"',r'"fn-color-red fn-color-green"')
    ans=ans[52:len(ans)-9]
    code=code[30:len(code)-2]
    tscore=re.findall(r'[0-9]+',tscore)
    score=tscore[0]
    maxscore=tscore[1]
    code=Decode_Code(code)
    t=lang,ans,code,score,maxscore
    return t
def GetAllLink(urlofrankpage):
    lis=re.findall(r'<a href=".*/solution/.*">',GetURL(urlofrankpage))
    lis2=[]
    for s in lis:
        lis2.append(r"http://hihocoder.com"+s[9:len(s)-2])
    return lis2
def write_to_file(codelist):
    outputdir=r"C:\Spider\hiho149\spider_"
    cnt=0
    if os.path.exists(os.path.dirname(outputdir)):
        shutil.rmtree(os.path.dirname(outputdir))
    os.makedirs(os.path.dirname(outputdir))
    for ll in codelist:
##        if cnt%10==0:
##            print("\nWriting:No."+str(cnt))
        if ll[0]!='G++' and ll[0]!='GCC':
            continue
        fpath=outputdir+str(cnt)+ll[0]+ll[1]+ll[3]+r"\firewall.cpp"
        if not os.path.exists(os.path.dirname(fpath)):
            os.makedirs(os.path.dirname(fpath))
        with open(fpath,"w") as f:
            f.write(ll[2])
        cnt=cnt+1
    

codeurllist=GetAllLink("http://hihocoder.com/contest/hiho149/rank")

##codeurllist=codeurllist+GetAllLink("http://hihocoder.com/contest/hiho38/rank?page=2")
##print(codelist)
##tt=GetText(GetURL("http://hihocoder.com/contest/hiho38/solution/261835"))
##print (tt[2])
print("\nAnalysed:"+str(len(codeurllist)))
codelist=[]
cnt=0
for url in codeurllist:
    if cnt%10==0:
        print("\nCaughting:No."+str(cnt))
    codelist.append(GetText(GetURL(url)))
    cnt=cnt+1
print("\nCode caught:"+str(len(codelist)))
write_to_file(codelist)
print("\nFile Written")
##print(GetURL(r"http://hihocoder.com/contest/hiho38/solution/263222"))
