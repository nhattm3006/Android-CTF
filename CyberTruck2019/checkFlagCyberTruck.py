staticFlag = ["s3cr3t$_n3veR_mUst_bE_h4rdc0d3d_m4t3!",
              "d474_47_r357_mu57_pR073C73D700!!",
              "Native_c0d3_1s_h4rd3r_To_r3vers3"]

dynamicFlag =  ["046e04ff67535d25dfea022033fcaaf23606b95a5c07a8c6",
                "512100f7cc50c76906d23181aff63f0d642b3d947f75d360b6b15447540e4f16",
                "backd00r$Mu$tAlw4ysBeF0rb1dd3n$$"]

def checkStaticFlag1(flag):
    if(flag == staticFlag[0]):
        print("Congrats! You captured static flag 1.")

def checkStaticFlag2(flag):
    if(flag == staticFlag[1]):
        print("Congrats! You captured static flag 2.")

def checkStaticFlag3(flag):
    if(flag == staticFlag[2]):
        print("Congrats! You captured static flag 3.")

def checkDynamicFlag1(flag):
    if(flag == dynamicFlag[0]):
        print("Congrats! You captured dynamic flag 1.")

def checkDynamicFlag2(flag):
    if(flag == dynamicFlag[1]):
        print("Congrats! You captured dynamic flag 2.")

def checkDynamicFlag3(flag):
    if(flag == dynamicFlag[2]):
        print("Congrats! You captured dynamic flag 3.")

while(True):
    print("\n--------------------")
    flag = input("Input Flag here: ")
    checkStaticFlag1(flag)
    checkStaticFlag2(flag)
    checkStaticFlag3(flag)
    checkDynamicFlag1(flag)
    checkDynamicFlag2(flag)
    checkDynamicFlag3(flag)
    
    again = input("\nCheck another Flag? (Enter n to exit): ")
    if(again == "n" or again == "N"):
        break
 