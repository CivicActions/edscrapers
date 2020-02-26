import json

class Model():

    def before_dump(self):
        pass

    def dump(self):
        self.before_dump()
        print('\n>>>>>>>>>    I AM DUMPING NOW!!!!!!!')
        print(json.dumps(self))
        # with open....
        #     json.dumps(self)
        pass
