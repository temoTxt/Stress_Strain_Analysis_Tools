#      SCALE Parsing Outputs



def main():
   '''
   yn=1 ;o=0; countbus=0; Nbus=-1; bulines=-2; countmats=0; isolimit=1E-8; lmd='sum'; hmd='sum'
   cc=[]
   '''

   NumberOfOutputs=157
  
   Numbers='File Name  Density  Keff  Sigma \n'

   for ofs in range(97,NumberOfOutputs+1):
     with open('punitrate'+str(ofs)+'.out') as temps:
        for line in temps:
            if ('Mixture = 1 with density') in line:
                nb=line.split()
                Density=nb[6]
            if ('best estimate system k-eff') in line:
                nb=line.split()
                keff=nb[5]
                sigma=nb[9]
        Numbers=Numbers+'punitrate'+str(ofs)+' '+str(Density)+' '+str(keff)+' '+str(sigma)+'\n'
   a1=open('output','w')
   a1.writelines(Numbers)

'''
            if ('HMT material') in line and bumats[-1]!='(#/barn-cm):':
                countmats+=1

########################## Read Input and Script Name ################

            if ('basecase input') in line:
                bs=line.split()
                Name=bs[-1]
  
            if ('script') in line:
                bs=line.split()
                script=bs[-1]

            if ('Isotopic Number Density') in line and bumats[-1]!='#/barn-cm):':
                bs=line.split()
                isolimit=float(bs[-1])

        NumOfCoolantComps=countmats
'''

########################## Count BU Steps ################
'''
   with open('basecase/'+Name) as infp1:
     for line in infp1:
       if 'bustep' in line or 'butot' in line or 'daystep' in line or 'daytot' in line or 'decstep' in line or 'dectot' in line:
           countbus=1
       if countbus==1:
          word1b=line[0]
          bulines+=1
          if line[0].isalpha() and Nbus>0:
            countbus=0
            break
          if word1b[0]!='%' and word1b[0]!='\n' and word1b[0]!=' ':
            Nbus+=1

########## Starting double loop: perturbations and BU Steps #######

   for bustep in range(0,Nbus+1):
     turnHM=0; turnHMD=0; turnLM=0; turnLMD=0; turnFU=0; turnFD=0; codef=''
   
     for nbs in range(1,NumOfBranches+1):
       turn=0; e=0; cmodtempL=0; cmodtempH=0
       cc=[];
       coolcard=''
       with open('input') as temps:
         for line in temps:
            coolcard=''
    
###################### Increasing Moderator Temp ###################

            if ('High Mod') in line and turn==0:
                hmt=line.split()
                if hmt[-1]!='(K):' and turnHM==0:
                   mtup=hmt[-1]
                   turnHM=1;
                   for f in range(0,len(mtup)):
                      if len(mtup)==3:
                         code='0'+mtup[0]
                      else:
                         code=mtup[0]+mtup[1]
  
####################### HMT Density #################

            if ('HMT Total') in line and turnHM==1 and turn==0:
                dl=line.split()
                if dl[-1]!='(default=sum):':
                  hmd=dl[-1]

            if ('HMT mat') in line and turnHM==1 and turn==0:
                dl=line.split()
                if dl[-2]=='nat' or dl[-2]=='Nat':
                    if turnHM==1 and turnHMD<NumOfCoolantComps:                                       
                      e+=1
                      dl=line.split()
                      if len(dl[-3])==2:
                        coolcard='%s000.%sc %s \n' % (dl[-3],code,dl[-1])
                      if len(dl[-3])==1:  
                        coolcard='%s000.%sc %s \n' % (dl[-3],code,dl[-1])
                      turnHMD+=1
                      if turnHMD==NumOfCoolantComps:
                          turn=1
                          cmodtempH=1
                else:
                    if turnHM==1 and turnHMD<NumOfCoolantComps:
                      e+=1
                      dl=line.split()
                      if len(dl[-3])+len(dl[-2])==5:
                        coolcard='%s%s.%sc %s \n' % (dl[-3],dl[-2],code,dl[-1])
                      if len(dl[-3])+len(dl[-2])==4 or len(dl[-3])+len(dl[-2])==3:  
                        coolcard='%s0%s.%sc %s \n' % (dl[-3],dl[-2],code,dl[-1])
                      if len(dl[-3])+len(dl[-2])==2:
                        coolcard='%s00%s.%sc %s \n' % (dl[-3],dl[-2],code,dl[-1])
                      turnHMD+=1   
                      if turnHMD==NumOfCoolantComps:
                          turn=1     
                          cmodtempH=1
                cc.append(coolcard)

###################### Decreasing Moderator Temp ###################
   
            if ('Low Mod') in line and turn==0:
                lmt=line.split()
                if lmt[-1]!='(K):' and turnLM==0:
                  mtdown=lmt[-1]
                  turnLM=1;
                  for f in range(0,len(mtdown)):
                     if len(mtdown)==3:
                       code2='0'+mtdown[0]
                     else:
                       code2=mtdown[0]+mtdown[1]

################### LMT Density #######################

            if ('LMT Total') in line and turnLM==1 and turn==0:
                dl=line.split()
                if dl[-1]!='(default=sum):':
                   lmd=dl[-1]

            if ('LMT mat') in line and turnLM==1 and turn==0:
                dl=line.split()
                if dl[-2]=='nat' or dl[-2]=='Nat':
                  if turnLM==1 and turnLMD<NumOfCoolantComps:
                    e+=1
                    dl=line.split()
                    if len(dl[-3])==2:
                        coolcard='%s00.%sc %s \n' % (dl[-3],code2,dl[-1])
                    if len(dl[-3])==1:
                        coolcard='%s000.%sc %s \n' % (dl[-3],code2,dl[-1])
                    turnLMD+=1
                    if turnLMD==NumOfCoolantComps:
                          turn=1
                          cmodtempL=1                       
                else:
                  if turnLM==1 and turnLMD<NumOfCoolantComps:
                    e+=1
                    dl=line.split()
                    if len(dl[-3])+len(dl[-2])==5:
                        coolcard='%s%s.%sc %s \n' % (dl[-3],dl[-2],code2,dl[-1])
                    if len(dl[-3])+len(dl[-2])==4 or len(dl[-3])+len(dl[-2])==3:
                        coolcard='%s0%s.%sc %s \n' % (dl[-3],dl[-2],code2,dl[-1])
                    if len(dl[-3])+len(dl[-2])==2:
                        coolcard='%s00%s.%sc %s \n' % (dl[-3],dl[-2],code2,dl[-1])
                    turnLMD+=1
                    if turnLMD==NumOfCoolantComps:
                        cmodtempL=1
                        turn=1
                cc.append(coolcard)
        
########################## High and Low Fuel Temperatures

            if ('High Fuel') in line and turn==0:
                hft=line.split()
                if hft[-1]!='(K):' and turnFU==0:
                  ftup=hft[-1]
                  turnFU=1;
                  turn=1
                  for f in range(0,len(ftup)):
                     if len(ftup)==3:
                       code3='0'+ftup[0]
                     else:
                       code3=ftup[0]+ftup[1]                
 
            if ('Low Fuel') in line and turn==0:
                lft=line.split()
                if lft[-1]!='(K):' and turnFD==0:
                  ftdown=lft[-1]
                  turnFD=1;
                  turn=1
                  for f in range(0,len(ftdown)):
                     if len(ftdown)==3:
                       code4='0'+ftdown[0]
                     else:
                       code4=ftdown[0]+ftdown[1]
   
#################### Boron Concentration ###################
             
            if ('High Boron') in line:
                hbc=line.split() 
            if ('Low Boron') in line:
                lbc=line.split()

       NB=1; count = 0; count2 = 0

       with open('basecase/'+Name+'.bumat'+str(bustep)) as infp:
         for line in infp:
           if line:
             count += 1
       Nall=count
       count=0
       countwhile=0
       with open('basecase/'+Name) as infp1:
         for line in infp1:
            if line:
               count += 1
       Iall=count
       count=0 
     
############## Getting Rid of Zeros from burnt fuel ########################


       with open('basecase/'+Name+'.bumat'+str(bustep),'r' ) as b12:
        blist=[]; gh=0; v=0;
        for line in b12:
            bl=line.split()
            numws= len(bl)
            j=0;
            if gh==1 and float(bl[1])<isolimit:
                  bl[0]=bl[0].replace(bl[0],'')
                  bl[1]=bl[1].replace(bl[1],'')            
            for i in range(0,numws):
                if '6000.12s' in bl:
                    bl[0]=bl[0].replace(bl[0],'6000.12c')
                if 'mat' in bl:
                  gh=1
                else:
                  word1=bl[0]
                  fcount=0; codef=0
                  for f in range(0,len(word1)):
                      fcount+=1
                      if word1[f]=='.':
                        cf=[]
                        word1list=list(word1)
                        if turnFU==1 or turnFD==1:
                          if turnFU==1:
                             codef=code3
                          if turnFD==1:
                             codef=code4
                        else:
                             codef=word1[f+1:f+3]
                        word1list[fcount]=codef[0]
                        word1list[fcount+1]=codef[1]
                        cf= ''.join(word1list)
                        tl='%s %s'%(cf,bl[1])
                        bl1 = tl.split()
                        bl=[0]*(3)
                        for i in range(0,2):
                          bl[i]=('%s ') % bl1[i]
                        bl[-1]=('  \n')
            if j==0:
                v+=1
                blist.append(bl)
##### Counting lines until fuel comp, 2nd comp, power and depletion blocks ####
    
       count=0; c=0; count2ndmat=0; countpow=0; countdep=0; countcoolant=0
       with open('basecase/'+Name) as infp:
        for line in infp:
            if 'mat fuel' in line:
                c=1
                FLchars=len(line)
                TilMat1=count       
            count +=1
	    if(c==1 and TilMat1 < count - 1):  
                if 'mat' in line:
                    break
                count2ndmat +=1    
 
       with open('basecase/'+Name) as infp:
        for line in infp:
            if 'set pow' in line:
                break
            countpow+=1

       with open('basecase/'+Name) as infp:
        for line in infp:
            if 'bustep' in line or 'butot' in line or 'daystep' in line or 'daytot' in line or 'decstep' in line or 'dectot' in line:
                break     
            countdep+=1                
                   
############## Changing Moderator Tempe and Den in Input ##################

       q=1
       with open('basecase/'+Name) as infp:
        for line in infp:
            if q==1: 
                countcoolant+=1
                if 'mat coolant' in line: 
                  if cmodtempL==1:
                    temp=mtdown
                    modden=lmd
                  if cmodtempH==1:
                    temp=mtup
                    modden=hmd
                  sl=line.split()
                  numws= len(sl)
                  if cmodtempH==1 or cmodtempL==1:
                    for i in range(0,numws):
                      if 'coolant' in sl[i]:
                          sl[i+1]=sl[i+1].replace(sl[i+1],modden)
                      if 'tmp' in sl[i]: 
                          sl[i+1]=sl[i+1].replace(sl[i+1],str(temp))
                          q=0
                          break
                  else:
                          q=0
                          break

############## Determining ENDF-VII Cross section library ##################    
       
        libcount=0; modline=0
        with open('basecase/'+Name) as infp:
          for line in infp:
            modl=line.split()
            modwords=len(modl)
            libcount+=1
            for b in range(1,modwords):
              if modl[0]=='therm':
                if cmodtempH==1 or cmodtempL==1:
                  xsec=modl[-1]
                  thermname=modl[1]
                  modletters=len(xsec)
                  for b2 in range(1,modletters):
                    if xsec[0]=='g':
                      lib=3; modtype='gre7'
                    if xsec[0]=='h':
                      lib=2;  modtype='hwe7'
                    if xsec[0]=='l':
                      lib=1;  modtype='lwe7'
                  with open('libraries') as infp:
                    for line in infp:
                      modl=line.split()
                      if modl[lib]==temp:
                         modline='therm '+thermname+' '+modtype+'.'+modl[0]
                         modline=modline.split()
                else:
                  modline=line.split()
            if modline!=0:
              break

#################### Adding spaces to a line ###############

       sl1=[0]*(numws+1)
       for i in range(0,numws):
         sl1[i]=('%s ') % sl[i]
       sl1[-1]=('  \n')   
       
       modline1=[0]*(modwords+1)
       for i in range(0,modwords):
         modline1[i]=('%s ') % modline[i]
       modline1[-1]=('  \n')
         
       a1=open('basecase/'+Name,'r')
       listme=a1.readlines()       
       
       b=blist[1]   
       for i in range(0,v):  
         b=b+blist[i]
       countb=0
       for line in b:
         countb+=1

################# Generating Input ############

       x1=listme[1:libcount-1]                             ### input from start to mod lib
       x2=modline1	                                      ### moderator library
       x3=listme[libcount:TilMat1+1]                       ### input from mod lib to fuel mat
       x4=b[24:countb]                                     ### fuel num dens
       x5=listme[TilMat1-1+count2ndmat:countcoolant-1]     ### second material to mod mat
       x6=sl1                                              ### coolant material line
       x7=cc                                               ### coolant num dens
       x8=listme[countcoolant+int(e):countpow]             ### input from coolant mat to depletion
       x9=listme[countdep+int(bulines)+1:Iall]             ### input from depletion to end

       bunches=x1+x2+x3+x4+x5+x6+x7+x8+x9
    
############# Taking out the burn in fuel material line ################

       bunches[TilMat1-1]= bunches[TilMat1-1].replace("burn 1"," ")

############ Writing for each BU step and branch ##################
       namenew='pert'+str(nbs)+'bu'+str(bustep)+'.inp'
       newscript='pert'+str(nbs)+'bu'+str(bustep)+'.pbs'
       a2=open(namenew,'w')
       a2.writelines(bunches)
      
############ Writing PBS Scirpt #######

       with open(script,'r') as b13:
        bslist=[]; m=0; bsc1=[]
        for line in b13:     
            
          bsc=line.split()            
          numws= len(bsc)        
          if 'mpirun' in line:           
            for i in range(0,numws):
              bsc[-1]=bsc[-1].replace(bsc[-1],'pert'+str(nbs)+'bu'+str(bustep)+'.nohup')
              bsc[-3]=bsc[-3].replace(bsc[-3],namenew)

          if '-N' in line:
            for i in range(0,numws):
              bsc[-1]=bsc[-1].replace(bsc[-1],'pert'+str(nbs)+'bu'+str(bustep))
          bsc1=[0]*(numws+1)
          for i in range(0,numws):
              bsc1[i]=('%s ') % bsc[i]
          bsc1[-1]=('  \n')          
          bslist.append(''.join(bsc1))  

       a4=open(newscript,'w')
       a4.writelines(bslist)
'''
if __name__ == "__main__":
    main() 
'''    
####################### Running PBS scripts ####################

    countbus=0; Nbus=0;
    with open('input') as temps:
        for line in temps:
            if ('Number of Branches') in line:
                nb=line.split()
                nbs=int(nb[-1])

            if ('basecase input') in line:
                bs=line.split()
                Name=bs[-1]

    with open('basecase/'+Name) as infp1:
     for line in infp1:
       if 'bustep' in line or 'butot' in line or 'daystep' in line or 'daytot' in line or 'decstep' in line or 'dectot' in line:
           countbus=1
       if countbus==1:
          word1b=line[0]
          if line[0].isalpha() and Nbus>0:
            countbus=0
            break
          if word1b[0]!='%' and word1b[0]!='\n' and word1b[0]!=' ':
            Nbus+=1; 
    for i in range(0,Nbus):
        for j in range(1,nbs+1):
          script2='pert%sbu%s.pbs' %(j,i)
          import os
          if i==2:
            print script2
           # os.system('qsub %s' %script2)

#noh clears
'''
