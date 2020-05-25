import smartpy as sp

# A smart contract developed in SmartPy to track student attendance.
# Does not yet provide support for Tezos transaction between addresses.
# 
# @author Finn Frankis
# @version 5/23/20
class AttendanceTracker(sp.Contract):
   def __init__(self):
      self.init(attendanceMap = sp.map(tkey=sp.TNat))
      
   @sp.entry_point
   # Adds an empty date to the attendance map.
   #
   # @param params.month the integer value representing the month
   # @param params.day the integer value representing the day
   # @param params.year the integer value representing the year
   def addDate(self, params):
      sp.set_type(params.month, sp.TNat)
      sp.set_type(params.day, sp.TNat)
      sp.set_type(params.year, sp.TNat)

      self.checkDate(self.date_to_int(params.month, params.day, params.year))
      
   @sp.entry_point
   # Adds an student entry associated with a given date to the attendance map.
   #
   # @param params.month the natural integer value representing the month
   # @param params.day the natural integer value representing the day
   # @param params.year the natural integer value representing the year
   # @param params.student the string value representing the student's name
   def addStudent(self, params):
      # Assert the types of the relevant variables: SmartPy is strongly typed 
      sp.set_type(params.month, sp.TNat)
      sp.set_type(params.day, sp.TNat)
      sp.set_type(params.year, sp.TNat)
      sp.set_type(params.student, sp.TString)

      # Necessary logical verification steps before the contract can proceed
      sp.verify(params.month <= 12)
      sp.verify(params.day <= 31)
      sp.verify(sp.len(params.student) > 0) # non-empty student name

      date = self.date_to_int(params.month, params.day, params.year)
      self.checkDate(date)
      self.data.attendanceMap[date].push(params.student)
   
   # Checks whether a given date value is contained within the attendance map; if not,
   # adds the date.
   #
   # @param date the date value as represented as a key in the attendance map
   def checkDate(self, date):
      sp.if ~(self.data.attendanceMap.contains(date)):
         self.data.attendanceMap[date] = sp.list(t=sp.TString)
   
   # Converts a date represented by a month, day, and year into a unique
   # integer representation in units of days.
   def date_to_int(self, month, day, year):
      return year * 12 * 31 + month * 31 + day
         

@add_test("Student Test")
# Test method for evaluation only within the SmartPy IDE. Ensures that 
# a given set of students wih corresponding dates can be added.
def test():
   scenario = sp.test_scenario()
   
   at = AttendanceTracker()
   scenario += at
   
   tom = sp.test_account("Tom")
   scenario += at.addStudent(month=10,day=24,year=2019, student="Finn").run()
   scenario += at.addStudent(month=10,day=24,year=2019, student="Jim").run()
   scenario += at.addStudent(month=10,day=24,year=2019, student="Tim").run()
   scenario += at.addStudent(month=10,day=29,year=2019, student="Tim").run()