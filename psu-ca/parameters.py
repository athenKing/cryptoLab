CONFIG = {
	"iknp":{
		"secureCoeffic" : 10,
		"PRIME" : (1<<521) - 1,
		"mLen" : 521
	}
	,
	"bloomFilterCapacity":5000
	,
	"networkPort":{
	"iknpAlice":'http://0.0.0.0:9000/',
	"iknpBob":"http://0.0.0.0:9001/",
	"aliceServer":'http://0.0.0.0:9002/'
	}
}