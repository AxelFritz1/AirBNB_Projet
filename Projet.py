#On importe nos 3 modules
import Data
import Interface

#On récupère nos données nettoyées (prend environ 10 secondes)
lis = Data.clean_lis()
cal = Data.clean_cal_price()

#On lance notre interface
Interface.Interface(lis, cal)