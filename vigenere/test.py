def test(isLowerCase,listVal):
	print("\n\n")
	alpha = "abcdefghijklmnopqrstuvwxyz"

	if not isLowerCase:
		alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	calc={}
	P=[]
	N = len(listVal)
	for v in alpha:
		calc[v]=0
	for i in range(N):
		calc[listVal[i]]+=1

	for v in alpha:
		# calc[v]/=N
		P.append(calc[v])
	print(P)
	return P

	
import math

eng_freq = [.0817, .0149, .0278, .0425, .1270, .0223, .0202, .0609, .0697, .0015, .0077, .0403, .0241, .0675, .0751,
            .0193, .0010, .0599, .0633, .0906, .0276, .0098, .0236, .0015, .0197, .0007]

cur = "westandtodayonthebrinkofarevolutionincryptographythedevelopmentofcheapdigitalhardwarehasfreeditfromthedesignlimitationsofmechanicalcomputingandbroughtthecostofhighgradecryptographicdevicesdowntowheretheycanbeusedinsuchcommercialapplicationsasremotecashdispensersandcomputerterminalsinturnsuchapplicationscreateaneedfornewtypesofcryptographicsystemswhichminimizethenecessityofsecurekeydistributionchannelsandsupplytheequivalentofawrittensignatureatthesametimetheoreticaldevelopmentsininformationtheoryandcomputerscienceshowpromiseofprovidingprovablysecurecryptosystemschangingthisancientartintoasciencethedevelopmentofcomputercontrolledcommunicationnetworkspronseseffortlessandinexpensivecontactbetweenpeopleorcomputersonoppositesidesoftheworldreplacingmostmailandmanyexcursionswithtelecommunicationsformanyapplicationsthesecontactsmustbemadesecureagainstbotheavesdroppingandtheinjectionofillegitimatemessagesatpresenth"

a = test(True,cur)

b = [ math.floor(i * len(cur)) for i in eng_freq ]

print(b)

c=[]
for i in range(len(a)):
	c.append(a[i]-b[i])

print(c)