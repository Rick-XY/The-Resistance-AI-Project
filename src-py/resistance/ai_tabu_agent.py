from agent import Agent
import random
import __main__
import copy

# Zuping Liu (22660453)
# Xinyu Lei (22604588)


class AIAgent1(Agent):
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name='AI'):
        '''
        Initialises the agent.
        '''
        self.name = name

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list
        temp_list = []
        round = 0
        mission_abort = 0
        betray_required = 0

        # initialize the watch list
        for i in range(number_of_players):
            temp_list.append(i)
        watch_list = dict.fromkeys(temp_list, 0)

        self.watch_list = watch_list
        self.round = round
        self.mission_abort = mission_abort
        self.betray_required = betray_required

    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list

    def tabu_search(self, watch_list, team):
        '''
        expect a herustic list and the team list of original proposed
        '''
        bestTeam = []
        tabuList = []
        recording = []
        teamList = [i for i in range(self.number_of_players) if i not in team]
        bestScore = 0
        score = 0
        max_tabu_length = 2
        for player in team:
            # calculate the base for the tabu search
            bestScore += watch_list[player]

        # tabu search
        if bestScore > 0:
            for times in range(30):
                for j in range(len(team)):
                    for i in range(len(teamList)):
                        temp = team[j]
                        team[j] = teamList[i]
                        teamList[i] = temp
                        score = 0
                        for player in team:
                            # calculate the new value for the tabu search
                            score += self.watch_list[player]
                        if sorted([j, i]) not in tabuList and score < bestScore:
                            recording.append(sorted([j, i]))
                            bestTeam.clear()
                            bestTeam = copy.deepcopy(team)
                            teamList[i] = temp
                        elif score >= bestScore:
                            teamList[i] = team[j]
                            team[j] = temp
                if score < bestScore:
                    bestScore = score
                if len(recording) != 0:
                    tabuList.append(recording[-1])
                recording.clear()
                if len(tabuList) > max_tabu_length:
                    tabuList.pop(0)
            return bestTeam
        else:
            return team

    def propose_mission(self, team_size, betrayals_required=1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        team = []
        # find the biggest number in watch_list
        max = 0
        for player in self.watch_list:
            if max < self.watch_list[player]:
                max = self.watch_list[player]

        # try to filter those players who have the highest mark and vote them out
        guess_spy_list = []
        for player in self.watch_list:
            if self.watch_list[player] == max and max != 0:
                guess_spy_list.append(player)

        # add logic into the agent when to propose its allies
        if self.is_spy():
            for allies in self.spy_list:
                team.append(allies)
            while len(team) < team_size:
                agent = random.randrange(team_size)
                if agent not in team:
                    team.append(agent)
            return team
        else:
            team.append(self.player_number)
            while len(team) < team_size:
                agent = random.randrange(team_size)
                if agent not in team:
                    team.append(agent)
            teams = self.tabu_search(self.watch_list, team)

            # making sure the team list return won't be empty or not enough people
            if len(teams) == team_size:
                return teams
            else:
                while len(teams) < team_size:
                    agent = random.randrange(team_size)
                    if agent not in teams:
                        teams.append(agent)
                while len(teams) > team_size:
                    teams.pop(0)
                return teams

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        vote_false = 0.5
        if self.is_spy() and self.player_number not in mission:
            return False
        elif self.is_spy() and self.mission_abort >= 3:
            return False
        elif self.is_spy() == False and self.round == 0:
            return True

        # find the biggest number in watch_list
        max = 0
        for player in self.watch_list:
            if max < self.watch_list[player]:
                max = self.watch_list[player]

        # try to filter those players who have the highest mark and vote them out
        guess_spy_list = []
        for player in self.watch_list:
            if self.watch_list[player] == max and max != 0:
                guess_spy_list.append(player)

        if self.is_spy() != True and max != 0:
            if proposer in guess_spy_list:
                return False
            for player in guess_spy_list:
                if player in mission and self.mission_abort < 5:
                    vote_false = 0.1
                    break
                elif player in mission:
                    vote_false = 1
                    break

        return random.random() < vote_false

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        if self.number_of_players/2 > len(votes):
            self.mission_abort += 1

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        betray_rate = 0.9

        if self.is_spy():
            return random.random() < betray_rate

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        if self.is_spy() != True and betrayals != 0:
            for opponent in mission:
                if opponent != self.player_number:  # no need to add value for myself since it's from resistant point of view
                    self.watch_list[opponent] += 0.2
                if opponent != self.player_number and self.round == 0:
                    self.watch_list[opponent] += 0.2

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        self.round = rounds_complete

    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        if self.is_spy() and spies_win == True:
            __main__.mine_win_num1 += 1
        elif self.is_spy() == False and spies_win == False:
            __main__.mine_win_num2 += 1
