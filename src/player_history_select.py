import pickle
import os
from players_against_matches import Match
import sc2reader
import feature_select

class SCPlayer:
    '''Information on a player's playing patterns across matches.'''
    def __init__(self, id, bnet_id):
        self.id = id
        self.bnet_id = bnet_id
        self.apm = 0.0
        self.workers = 0.0
        self.food_capped = 0.0
        self.econ = 0.0
        self.upgrades = 0.0
        self.match_count = 0
        self.matches_won = []
        self.matches_lost = []
        self.win_count = 0
        self.p_dicts = []
        ### Strategies ###
        self.strategies = [0.0] * 35
        
    def addWin(self, match_no):
        self.matches_won.append(match_no)
        self.win_count += 1
        self.match_count += 1
        
    def addLoss(self, match_no):
        self.matches_lost.append(match_no)
        self.match_count += 1
        
    def aggregate(self):
        ''' Combine the information from all p_dicts. '''
        for d in self.p_dicts:
            self.apm += d['apm']
            self.workers += d['workers']
            self.food_capped += d['food_capped']
            if d['s_econ'] == "Early Command Center":
                self.econ += 1
            if d['s_upgrades'] == "Fast Upgrades":
                self.upgrades += 1
            
            index = -1
            if d['s_early'] == "Banshee Start":
                index = 0
            elif d['s_early'] == "Reaper Start":
                index = 5
            elif d['s_early'] == "Marine Start":
                index = 10
            elif d['s_early'] == "Hellbat/Hellion Start":
                index = 15
            elif d['s_early'] == "Marine/Marauder Start":
                index = 20
            elif d['s_early'] == "Ghost Start!?":
                index = 25
            elif d['s_early'] == "Mixed Start":
                index = 30
                
            if d['s_late'] == "Bio End":
                index += 0
            elif d['s_late'] == "Mecha End":
                index += 1
            elif d['s_late'] == "Bio/Mech End":
                index += 2
            elif d['s_late'] == "Sky End":
                index += 3
            elif d['s_late'] == "Mixed End":
                index += 4
            self.strategies[index] += 1
        count = len(self.p_dicts)
        self.apm /= count
        self.workers /= count
        self.food_capped /= count
        self.econ /= count
        self.upgrades /= count
        self.strategies = [x / count for x in self.strategies]
        
def get_bad_match_list(path):
    '''Machine specific'''
    bad_files = os.listdir(path)
    bad_list = []
    for f in bad_files:
        bad_list.append(f[:-10])
        print f + " " + f[:-10]
    return bad_list
        
def get_explicit_bad_list(fname):
    '''Machine Specific'''
    bad_list = []
    with open(fname, "rb") as f:
        for name in f:
            bad_list.append(name[18:-12])
            print "Debug: " + name[18:-12]
    return bad_list
        
def output_meta_data (replay_pickle):
    '''Writes meta data from a pickled file to a text file for testing
    a learner that has player history information.
    
    Format:
    1st Column -- Match ID
    2nd Column -- Player A ID
    3rd Column -- Player A BNET ID
    4th Column -- Player B ID
    5th Column -- Player B BNET ID
    6th Column -- Which player won (1 means player A, 2 means player B)
    '''
    matches = pickle.load(open(replay_pickle, "rb"))
    with open("test_matches.txt", "a") as f:
        for match in matches:
            output = match.match_id + ","
            output += match.player_1_id + ","
            output += match.player_1_bnet_id + ","
            output += match.player_2_id + ","
            output += match.player_2_bnet_id + ","
            output += match.winner + "\n"
            f.write(output)
    
def init_replay_data (replay_pickle):
    '''Aggregates player information across matches for all players found
    in all matches corresponding to a pickled metadata file.'''
    matches = pickle.load(open(replay_pickle, "rb"))
    
    scplayers = {}
    # Disable bad_lists in production setting.
    bad_list = get_bad_match_list("../bad_expert_replays")
    bad_list2 = get_explicit_bad_list("./more_bad.txt")
    j = 0
    k = 0
    for match in matches:
        if match.match_id in bad_list or match.match_id in bad_list2:
            j += 1
            print "Caught bad list #" + `j`
            continue
        k += 1
        if k % 5 == 0:
            print "Processed match #" + str(k)
        if match.player_1_id not in scplayers:
            scplayers[match.player_1_id] = SCPlayer(match.player_1_id, match.player_1_bnet_id)
        if match.player_2_id not in scplayers:
            scplayers[match.player_2_id] = SCPlayer(match.player_2_id, match.player_2_bnet_id)

        if match.winner == 1:
            scplayers[match.player_1_id].addWin(match.match_id)
            scplayers[match.player_2_id].addLoss(match.match_id)
        else: # Assuming no stalemates
            scplayers[match.player_2_id].addWin(match.match_id)
            scplayers[match.player_1_id].addLoss(match.match_id)
        
    k = 0
    THRESHOLD = 4
    for p_num in scplayers:
        k += 1
        if k % 5 == 0:
            print "Aggregating player #" + str(k)
        p = scplayers[p_num]
        BASE = "../expert_replays/"
        SUFFIX = ".SC2Replay"
        if p.match_count < THRESHOLD:
            continue
        for match_no in p.matches_won:
            rep = sc2reader.load_replay(BASE + `match_no`[1:-1] + SUFFIX)
            p_dict = feature_select.get_single_history(rep, isWinner=True)
            p.p_dicts.append(p_dict)
        for match_no in p.matches_lost:
            rep = sc2reader.load_replay(BASE + `match_no`[1:-1] + SUFFIX)
            p_dict = feature_select.get_single_history(rep, isWinner=False)
            p.p_dicts.append(p_dict)
        p.aggregate()
    
    def app_format(l, elm, round=False):
        if round:
            l.append("{0:.2f}".format(elm, 2))
        else:
            l.append(str(elm))
        return l
    
    k = 0
    with open("./histories.txt", "a") as f:
        for p_num in scplayers:
            k += 1
            if k % 5 == 0:
                print "Outputting player #" + str(k)
            p = scplayers[p_num]
            if p.match_count >= THRESHOLD:
                output = []
                output = app_format(output, p.id)
                output = app_format(output, p.bnet_id)
                output = app_format(output, p.apm, True)
                output = app_format(output, p.workers, True)
                output = app_format(output, p.food_capped, True)
                for i in range(len(p.strategies) -1):
                    output = app_format(output, p.strategies[i], True)
                output = app_format(output, p.econ, True)
                output = app_format(output, p.upgrades, True)
                output_string = ""
                for i in range(len(output)):
                    output_string += output[i] + ","
                f.write(output_string[:-1] + "\n")                    
    
    
def main ():
    #init_replay_data("../expert_replays/games_replays_1845.p")
    output_meta_data("../expert_replays/games_replays_78.p")

if __name__ == '__main__':
    main()