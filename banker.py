import numpy as np

###############################taking input##################################################################################################################
def takeInput():
    try:
        number_of_processes = int(input("enter number of processes: "))
        number_of_resources = int(input("enter number of resources: "))
    except ValueError:
        print('invalid input')
        return -1
    
    
    
    allocation = []   #
    maxx =  []      # 
    available = []  #
    
    print("please enter the allocation matrix row by row")
    
    
    
    for i in range(number_of_processes):
        s = input('enter allocated resources of p'+str(i)+', separated by spaces: ').split()
        
        row = []
            
        for integer in s:
            row.append(int(integer))
    
        
        if len(row) != number_of_resources:
            print("invalid allocation matrix")
            print(' ')
            return -1
            
        allocation.append(row)
    
    
    print('  ')
    print("please enter the Max matrix row by row")
    
    for i in range(number_of_processes):
        s = input('enter max resources of p'+str(i)+', separated by spaces: ').split()
        
        row = []
            
        for integer in s:
            row.append(int(integer))
    
        if len(row) != number_of_resources:
            print("invalid Max matrix")
            print(' ')
            return -1
    
        maxx.append(row)
    
    print(' ')
    s = input('enter available vector separated by spaces: ').split()
           
    for integer in s:
        available.append(int(integer))

    if len(available) != number_of_resources:
            print("invalid avaliable vector")
            print(' ')
            return -1

    return allocation,maxx,available,number_of_processes,number_of_resources
############################################################################################################################################################

#################################calculate Need matrix #####################################################################################################
def getNeed(allocation,maxx,avaliable):
    Allocation = np.array(allocation)
    Max = np.array(maxx)
    Avaliable = np.array(avaliable)
    Need = Max - Allocation
    return Allocation,Avaliable,Need
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
    try:
        process = int(input("enter the process number: "))
        request = []
        s = input('enter request vector separated by spaces: ').split()
    except ValueError:
        return 404
    
           
    for integer in s:
        request.append(int(integer))


    

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

    Need[process,:] = Need[process,:] - Request

    safe,sequence = safety(Allocation,Avaliable,Need,number_of_processes,number_of_resources)

    return safe,sequence,process
############################################################################################################################################################


while True:
    
    try:
        allocation,maxx,available,number_of_processes,number_of_resources = takeInput()
    except TypeError:
        continue


    

    Allocation,Avaliable,Need = getNeed(allocation,maxx,available)

    
    
    print("Need matrix :")
    print(Need)
    
    while True:
        choose = input("enter 'S' to check safe state, or enter 'R' to chech immediate request safety, and any key to enter new input ")

        if choose == 'S':
            safe,sequence = safety(np.copy(Allocation),np.copy(Avaliable),np.copy(Need),number_of_processes,number_of_resources)

            p_sequence= []

            for num in sequence:
                p_sequence.append("p"+str(num))

            if safe:
                print("Yes , Safe state <",p_sequence,">")
            else:
                print('Not safe')

    
    
        elif choose == 'R':
            try:
                safe,sequence,process = resource_request(np.copy(Allocation),np.copy(Avaliable),np.copy(Need),number_of_processes,number_of_resources)
            except TypeError:
                print("Not safe")
                print(' ')
                continue
            
            
            p_sequence= []

            for num in sequence:
                p_sequence.append("p"+str(num))


            if safe:
                print("Yes request can be granted with safe state , Safe state <P"+str(process)+"req",p_sequence,">")
                print(' ')
            else:
                print('Not safe')
                print(' ')
    
        else:
            break
    


    

    
    
    
    


