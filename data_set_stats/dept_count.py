from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


'''Counts number of courses in each department from the courses_data_set.json file'''

class DeptCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def map_dept(self, _, record):
        for i in record:
            yield [record[i]['dept_code'], 1]
				
    def count_dept(self, dept, counts):
        yield [dept, sum(counts)]
        
		
    def steps(self):
        return [self.mr(self.map_dept, self.count_dept)]
		
if __name__ == '__main__':
    DeptCount.run()
