from src.database.dbutil.poll_entity import Poll_Entity
import src.database.dba.config as config
from src.database.db.poll.poll import Poll as Poll

class Point_Config(Poll_Entity):
    _df = {}
    _entity_identifier = {}

    def __new__(cls):
        try:
            # if cls._instance is None:
            hasInstance, cls._instance = cls.HasInstance()
            if not hasInstance:
                cls._df[0] = None
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet')
                cls._entity_identifier[0] = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                             'pk' : __class__.__name__.lower() + '_id',
                                             'db_type' : 'googlesheet',
                                             'db_name': config.poll_db,
                                             'table_name': __class__.__name__.lower()}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None

    @classmethod
    def GetPointsConfigForPoll(cls, poll_id: int):
        # data = []
        # point_config = cls.GetData()
        # poll_data = Poll().GetDatum(poll_id)
        # point_config_for_poll = [pc for pc in point_config if point_config['point_config_id'] == poll_data['point_config_id']]
        # if len(point_config_for_poll) == 0:
        #     point_config_for_poll = [pc for pc in point_config if point_config['point_config_name'] == 'default']
        # if len(point_config_for_poll) == 0:
        #     point_config_for_poll = [{'right': 2,
        #                               'wrong': 0}]
        # data = point_config_for_poll[0]

        data = {'right': 2, 'wrong': -2}
        point_config_id = Poll().GetDatum(poll_id)['point_config_id']
        if '{}'.format(point_config_id).isdigit():
            data = Point_Config().GetDatum(point_config_id)
        else:
            point_config_data = Point_Config().GetFilteredData({'point_config_name' : 'default'})
            if len(point_config_data) > 0:
                data = point_config_data[0]
        
        return data