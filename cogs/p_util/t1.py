import traceback
log = open("cogs/p_util/plog.txt", "w")
try:
	print("database")
except Exception as e:
	traceback.print_exc(file=log)
log.close()