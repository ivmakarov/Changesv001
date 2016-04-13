from ElementsT1 import *

from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
        
        # linux
        taiji = load_from_file(taijiLName)

        liangyi = load_from_file(liangyiLName)

        sixiang = load_from_file(sixiangLName)

        bagua = load_from_file(baguaLName)

        Hextable  = load_from_file(HextableLName)

        wuxing = load_from_file(wuxingLName)

        stems = load_from_file(stemsLName)

        branches = load_from_file(branchesLName)
        
        channels = load_from_file(channelsLName)

	points = load_from_file(pointsLName)

elif _platform == "darwin":
        # OS X
        taiji = load_from_file(taijiLName)

        liangyi = load_from_file(liangyiLName)

        sixiang = load_from_file(sixiangLName)

        bagua = load_from_file(baguaLName)

        Hextable  = load_from_file(HextableLName)

        wuxing = load_from_file(wuxingLName)

        stems = load_from_file(stemsLName)

        branches = load_from_file(branchesLName)
        
        channels = load_from_file(channelsLName)

	points = load_from_file(pointsLName)

elif _platform == "win32":
        # Windows...
        taiji = load_from_file(taijiWName)

        liangyi = load_from_file(liangyiWName)

        sixiang = load_from_file(sixiangWName)

        bagua = load_from_file(baguaWName)

        Hextable  = load_from_file(HextableWName)

        wuxing = load_from_file(wuxingWName)

        stems = load_from_file(stemsWName)

        branches = load_from_file(branchesWName)
        
        channels = load_from_file(channelsWName)

	points = load_from_file(pointsWName)



from ChangesT1_medical import med_unit



P1 = med_unit()
