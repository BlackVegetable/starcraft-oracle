
import sys
import sc2reader
import os
import shutil
from sc2reader.engine.plugins import APMTracker

sc2reader.engine.register_plugin(APMTracker())
BASE_PATH = "../replays/"
NEUTRAL = 0
VALID_REPLAYS_TO_PROCESS = 700
VEHICLE_WEAPON = 0
VEHICLE_ARMOR = 1
SHIP_WEAPON = 2
SHIP_ARMOR = 3
INFANTRY_WEAPON = 4
INFANTRY_ARMOR = 5

def remove_marked():
    with open('blacklist.txt', 'r+') as f:
        for x in f:
            print x[11:-1]
            shutil.move(x[:-1], "c:/useless_replays/" + x[11:-1]) 
        f.write("\n")

def mark_bad_replay(rep, f):
    '''Assumes file f has already been opened.
    Returns True if a bad replay was marked.'''
    if rep.players[0].play_race != "Terran" or rep.players[1].play_race != "Terran":
        f.write(rep.filename + "\n")
        print "Marked bad file"
        return True
    return False
        
def main():
    total_count = 0
    all_replays = sc2reader.load_replays(BASE_PATH)
    with open('blacklist.txt', 'a') as f:
        for rep in all_replays:
            if mark_bad_replay(rep, f):
                continue
            # Short circuit for filtering ---
            #total_count += 1
            #if total_count > VALID_REPLAYS_TO_PROCESS:
            #    break
            #continue
            # -------------------------------
            
            game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
            print "Game Processed #: " + `total_count`
            print "Game lasted: " + `game_time` + " seconds."
            
            apms = getAPM(rep)
            print "Winner APM: " + `apms[0]`
            print "Loser APM: " + `apms[1]` + "\n"
            
            #avgWorkersList = getAverageWorkers(rep)
            #print avgWorkersList[0][0] + " Avg Workers (0~80): " + str(avgWorkersList[0][1])
            #print avgWorkersList[1][0] + " Avg Workers (0~80): " + str(avgWorkersList[1][1]) + "\n"
            #avgMineralList = getMineralRate(rep)
            #print avgMineralList[0][0] + " Avg Mineral Rate (0~80): " + str(avgMineralList[0][1])
            #print avgMineralList[1][0] + " Avg Mineral Rate (0~80): " + str(avgMineralList[1][1]) + "\n"
            #avgGasList = getGasRate(rep)
            #print avgGasList[0][0] + " Avg Gas Rate (0~80): " + str(avgGasList[0][1])
            #print avgGasList[1][0] + " Avg Gas Rate (0~80): " + str(avgGasList[1][1]) + "\n"
            #upgrades = getBasicUpgrades(rep)
            #print "Winner --" + \
            #      " Vehicles: " + `upgrades[0][VEHICLE_WEAPON]` + "/" + `upgrades[0][VEHICLE_ARMOR]` + \
            #      " Ships: " + `upgrades[0][SHIP_WEAPON]` + "/" + `upgrades[0][SHIP_ARMOR]` + \
            #      " Infantry: " + `upgrades[0][INFANTRY_WEAPON]` + "/" + `upgrades[0][INFANTRY_ARMOR]`
            #print "Loser --" + \
            #      " Vehicles: " + `upgrades[1][VEHICLE_WEAPON]` + "/" + `upgrades[1][VEHICLE_ARMOR]` + \
            #      " Ships: " + `upgrades[1][SHIP_WEAPON]` + "/" + `upgrades[1][SHIP_ARMOR]` + \
            #      " Infantry: " + `upgrades[1][INFANTRY_WEAPON]` + "/" + `upgrades[1][INFANTRY_ARMOR]`
            # marinesList = getUnitBuilt(rep, "Marine")
            # print marinesList[0][0] + " Marines Built (0~80): " + str(marinesList[0][1])
            # print marinesList[1][0] + " Marines Built (0~80): " + str(marinesList[1][1]) + "\n"
            # marauderList = getUnitBuilt(rep, "Marauder")
            # print marauderList[0][0] + " Marauders Built (0~80): " + str(marauderList[0][1])
            # print marauderList[1][0] + " Marauders Built (0~80): " + str(marauderList[1][1]) + "\n"
            # reaperList = getUnitBuilt(rep, "Reaper")
            # print reaperList[0][0] + " Reapers Built (0~80): " + str(reaperList[0][1])
            # print reaperList[1][0] + " Reapers Built (0~80): " + str(reaperList[1][1]) + "\n"
            # hellionList = getUnitBuilt(rep, "Hellion")
            # print hellionList[0][0] + " Hellions Built (0~80): " + str(hellionList[0][1])
            # print hellionList[1][0] + " Hellions Built (0~80): " + str(hellionList[1][1]) + "\n"
            # bansheeList = getUnitBuilt(rep, "Banshee")
            # print bansheeList[0][0] + " Banshees Built (0~80): " + str(bansheeList[0][1])
            # print bansheeList[1][0] + " Banshees Built (0~80): " + str(bansheeList[1][1]) + "\n"
            # battlecruiserList = getUnitBuilt(rep, "Battlecruiser")
            # print battlecruiserList[0][0] + " Battlecruisers Built (0~80): " + str(battlecruiserList[0][1])
            # print battlecruiserList[1][0] + " Battlecruisers Built (0~80): " + str(battlecruiserList[1][1]) + "\n"
            # ghostList = getUnitBuilt(rep, "Ghost")
            # print ghostList[0][0] + " Ghosts Built (0~80): " + str(ghostList[0][1])
            # print ghostList[1][0] + " Ghosts Built (0~80): " + str(ghostList[1][1]) + "\n"
            # medivacList = getUnitBuilt(rep, "Medivac")
            # print medivacList[0][0] + " Medivacs Built (0~80): " + str(medivacList[0][1])
            # print medivacList[1][0] + " Medivacs Built (0~80): " + str(medivacList[1][1]) + "\n"
            # ravenList = getUnitBuilt(rep, "Raven")
            # print ravenList[0][0] + " Ravens Built (0~80): " + str(ravenList[0][1])
            # print ravenList[1][0] + " Ravens Built (0~80): " + str(ravenList[1][1]) + "\n"
            # tankList = getUnitBuilt(rep, "SiegeTank")
            # print tankList[0][0] + " Tanks Built (0~80): " + str(tankList[0][1])
            # print tankList[1][0] + " Tanks Built (0~80): " + str(tankList[1][1]) + "\n"
            # thorList = getUnitBuilt(rep, "Thor")
            # print thorList[0][0] + " Thors Built (0~80): " + str(thorList[0][1])
            # print thorList[1][0] + " Thors Built (0~80): " + str(thorList[1][1]) + "\n"
            # vikingList = getUnitBuilt(rep, "VikingFighter")
            # print vikingList[0][0] + " Vikings Built (0~80): " + str(vikingList[0][1])
            # print vikingList[1][0] + " Vikings Built (0~80): " + str(vikingList[1][1]) + "\n"
            # hellbatList = getUnitBuilt(rep, "HellionTank")
            # print hellbatList[0][0] + " Hellbats Built (0~80): " + str(hellbatList[0][1])
            # print hellbatList[1][0] + " Hellbats Built (0~80): " + str(hellbatList[1][1]) + "\n"
            # widowMineList = getUnitBuilt(rep, "WidowMine")
            # print widowMineList[0][0] + " WidowMines Built (0~80): " + str(widowMineList[0][1])
            # print widowMineList[1][0] + " WidowMines Built (0~80): " + str(widowMineList[1][1]) + "\n"
            print "-----------------------------"
            
            total_count += 1
            if total_count > VALID_REPLAYS_TO_PROCESS:
                break

def getAPM(rep):
    if rep.players[0].result == "Win":
        return [int(rep.players[0].avg_apm), int(rep.players[1].avg_apm)]
    else:
        return [int(rep.players[1].avg_apm), int(rep.players[0].avg_apm)]
                
def getBasicUpgrades(rep, start=0.0, end=0.8):
    ''' Returns the number of levels of upgrades a player finishes.  Format:
    Winner is listed first:
    [[v_weapon, v_armor, s_weapon, s_armor, i_weapon, i_armor],
    [v_weapon, v_armor, s_weapon, s_armor, i_weapon, i_armor]] '''
    upgrade_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.UpgradeCompleteEvent)]
    game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
    pids = []
    playerA_amt = [0,0,0,0,0,0]
    playerB_amt = [0,0,0,0,0,0]
    playerAmt = [playerA_amt, playerB_amt]
    vWeaponEvents = ["TerranVehicleWeaponsLevel1", "TerranVehicleWeaponsLevel2", "TerranVehicleWeaponsLevel3"]
    vArmorEvents = ["TerranVehiclePlatingLevel1", "TerranVehicalPlatingLevel2", "TerranVehicalPlatingLevel3"]
    sWeaponEvents = ["TerranShipWeaponsLevel1", "TerranShipWeaponsLevel2", "TerranShipWeaponsLevel3"]
    sArmorEvents = ["TerranVehicleAndShipArmorsLevel1", "TerranVehicleAndShipArmorsLevel2", "TerranVehicleAndShipArmorsLevel3"]
    iWeaponEvents = ["TerranInfantryWeaponsLevel1", "TerranInfantryWeaponsLevel2", "TerranInfantryWeaponsLevel3"]
    iArmorEvents = ["TerranInfantryArmorsLevel1", "TerranInfantryArmorsLevel2", "TerranInfantryArmorsLevel3"]
    basicUpgradeEvents = vWeaponEvents + vArmorEvents + sWeaponEvents + sArmorEvents + iWeaponEvents + iArmorEvents
    
    def _getSlot(upgrade_name, upgrade_pid):
        playerSlot = None
        if upgrade_pid == pids[0]:
            playerSlot = 0
        else:
            playerSlot = 1
        upgradeMatrix = [vWeaponEvents, vArmorEvents, sWeaponEvents,
                         sArmorEvents, iWeaponEvents, iArmorEvents]
        for i in range(0,6):
            if upgrade_name in upgradeMatrix[i]:
                return (playerSlot, i)
    
    for event in upgrade_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.upgrade_type_name in basicUpgradeEvents:
            if event.pid not in pids and event.pid != NEUTRAL:
                pids.append(event.pid)
            slotTuple = _getSlot(event.upgrade_type_name, event.pid)
            playerAmt[slotTuple[0]][slotTuple[1]] += 1
    if rep.players[0].result == "Win":
        return playerAmt
    else:
        return [playerAmt[1], playerAmt[0]]
    
def getUnitBuilt(rep, name, start=0.0, end=0.80):
    ''' Returns the number of a specified unit built within the time frame given.
    Format: [["Winner", amt]["Loser", amt]]'''
    unit_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.UnitBornEvent)]
    game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
    pids = []
    playerA_amt = 0
    playerB_amt = 0
    for event in unit_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.unit_type_name == name:
            if event.upkeep_pid not in pids and event.upkeep_pid != NEUTRAL:
                pids.append(event.upkeep_pid)
            if event.upkeep_pid == pids[0]:
                playerA_amt += 1
            else:
                playerB_amt += 1
    if rep.players[0].result == "Win":
        return [["Winner:", int(playerA_amt)],["Loser:", int(playerB_amt)]]
    elif rep.players[1].result == "Win":
        return [["Winner:", int(playerB_amt)],["Loser:", int(playerA_amt)]]
    else:
        return [["No winner found:", playerA_amt],["No winner found:", playerB_amt]]
        
def getGasRate(rep, start=0.0, end=0.8):
    ''' Returns the average amount of gas collected for each player
    over the course of the replay. Format:
    [["Winner", amt]["Loser", amt]]'''
    stats_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.PlayerStatsEvent)]
    game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
    pids = []
    playerA_amt = 0.0
    playerB_amt = 0.0
    event_count = len(stats_events) / 2 # How many events belonged to each player.
    for event in stats_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.pid not in pids:
            pids.append(event.pid)
        if event.pid is pids[0]:
            playerA_amt += event.vespene_collection_rate
        else:
            playerB_amt += event.vespene_collection_rate
    playerA_amt /= float(event_count)
    playerB_amt /= float(event_count)
    if rep.players[0].result == "Win":
        return [["Winner:", int(playerA_amt)],["Loser:", int(playerB_amt)]]
    elif rep.players[1].result == "Win":
        return [["Winner:", int(playerB_amt)],["Loser:", int(playerA_amt)]]
    else:
        return [["No winner found:", playerA_amt],["No winner found:", playerB_amt]]
        
def getMineralRate(rep, start=0.0, end=0.8):
    ''' Returns the average amount of minerals collected for each player
    over the course of the replay. Format:
    [["Winner", amt]["Loser", amt]]'''
    stats_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.PlayerStatsEvent)]
    game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
    pids = []
    playerA_amt = 0.0
    playerB_amt = 0.0
    event_count = len(stats_events) / 2 # How many events belonged to each player.
    current_count = 0
    for event in stats_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.pid not in pids:
            pids.append(event.pid)
        if event.pid is pids[0]:
            playerA_amt += event.minerals_collection_rate
        else:
            playerB_amt += event.minerals_collection_rate
    playerA_amt /= float(event_count)
    playerB_amt /= float(event_count)
    if rep.players[0].result == "Win":
        return [["Winner:", int(playerA_amt)],["Loser:", int(playerB_amt)]]
    elif rep.players[1].result == "Win":
        return [["Winner:", int(playerB_amt)],["Loser:", int(playerA_amt)]]
    else:
        return [["No winner found:", playerA_amt],["No winner found:", playerB_amt]]
        
        
def getAverageWorkers(rep, start=0.0, end=0.8):
    ''' Returns an average number of workers active for each player
    over the course of the replay.  Returns this in a list of list format:
    [["Winner", count],["Loser", count]]'''
    stats_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.PlayerStatsEvent)]
    game_time = rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours
    pids = []
    playerA_count = 0
    playerB_count = 0
    event_count = len(stats_events) / 2 # How many events belonged to each player.
    current_count = 0
    for event in stats_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.pid not in pids:
            pids.append(event.pid)
        if event.pid is pids[0]:
            playerA_count += event.workers_active_count
        else:
            playerB_count += event.workers_active_count
    playerA_count /= event_count
    playerB_count /= event_count
    if rep.players[0].result == "Win":
        return [["Winner:", playerA_count],["Loser:", playerB_count]]
    elif rep.players[1].result == "Win":
        return [["Winner:", playerB_count],["Loser:", playerA_count]]
    else:
        return [["No winner found:", playerA_count],["No winner found:", playerB_count]]
    
def formatReplay(replay):
    output =  replay.filename +'\n'
    output += '-------------------------\n'
    output += replay.category+' Game, '+str(replay.start_time)+'\n'
    output += replay.type+' on '+replay.map_name+'\n'
    output += 'Length: '+str(replay.game_length)
    return output
    
def formatPlayers(replay):
    if replay.type != '1v1':
        return "Not a 1v1 match"
    output_string = ""
    for team in replay.teams:
        for player in team:
            output_string += "\n    " + player.pick_race[0] + " " + player.name
    return output_string
    
def isBadMatch(replay):
    '''If the level difference between the players is 
    beyond a threshold or if the match in question is
    not a 1v1 or if either player was an AI,
    this match is considered bad.'''
    if replay.type != '1v1':
        print "Wasn't a 1v1"
        return True
    if replay.winner is None:
        print "No winner"
        return True
    if len(replay.humans) != 2:
        print "Player was an AI"
        return True
    
    sidA = replay.humans[0].sid
    sidB = replay.humans[1].sid
    
    #levelA = replay.humans[0].sidcombined_race_levels
    #levelB = replay.users[1].combined_race_levels
    #if math.abs(levelA - levelB) > 25:
    #    print "Players too different: " + str(math.abs(lavelA - levelB))
    #    return True
    return False
    
def getWinner(replay):
    winningPid = None
    if replay.winner is replay.teams[0]:
        winningPid = replay.teams[0].players[0].pid
    elif replay.winner is replay.teams[1]:
        winningPid = replay.teams[1].players[0].pid
    else:
        print "What the heck?  Wrong team won??"
    return winningPid
    
#def formatUsers(replay):
#    output_string = ""
#    output_string = "\n    " + replay.users[0].uid
#    output_string = "\n    is level: " + str(replay.users[0].combined_race_levels)
#    output_string = "\n    has highest league: " + replay.users[0].highest_league
#    output_string = "----------------"
#    output_string = "\n    " + replay.users[1].uid
#    output_string = "\n    is level: " + str(replay.users[1].combined_race_levels)
#    output_string = "\n    has highest league: " + replay.users[1].highest_league
#    return output_string
    

if __name__ == '__main__':
    main()
    
    