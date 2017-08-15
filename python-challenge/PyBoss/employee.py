from datetime import datetime

class Employee:

	fieldNames = ["Emp ID", "First Name", "Last Name", "DOB", "SSN", "State"]

	us_state_abbrev = {
	    'Alabama': 'AL',
	    'Alaska': 'AK',
	    'Arizona': 'AZ',
	    'Arkansas': 'AR',
	    'California': 'CA',
	    'Colorado': 'CO',
	    'Connecticut': 'CT',
	    'Delaware': 'DE',
	    'Florida': 'FL',
	    'Georgia': 'GA',
	    'Hawaii': 'HI',
	    'Idaho': 'ID',
	    'Illinois': 'IL',
	    'Indiana': 'IN',
	    'Iowa': 'IA',
	    'Kansas': 'KS',
	    'Kentucky': 'KY',
	    'Louisiana': 'LA',
	    'Maine': 'ME',
	    'Maryland': 'MD',
	    'Massachusetts': 'MA',
	    'Michigan': 'MI',
	    'Minnesota': 'MN',
	    'Mississippi': 'MS',
	    'Missouri': 'MO',
	    'Montana': 'MT',
	    'Nebraska': 'NE',
	    'Nevada': 'NV',
	    'New Hampshire': 'NH',
	    'New Jersey': 'NJ',
	    'New Mexico': 'NM',
	    'New York': 'NY',
	    'North Carolina': 'NC',
	    'North Dakota': 'ND',
	    'Ohio': 'OH',
	    'Oklahoma': 'OK',
	    'Oregon': 'OR',
	    'Pennsylvania': 'PA',
	    'Rhode Island': 'RI',
	    'South Carolina': 'SC',
	    'South Dakota': 'SD',
	    'Tennessee': 'TN',
	    'Texas': 'TX',
	    'Utah': 'UT',
	    'Vermont': 'VT',
	    'Virginia': 'VA',
	    'Washington': 'WA',
	    'West Virginia': 'WV',
	    'Wisconsin': 'WI',
	    'Wyoming': 'WY',
	}
		
	def __init__(self, id, fullname, dob_str, ssn, state):
		self.id = id
		self.fullname = fullname
		self.getFirstAndLast()
		self.dob_str = dob_str
		self.getDateOfBirth()
		self.ssn = ssn
		self.getEncryptedSSN()
		self.state = state
		self.getStateAbbr()
		self.createDict()

	def getFirstAndLast(self):
		name = self.fullname.split(" ")
		self.first = name[0]
		if (self.hasExpectedLength(2, name, 2)):
			self.last = " ".join(name[1:])

	def getDateOfBirth(self):
		self.dob = datetime.now()
		if "-" in self.dob_str:
			dob_list = self.dob_str.split("-")
			if (self.hasExpectedLength(1,dob_list,3)): #assume yyyy-mm-dd
				self.dob = datetime(int(dob_list[0]), int(dob_list[1]), int(dob_list[2]))
			else:
				print(f"Employee {self.id} has an invalid date of birth: {self.dob_str}.")
		elif "/" in self.dob_str:
			dob_list = self.dob_str.split("/")
			if (self.hasExpectedLength(1,dob_list,3)): #assume yyyy/mm/dd
				self.dob = datetime(int(dob_list[0]), int(dob_list[1]), int(dob_list[2]))
			else:
				print(f"Employee {self.id} has an invalid date of birth: {self.dob_str}.")
		else: 
			if (self.hasExpectedLength(1,self.dob_str, 8)): #assume mmddyyyy format
				self.dob = datetime(int(self.dob_str[4:7]), int(self.dob_str[0:1]), int(self.dob_str[2:3]))
			else:
				if (self.hasExpectedLength(1,self.dob_str, 6)): #assume mmddyyy format
					self.dob = datetime(int(self.dob_str[4:5]), int(self.dob_str[0:1]), int(self.dob_str[2:3]))
				else:
					print(f"Employee {self.id} has an invalid date of birth: {self.dob_str}.")
	
	
	def getEncryptedSSN(self):
		self.encrypted_ssn = "***-**-****"
		if "-" in self.ssn:
			ssn_list = self.ssn.split("-")
			if (self.hasExpectedLength(1,ssn_list,3)):
				if (self.hasExpectedLength(1,ssn_list[2],4)):
					self.encrypted_ssn = "***-**-" + ssn_list[2]
				else:
					print(f"Employee {self.id} has an invalid Social Security: {self.ssn}.")
			else:
				print(f"Employee {self.id} has an invalid Social Security: {self.ssn}.")
		else:
			print(f"Employee {self.id} has an invalid Social Security: {self.ssn}.")

	def getStateAbbr(self):
		if (self.hasExpectedLength(1, self.state,2)):
			self.state_abbr = self.state
			return 
		
		if self.state in self.us_state_abbrev:
			self.state_abbr = self.us_state_abbrev[self.state]
		else:
			self.state_abbr = ""
			print(f"Employee {self.id} has an invalid state: {self.state}")

	def printSummary(self):
		print(f"Employee ID {self.id} Name: {self.fullname} DOB: {self.dob_str} SSN: {self.ssn}  State: {self.state}")
		print(f"First: {self.first} Last: {self.last} DOB: {datetime.strftime(self.dob,'%m/%d/%Y')} SSN: {self.encrypted_ssn} State Abbr: {self.state_abbr}")

	def createDict(self):
		self.emp_dict = {"Emp ID": self.id, "First Name": self.first, "Last Name": self.last, "DOB": datetime.strftime(self.dob,'%m/%d/%Y'), "SSN": self.encrypted_ssn, "State": self.state_abbr}

	def hasExpectedLength(self, mode, val1, val2):
		if (mode == 1):
			if (len(val1) == val2):
				return True
			else:
				return False
		else:
			if (len(val1) >= val2):
				return True
			else:
				return False

if __name__ == "__main__":
    main()