#      SCALE Input Generator

def main():
# import os

# RunScale = '..\..\..\..\SerialRunAll.bat'
# HPuRun = 700
   


    for j in range (0,1):
     HPu = 700+j*100
     for i in range (0,2):
       M=[0.5, 6.0]
       Density = round((26539 - 638.7*M[i] )/ (HPu +9.606),2)
   
       input='=CSAS6 Parm=( ) 								\n'\
             ' H/Pu = ' + str(HPu)+' Plutonium Nitrate Solution 			\n'\
             ' v7.1-252n 									\n'\
             ' read comp  									\n'\
             '   solution  									\n'\
             '       mix=1  								\n'\
             '          rho[pu(no3)4]=' + str(Density) + ' 94239 100 density=?      	\n'\
             '          temp=300 vol_frac=1.0 molar[hno3]=' + str(M[i]) +'          	\n'\
             '   end solution 		 					     	\n\n'\
             '   h2o 2 1.0 end 	 							\n'\
      	     ' end comp                                                           	\n\n'\
      	     ' read geometry                                                      	\n\n'\
             ' global unit 1                                                      	\n\n'\
 	         '   sphere 10 23.0                                                    	 \n'\
             '   media 1 1 10 						              	\n'\
             '   cuboid 11 6p30 							\n'\
             '   media 2 1 11 -10  					           	 \n\n'\
             '   boundary 11  						                  \n'\
             ' end geometry  						            	\n\n'\
             ' read parameters 						              		\n'\
             ' run=no                                        \n'\
             ' end parameters  							     \n\n'\
             ' end data  									\n'\
             'end                                           \n'\
			 '=shell                                         \n'\
			 ' cp ft04f001 ${OUTDIR}/punitrate_MG.ampx        \n'\
			 'end '
       inputname=str('punitrate_'+str(HPu)+'_'+str(M[i])+'.inp')
       a1=open(inputname,'w')
       a1.writelines(input)
     
#       if HPu == HPuRun:
#	     print inputname
#         os.system(RunScale)  


if __name__ == "__main__":
    main() 
#noh clears

