import numpy as np

###############################taking input##################################################################################################################
def takeInput():
    number_of_processes = int(input("enter number of processes: "))
    number_of_resources = int(input("enter number of resources: "))
    
    
    allocation = []
    maxx = []
    available = []
    
    print("please enter the allocation matrix row by row")
    
    
    
    for i in range(number_of_processes):
        s = input('enter allocated resources of p'+str(i)+', separated by spaces: ').split()
        
        row = []
            
        for integer in s:
            row.append(int(integer))
    
        
    
        allocation.append(row)
    
    
    print('  ')
    print("please enter the Max matrix row by row")
    
    for i in range(number_of_processes):
        s = input('enter max resources of p'+str(i)+', separated by spaces: ').split()
        
        row = []
            
        for integer in s:
            row.append(int(integer))
    
        
    
        maxx.append(row)
    
    
    s = input('enter available vector separated by spaces: ').split()
           
    for integer in s:
        available.append(int(integer))

    return allocation,maxx,available,number_of_processes,number_of_resources
############################################################################################################################################################

#################################calculate Need matrix #####################################################################################################
def getNeed(allocation,maxx,avaliable):
    Allocation = np.array(allocation)
    Max = np.array(maxx)
    Avaliable = np.array(avaliable)
    Need = Max - Allocation
    return Allocation,Max,Avaliable,Need
############################################################################################################################################################

def arrayLessThanOrEqual(arr1,arr2,size):
    flag = True
    for i in range(size):
        if arr1[i] > arr2[i]:flag = False
    return flag
    

################################################################safety######################################################################################
def safety(Allocation,Avaliable,Need,number_of_processes,number_of_resources):
    work = np.copy(Avaliable)
    finish = np.zeros(shape=(number_of_processes,1),dtype=bool)
    sequence = []
    i = 0
    count = 0
    while count < number_of_processes*2:
        index = 404
        if i >= number_of_processes:i=0
    

        if finish[i] == False and arrayLessThanOrEqual(Need[i,:],work,number_of_resources):
            #print("Im here")
            index = i
            sequence.append(i)
        else:
            count = count+1
            i = i+1
            continue


        
        work = work + Allocation[i,:]
        finish[i] = True
        count = count+1
        i = i+1



    
    
    safe = True
    
    for x in finish:
        if x == False:safe=False
    
    return safe,sequence
############################################################################################################################################################    

##############################################################resource_request##############################################################################
def resource_request(Allocation,Avaliable,Need,number_of_processes,number_of_resources):
    process = int(input("enter the process number"))
    request = []
    s = input('enter request vector separated by spaces: ').split()
           
    for integer in s:
        request.append(int(integer))


    #print(request,Need[process,:])

    condition1 = arrayLessThanOrEqual(request,Need[process,:],number_of_resources)
    condition2 = arrayLessThanOrEqual(request,Avaliable,number_of_resources)
   
    if condition1 == False:
        print("Error,process has exceed its maximum claim")
        return 404

    if condition2 == False:
        print("process must wait till resources are avaliable")
        return 404

    


    Request = np.array(request)



    Avaliable = Avaliable - Request

    Allocation[process,:] = Allocation[process,:] + Request

    print(Allocation)

    Need[process,:] = Need[process,:] - Request

    safe,sequence = safety(Allocation,Avaliable,Need,number_of_processes,number_of_resources)

    return safe,sequence,process
############################################################################################################################################################


while True:

    allocation,maxx,available,number_of_processes,number_of_resources = takeInput()

    Allocation,Max,Avaliable,Need = getNeed(allocation,maxx,available)
    
    
    print("Need matrix :")
    print(Need)
    
    while True:
        choose = input("enter 'S' to check safe state, or enter 'R' to chech immediate request safety, and any key to enter new input ")

        if choose == 'S':
            safe,sequence = safety(np.copy(Allocation),np.copy(Avaliable),np.copy(Need),number_of_processes,number_of_resources)
            if safe:
                print("Yes , Safe state <",sequence,">")
            else:
                print('Not safe')

    
    
        elif choose == 'R':
            safe,sequence,process = resource_request(np.copy(Allocation),np.copy(Avaliable),np.copy(Need),number_of_processes,number_of_resources)
            if safe:
                print("Yes request can be granted with safe state , Safe state <P"+str(process)+"req",sequence,">")
            else:
                print('Not safe')
    
        else:
            break
    


    

    
    
    
    


