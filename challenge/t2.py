import traceback
log = open("challenge/log.txt", "w")
try:
	/rank
except Exception as e:
	traceback.print_exc(file=log)
log.close()