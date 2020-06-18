from flask import Flask,jsonify,request
import json

iknpAliceEntity = Flask("IKNPAlice")

@iknpAliceEntity.route('/onInit',methods=['POST'])
def onInit():
	global ikAlice

	data = json.loads(request.get_json())
	
	secureCoeffic = data['secureCoeffic']
	mNumber = data['mNumber']
	messages = data['messages']

	print(messages)

	mLen = data['mLen']

	# ikAlice  = iknpAlice(secureCoeffic,mNumber,messages,mLen)#belong to outside caller
	# aliceRandomSecret = ikAlice.getRandomSecrets()#belong to outside caller


	return "Success"


@iknpAliceEntity.route('/onReset',methods=['GET'])
def onReset():
	return "success"


if __name__ == "__main__":
    #Start the sender
    iknpAliceEntity.run(host='0.0.0.0',port=9000)