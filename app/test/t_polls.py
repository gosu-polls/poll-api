from app.src.database.db.poll.poll import Poll as Poll
from app.src.database.dbutil.poll_object import Poll_Object as Poll_Object
from app.src.database.db.poll.group import Group as Group
from app.src.database.db.poll.group_detail import Group_Detail as Group_Detail
from app.src.database.db.vote.vote import Vote as Vote
from app.src.database.db.vote.vote_detail import Vote_Detail as Vote_Detail
import json
class TestSuite():

    @staticmethod
    def get_participating_polls(email: str):
        data = []
        group_detail = Group_Detail().GetData()
        group = Group().GetData()
        poll = Poll().GetData()
        data = [p for p in poll if p['poll_id'] in 
                    [g['poll_id'] for g in group if g['group_id'] in 
                        [gd['group_id'] for gd in group_detail if gd['email'] == email]]
                ]
        return data
    @staticmethod
    def test_get_poll(poll_id: int) -> dict:
        print('******************************************************************')

        data = Poll().GetDatum(poll_id)
        print(data)
        return {'data': data}
    
    @staticmethod
    def test_vote_detail() -> dict:
        print('******************************************************************')
        data = []
        vote = [
             {'vote_id': 1,'vote_title': 'Eng vs Nz','valid_from': '', 'valid_to': '20231005 090000', 'poll_id': 1},
             {'vote_id': 2,'vote_title': 'Ned vs Pak','valid_from': '20231005 090000', 'valid_to': '20231006 090000', 'poll_id': 1},
        ]

        vote_detail = [
            {'vote_detail_id': 1, 'vote_id': 1, 'option': 'Eng'},
            {'vote_detail_id': 2, 'vote_id': 1, 'option': 'NZ'},
            {'vote_detail_id': 3, 'vote_id': 1, 'option': 'NR/Tie'},
            {'vote_detail_id': 4, 'vote_id': 2, 'option': 'Ned'},
            {'vote_detail_id': 5, 'vote_id': 2, 'option': 'Pak'},
            {'vote_detail_id': 6, 'vote_id': 2, 'option': 'NR/Tie'}
        ]
        
        data = []
        # u = User().GetUser(request)
        # if u != None:
        email = 'kirankumar.gosu@gmail.com'
        participating_polls = TestSuite().get_participating_polls(email)
        for pp in participating_polls:
            po = Poll_Object(pp)
            # print(f'poll object of {pp} is {po.poll_name}.{po.poll_id}')
            vote = Vote(po).GetData()
            vote_detail = Vote_Detail(po).GetData()
            # print(vote)
            # print(vote_detail)
            # for each poll_id, get the vote
            # for each vote, get vote_detail
            # for each vote_detail get ballot
            poll_data = []
            for v in vote:
                print('vote: ', v)
                vd = [vd for vd in vote_detail if vd['vote_id'] == v['vote_id']]
                print('vote_detail: ', vd)
                v['vote_detail'] = vd 
                print('vote after: ', v)
                poll_data.append(v)
                
                # poll_data = [vd for vd in vote_detail if vd['vote_id'] in 
                #                 [v['vote_id'] for v in vote]
                #             ]
            data.append({'poll_id': pp['poll_id'],
                        #  'vote_title': v['vote_title'],
                        'data': poll_data})
            # data.append({pp['poll_id']: poll_data})
        # jsonStr = json.dumps(data)
        print(json.dumps(data, indent=4))
        # print(data)
        return {'data': data}