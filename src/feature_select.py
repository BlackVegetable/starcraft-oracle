
import sys
import sc2reader
import os
import shutil
from sc2reader.engine.plugins import APMTracker

sc2reader.engine.register_plugin(APMTracker())

# Misc constants
BASE_PATH = "../replays/"
NEUTRAL = 0
VALID_REPLAYS_TO_PROCESS = 700

# Upgrade constants
VEHICLE_WEAPON = 0
VEHICLE_ARMOR = 1
SHIP_WEAPON = 2
SHIP_ARMOR = 3
INFANTRY_WEAPON = 4
INFANTRY_ARMOR = 5
SHIP_AND_VEHICLE_ARMOR = 6

# Timing constants
MID_GAME = 450 # 60 seconds/minute * 7.5 minutes

# Sadly hardcoded unit resource costs
UNIT_COSTS = {"Marine" : 50, "Marauder" : 125, "Reaper" : 100, "Medivac" : 200,
              "SiegeTank" : 275, "Thor" : 500, "Hellion" : 100, "HellionTank" : 100,
              "WidowMine" : 100, "Battlecruiser" : 700, "VikingFighter" : 225,
              "Raven" : 300, "Banshee" : 250, "Ghost" : 300}



def remove_marked():
    with open('blacklist.txt', 'r+') as f:
        for x in f:
            print x[11:-1]
            shutil.move(x[:-1], "c:/useless_replays/" + x[11:-1])
        f.write("\n")

def compute_time(rep):
    '''Returns the number of seconds of game_time in a replay.'''
    return rep.game_length.secs + 60 * rep.game_length.mins + 3600 * rep.game_length.hours

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

            game_time = compute_time(rep)
            print "Game Processed #: " + `total_count`
            print "Game lasted: " + `game_time` + " seconds."

            strategies = getStrategies(rep)
            print "Winner -- Start: " + strategies[0][1] + "  End: " + strategies[0][2]
            print "Loser  -- Start: " + strategies[1][1] + "  End: " + strategies[1][2] + "\n"

            #unitComps = getOpeningStrategies(rep)
            #print "Winner --------------- "
            #for key in unitComps[0][1]:
            #    if key == "Total":
            #        continue
            #    print key + ": " + `unitComps[0][1][key]` + "%"
            #print "Loser ---------------- "
            #for key in unitComps[1][1]:
            #    if key == "Total":
            #        continue
            #    print key + ": " + `unitComps[1][1][key]` + "%"

            #apms = getAPM(rep)
            #print "Winner APM: " + `apms[0]`
            #print "Loser APM: " + `apms[1]` + "\n"

            #foodBlockage = getSupplyCappedPercent(rep)
            #print foodBlockage[0][0] + " Supply Capped Time: " + `foodBlockage[0][1]` + "%"
            #print foodBlockage[1][0] + " Supply Capped Time: " + `foodBlockage[1][1]` + "%\n"

            #bunkersList = getBuildingBuilt(rep, "Bunker")
            #print bunkersList[0][0] + " Bunkers Built: " + str(bunkersList[0][1])
            #print bunkersList[1][0] + " Bunkers Built: " + str(bunkersList[1][1]) + "\n"

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



def getUnitComposition(rep, early_game=False):
    ''' Returns the unit composition for each player on this replay with each
    unit represented by a percentage of total resources spent on units (other
    than SCVs. '''
    unit_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.UnitBornEvent)]
    game_time = compute_time(rep)
    pids = []
    compA = {
              #Bio Composition Units
              "Marine" : 0,
              "Marauder" : 0,
              "Reaper" : 0,
              "Medivac" : 0,
              # Mech Composition Units
              "SiegeTank" : 0,
              "Thor" : 0,
              "HellionTank" : 0,
              "Hellion" : 0,
              # Bio-Mech Composition Units
              "WidowMine" : 0,
              # Air Units
              "VikingFighter" : 0,
              "Raven" : 0,
              "Battlecruiser" : 0,
              # Other Units
              "Banshee" : 0,
              "Ghost" : 0,
              "Total" : 0
            }
    compB = compA.copy()

    for event in unit_events:
        if early_game and event.second >= MID_GAME:
            break
        if event.unit_type_name in compA:
            if event.upkeep_pid not in pids and event.upkeep_pid != NEUTRAL:
                pids.append(event.upkeep_pid)
            if event.upkeep_pid == pids[0]:
                compA[event.unit_type_name] += UNIT_COSTS[event.unit_type_name]
                compA["Total"] += UNIT_COSTS[event.unit_type_name]
            else:
                compB[event.unit_type_name] += UNIT_COSTS[event.unit_type_name]
                compB["Total"] += UNIT_COSTS[event.unit_type_name]

    if compA["Total"] == 0:
        compA["Total"] = 1
    if compB["Total"] == 0:
        compB["Total"] = 1
    for key in compA:
        if key == "Total":
            continue
        compA[key] *= 100
        compA[key] /= compA["Total"]
    for key in compB:
        if key == "Total":
            continue
        compB[key] *= 100
        compB[key] /= compB["Total"]

    if rep.players[0].result == "Win":
        return [["Winner:", compA],["Loser:", compB]]
    else:
        return [["Winner:", compB],["Loser:", compA]]

def getStrategies(rep):
    start_comps = getUnitComposition(rep, True)
    compA = start_comps[0][1]
    compB = start_comps[1][1]
    startA = "Unknown"
    startB = "Unknown"
    def selectEarlyStrategy(comp):
        '''Strategy identification logic.'''
        # Banshees are a distinct strategy, and are thus prioritized.
        if comp["Banshee"] >= 30:
            return "Banshee Start"
        elif comp["Reaper"] >= 51:
            return "Reaper Start"
        elif comp["Marine"] >= 51:
            return "Marine Start"
        elif comp["Hellion"] + comp["HellionTank"] >= 51:
            return "Hellbat/Hellion Start"
        elif comp["Marine"] >= 25 and comp["Marauder"] >= 20 and \
             comp["Marine"] + comp["Marauder"] >= 51:
            return "Marine/Marauder Start"
        elif comp["Ghost"] >= 25:
            return "Ghost Start!?"
        else:
            return "Mixed Start"
    startA = selectEarlyStrategy(compA)
    startB = selectEarlyStrategy(compB)
    endA = "Unknown"
    endB = "Unknown"
    if compute_time(rep) < MID_GAME:
        endA = "Game Ended Early"
        endB = "Game Ended Early"
    end_comps = getUnitComposition(rep, False)
    compA = end_comps[0][1]
    compB = end_comps[1][1]
    def selectLateStrategy(comp):
        '''Strategy identification logic.'''
        if comp["Marine"] + comp["Reaper"] + comp["Marauder"] + \
           comp["Medivac"] >= 80:
           return "Bio End"
        elif comp["SiegeTank"] + comp["Thor"] + comp["Hellion"] + \
           comp["HellionTank"] >= 60:
           return "Mech End"
        elif comp["Marine"] + comp["Medivac"] >= 33 and \
             comp["SiegeTank"] + comp["WidowMine"] >= 33:
            return "Bio/Mech End"
        elif comp["Battlecruiser"] + comp["VikingFighter"] + \
             comp["Raven"] >= 45:
            return "Sky End"
        else:
            return "Mixed End"
    endA = selectLateStrategy(compA)
    endB = selectLateStrategy(compB)
    if rep.players[0].result == "Win":
        return [["Winner:", startA, endA],["Loser:", startB, endB]]
    else:
        return [["Winner:", startB, endB],["Loser:", startA, endA]]

def getBuildingBuilt(rep, name, start=0.0, end=0.8):
    '''Returns the numbers of a specific type of building whose construction
    was initiated by the players.  Thus, there is no differentiation between
    starting and cancelling a structure or having it destroyed partway, or
    actually finishing the structure.'''
    init_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.UnitInitEvent)]
    game_time = compute_time(rep)
    pids = []
    playerA_amt = 0
    playerB_amt = 0
    for event in init_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.unit_type_name != name:
            continue
        if event.upkeep_pid not in pids:
            pids.append(event.upkeep_pid)
        if event.upkeep_pid is pids[0]:
            playerA_amt += 1
        else:
            playerB_amt += 1
    if rep.players[0].result == "Win":
        return [["Winner:", playerA_amt],["Loser:", playerB_amt]]
    else:
        return [["Winner:", playerB_amt],["Loser:", playerA_amt]]

def getSupplyCappedPercent(rep, start=0.0, end=1.0):
    '''Returns an estimate of the percentage of time a player spends
    unable to produce new units due to having insufficient supply.
    This is typically considered one component of an inefficient
    playstyle.
    Returns this value as a percentage of time where this is true, as
    an int.'''
    stats_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.PlayerStatsEvent)]
    game_time = compute_time(rep)
    pids = []
    playerA_amt = 0.0
    playerB_amt = 0.0
    event_count = len(stats_events) / 2 # How many events belonged to each player.
    for event in stats_events:
        if game_time * start > event.second or game_time * end < event.second:
            break
        if event.pid not in pids:
            pids.append(event.pid)
        if event.food_made <= event.food_used:
            if event.pid is pids[0]:
                playerA_amt += 1.0
            else:
                playerB_amt += 1.0
    playerA_amt /= float(event_count)
    playerB_amt /= float(event_count)
    if rep.players[0].result == "Win":
        return [["Winner:", int(playerA_amt * 100)],["Loser:", int(playerB_amt * 100)]]
    else:
        return [["Winner:", int(playerB_amt * 100)],["Loser:", int(playerA_amt * 100)]]

def getAPM(rep):
    '''Returns the Actions per minute of the players as defined by the
    APMtracker module bundled with sc2reader.'''
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
    game_time = compute_time(rep)
    pids = []
    playerA_amt = [0,0,0,0,0,0,0] # Last value is for ship and vehicle armors which share
    playerB_amt = [0,0,0,0,0,0,0] # an upgrade in HotS.
    playerAmt = [playerA_amt, playerB_amt]
    vWeaponEvents = ["TerranVehicleWeaponsLevel1", "TerranVehicleWeaponsLevel2", "TerranVehicleWeaponsLevel3"]
    vArmorEvents = ["TerranVehiclePlatingLevel1", "TerranVehicalPlatingLevel2", "TerranVehicalPlatingLevel3",
                    "TerranVehicleAndShipArmorsLevel1", "TerranVehicleAndShipArmorsLevel2", "TerranVehicleAndShipArmorsLevel3"]
    sWeaponEvents = ["TerranShipWeaponsLevel1", "TerranShipWeaponsLevel2", "TerranShipWeaponsLevel3"]
    sArmorEvents = ["TerranShipPlatingLevel1", "TerranShipPlatingLevel2", "TerranShipPlatingLevel3",
                    "TerranVehicleAndShipArmorsLevel1", "TerranVehicleAndShipArmorsLevel2", "TerranVehicleAndShipArmorsLevel3"]
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
        shipAndVehicleArmor = ["TerranVehicleAndShipArmorsLevel1",
                              "TerranVehicleAndShipArmorsLevel2",
                              "TerranVehicleAndShipArmorsLevel3"]
        for i in range(0,6):
            if upgrade_name in shipAndVehicleArmor:
                return (playerSlot, SHIP_AND_VEHICLE_ARMOR)
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
    playerAmt[0][VEHICLE_ARMOR] += playerAmt[0][SHIP_AND_VEHICLE_ARMOR]
    playerAmt[0][SHIP_ARMOR] += playerAmt[0][SHIP_AND_VEHICLE_ARMOR]
    playerAmt[1][VEHICLE_ARMOR] += playerAmt[1][SHIP_AND_VEHICLE_ARMOR]
    playerAmt[1][SHIP_ARMOR] += playerAmt[1][SHIP_AND_VEHICLE_ARMOR]
    if rep.players[0].result == "Win":
        return playerAmt
    else:
        return [playerAmt[1], playerAmt[0]]

def getUnitBuilt(rep, name, start=0.0, end=0.80):
    ''' Returns the number of a specified unit built within the time frame given.
    Format: [["Winner", amt]["Loser", amt]]'''
    unit_events = [x for x in rep.events if isinstance(x, sc2reader.events.tracker.UnitBornEvent)]
    game_time = compute_time(rep)
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
    game_time = compute_time(rep)
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
    game_time = compute_time(rep)
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
    game_time = compute_time(rep)
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

