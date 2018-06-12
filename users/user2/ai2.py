import sys
sys.path.append(sys.path[0] + "/users/")
import lib

def main():
   sId = lib.getMyId()
   sPos = lib.getCell(sId)
   sMP = lib.getMp(sId)
   ePos = lib.getCell(lib.getEnemyId())
   lib.setWeapon(lib.WEAPON_SIMPLE_GUN)

   path = lib.getPath(sPos, ePos)
   if path != -1:
      for cell in path:
         lib.moveOn(cell)

   lib.attackOn(ePos)

   
   pass
